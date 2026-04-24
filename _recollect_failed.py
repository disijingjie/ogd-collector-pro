"""
重新采集失败的省级平台
目标：确保28个样本（31省-青海-甘肃-西藏）都有数据
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sqlite3
import time
import json
from datetime import datetime
from pathlib import Path
from collector_engine import CollectorEngine, create_collection_task
from models import get_db, DB_PATH

# 失败的13个平台（需要重试）
FAILED_PLATFORMS = [
    ('heilongjiang', '黑龙江省', 'https://data.hlj.gov.cn'),
    ('jiangsu', '江苏省', 'https://data.jszwfw.gov.cn:8118/extranet/openportal/pages/default/index.html'),
    ('shanghai', '上海市', 'https://data.sh.gov.cn'),
    ('henan', '河南省', 'https://data.hnzwfw.gov.cn'),
    ('hebei', '河北省', 'https://data.hebei.gov.cn'),
    ('shanxi', '山西省', 'http://data.shanxi.gov.cn'),
    ('shaanxi', '陕西省', 'https://data.shaanxi.gov.cn'),
    ('xinjiang', '新疆维吾尔自治区', 'https://data.xinjiang.gov.cn'),
    ('xizang', '西藏自治区', 'https://data.xizang.gov.cn'),
    ('sichuan', '四川省', 'https://scdata.net.cn'),
    ('gansu', '甘肃省', 'https://data.gansu.gov.cn'),
    ('ningxia', '宁夏回族自治区', 'https://data.nx.gov.cn'),
    ('qinghai', '青海省', 'https://data.qinghai.gov.cn'),
]

def recollect_all():
    """重新采集所有失败平台"""
    print("=" * 80)
    print("重新采集失败的省级平台")
    print("采集时间:", datetime.now().isoformat())
    print("=" * 80)
    
    # 创建采集任务
    task_id = create_collection_task("省级平台补采_" + datetime.now().strftime('%Y%m%d_%H%M%S'), 
                                      "provincial")
    
    engine = CollectorEngine(task_id=task_id, max_workers=2, delay=3)
    
    results = []
    for code, name, url in FAILED_PLATFORMS:
        print(f"\n[{code}] {name} -> {url}")
        result = engine.detect_platform(url, name)
        
        # 保存记录到数据库
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM platforms WHERE code=?", (code,))
        platform_id = cursor.fetchone()
        platform_id = platform_id[0] if platform_id else None
        
        cursor.execute("""
            INSERT INTO collection_records 
            (task_id, platform_id, platform_code, platform_name, tier, region, status, status_detail,
             response_time, http_status, has_https, has_search, has_download, has_api, has_visualization,
             has_update_info, has_metadata, has_feedback, has_register, has_preview, dataset_count, app_count,
             score_c1, score_c2, score_c3, score_c4, overall_score, collected_at)
            VALUES (?, ?, ?, ?, '省级', 
                    (SELECT region FROM platforms WHERE code=?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task_id, platform_id, code, name, code,
            result['status'], result['status_detail'],
            result.get('response_time', 0),
            result.get('http_status', None),
            result.get('has_https', 0),
            result.get('has_search', 0),
            result.get('has_download', 0),
            result.get('has_api', 0),
            result.get('has_visualization', 0),
            result.get('has_update_info', 0),
            result.get('has_metadata', 0),
            result.get('has_feedback', 0),
            result.get('has_register', 0),
            result.get('has_preview', 0),
            result.get('dataset_count', 0),
            result.get('app_count', 0),
            0, 0, 0, 0, 0,  # scores will be calculated later
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
        
        print(f"  状态: {result['status']} | 详情: {result['status_detail']} | 响应: {result.get('response_time', 0):.2f}s")
        results.append({
            'code': code, 'name': name, 'status': result['status'],
            'detail': result['status_detail'], 'response_time': result.get('response_time', 0),
            'http_status': result.get('http_status'), 'collected_at': datetime.now().isoformat()
        })
        time.sleep(2)
    
    # 更新任务状态
    success_count = sum(1 for r in results if r['status'] == 'available')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE collection_tasks 
        SET status='completed', completed_count=?, success_count=?, fail_count=?, completed_at=?
        WHERE id=?
    """, (len(results), success_count, len(results) - success_count, datetime.now().isoformat(), task_id))
    conn.commit()
    conn.close()
    
    # 生成验证报告
    report_path = Path('data') / f"recollection_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            'task_id': task_id,
            'collected_at': datetime.now().isoformat(),
            'total': len(FAILED_PLATFORMS),
            'success': success_count,
            'failed': len(FAILED_PLATFORMS) - success_count,
            'results': results
        }, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 80)
    print("补采完成: 成功 %d / %d" % (success_count, len(FAILED_PLATFORMS)))
    print("验证报告已保存:", report_path)
    return results

if __name__ == '__main__':
    recollect_all()
