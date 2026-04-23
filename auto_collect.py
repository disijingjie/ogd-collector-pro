#!/usr/bin/env python3
"""
OGD-Collector Pro 每日自动采集脚本
用法: python auto_collect.py [--tier provincial|subprovincial|prefectural|full]
"""

import os
import sys
import sqlite3
import json
import argparse
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models import get_db, DB_PATH
from collector_engine import CollectorEngine


def ensure_data_dir():
    """确保数据目录存在"""
    data_dir = DB_PATH.parent
    data_dir.mkdir(parents=True, exist_ok=True)
    logs_dir = data_dir.parent / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir


def log_message(message, level="INFO"):
    """记录日志"""
    logs_dir = ensure_data_dir()
    log_file = logs_dir / f"auto_collect_{datetime.now().strftime('%Y%m')}.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {message}\n"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())


def run_daily_collection(tier_filter=None, max_workers=3):
    """执行每日采集"""
    log_message(f"开始每日自动采集... tier={tier_filter or 'all'}")

    # 创建采集任务记录
    conn = get_db()
    cursor = conn.cursor()
    task_name = f"自动采集_{datetime.now().strftime('%m%d_%H%M')}"
    task_type = tier_filter or "full"

    cursor.execute("""
        INSERT INTO collection_tasks (task_name, task_type, status, created_at)
        VALUES (?, ?, 'pending', ?)
    """, (task_name, task_type, datetime.now().isoformat()))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()

    log_message(f"创建任务 ID={task_id}, name={task_name}")

    # 构建平台过滤器
    filter_map = {
        'full': None,
        'provincial': {'tier': '省级'},
        'subprovincial': {'tier': '副省级/计划单列市'},
        'prefectural': {'tier': '地级市'}
    }
    platform_filter = filter_map.get(task_type)

    # 创建采集引擎并运行
    engine = CollectorEngine(task_id=task_id, max_workers=max_workers, delay=2)

    try:
        log_message("启动采集引擎...")
        engine.run_collection(platform_filter)

        # 等待完成（同步运行）
        while engine.is_running:
            import time
            time.sleep(2)

        log_message(f"采集完成。成功: {engine.success_count}, 失败: {engine.fail_count}")

        # 汇总统计到 collection_stats 表
        summarize_to_stats(task_id)

        log_message("每日采集任务完成!")
        return True

    except Exception as e:
        log_message(f"采集异常: {e}", "ERROR")
        # 更新任务状态为失败
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE collection_tasks SET status='failed', completed_at=?
            WHERE id=?
        """, (datetime.now().isoformat(), task_id))
        conn.commit()
        conn.close()
        return False


def summarize_to_stats(task_id):
    """将采集结果汇总到 collection_stats 表"""
    conn = get_db()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")

    # 按层级汇总
    cursor.execute("""
        SELECT tier,
               COUNT(*) as total,
               SUM(CASE WHEN status='available' THEN 1 ELSE 0 END) as available,
               ROUND(AVG(CASE WHEN status='available' THEN overall_score ELSE NULL END), 3) as avg_score,
               ROUND(AVG(CASE WHEN status='available' THEN score_c1 ELSE NULL END), 3) as avg_c1,
               ROUND(AVG(CASE WHEN status='available' THEN score_c2 ELSE NULL END), 3) as avg_c2,
               ROUND(AVG(CASE WHEN status='available' THEN score_c3 ELSE NULL END), 3) as avg_c3,
               ROUND(AVG(CASE WHEN status='available' THEN score_c4 ELSE NULL END), 3) as avg_c4,
               SUM(dataset_count) as datasets
        FROM collection_records
        WHERE task_id=? AND tier IS NOT NULL
        GROUP BY tier
    """, (task_id,))

    for row in cursor.fetchall():
        tier, total, available, avg_score, avg_c1, avg_c2, avg_c3, avg_c4, datasets = row
        # 检查是否已有今天的记录
        cursor.execute("""
            SELECT id FROM collection_stats
            WHERE stat_date=? AND tier=? AND task_id=?
        """, (today, tier, task_id))
        existing = cursor.fetchone()

        if existing:
            cursor.execute("""
                UPDATE collection_stats SET
                    total_platforms=?, available_count=?, avg_score=?,
                    avg_c1=?, avg_c2=?, avg_c3=?, avg_c4=?, new_datasets=?
                WHERE id=?
            """, (total, available, avg_score, avg_c1, avg_c2, avg_c3, avg_c4, datasets, existing[0]))
        else:
            cursor.execute("""
                INSERT INTO collection_stats
                (stat_date, task_id, tier, total_platforms, available_count,
                 avg_score, avg_c1, avg_c2, avg_c3, avg_c4, new_datasets)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (today, task_id, tier, total, available, avg_score, avg_c1, avg_c2, avg_c3, avg_c4, datasets))

    conn.commit()
    conn.close()
    log_message(f"统计汇总完成: {today}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OGD每日自动采集')
    parser.add_argument('--tier', choices=['full', 'provincial', 'subprovincial', 'prefectural'],
                        default='full', help='采集层级')
    parser.add_argument('--workers', type=int, default=3, help='并发数')
    args = parser.parse_args()

    run_daily_collection(tier_filter=args.tier, max_workers=args.workers)
