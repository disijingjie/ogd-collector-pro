"""
生成经验证的数据集、计算评估指标、输出验证报告和图表
基于真实采集数据，确保数据来源可追溯
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sqlite3
import json
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
from models import get_db, DB_PATH

# 28个目标样本（31省-青海-甘肃-西藏，含宁夏）
TARGET_PROVINCES = [
    'beijing', 'tianjin', 'hebei', 'shanxi', 'neimenggu',
    'liaoning', 'jilin', 'heilongjiang',
    'shanghai', 'jiangsu', 'zhejiang', 'anhui', 'fujian', 'jiangxi', 'shandong',
    'henan', 'hubei', 'hunan',
    'guangdong', 'guangxi', 'hainan',
    'chongqing', 'sichuan', 'guizhou', 'yunnan',
    'shaanxi', 'ningxia', 'xinjiang'
]

# 区域映射
REGION_MAP = {
    'beijing': '华北', 'tianjin': '华北', 'hebei': '华北', 'shanxi': '华北', 'neimenggu': '华北',
    'liaoning': '东北', 'jilin': '东北', 'heilongjiang': '东北',
    'shanghai': '华东', 'jiangsu': '华东', 'zhejiang': '华东', 'anhui': '华东', 'fujian': '华东', 'jiangxi': '华东', 'shandong': '华东',
    'henan': '华中', 'hubei': '华中', 'hunan': '华中',
    'guangdong': '华南', 'guangxi': '华南', 'hainan': '华南',
    'chongqing': '西南', 'sichuan': '西南', 'guizhou': '西南', 'yunnan': '西南',
    'shaanxi': '西北', 'xinjiang': '西北'
}

def extract_latest_data():
    """提取所有省级平台的最新采集数据"""
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.code, p.name, p.region, p.url,
               cr.status, cr.dataset_count, cr.response_time, cr.has_https, cr.has_search, 
               cr.has_download, cr.has_api, cr.has_visualization, cr.has_update_info, 
               cr.has_metadata, cr.has_feedback, cr.has_register, cr.has_preview,
               cr.score_c1, cr.score_c2, cr.score_c3, cr.score_c4, cr.overall_score,
               cr.collected_at, cr.http_status, cr.status_detail
        FROM platforms p
        LEFT JOIN (
            SELECT platform_code, MAX(id) as max_id 
            FROM collection_records 
            GROUP BY platform_code
        ) latest ON p.code = latest.platform_code
        LEFT JOIN collection_records cr ON latest.max_id = cr.id
        WHERE p.tier = '省级'
        ORDER BY p.code
    """)
    
    rows = cursor.fetchall()
    data = []
    for r in rows:
        row_dict = dict(r)
        row_dict['target_sample'] = r['code'] in TARGET_PROVINCES
        data.append(row_dict)
    
    conn.close()
    return data

def calculate_entropy_weights(df):
    """熵权法计算指标权重"""
    # 使用原始计数指标
    indicators = ['dataset_count', 'has_https', 'has_search', 'has_download', 
                  'has_api', 'has_visualization', 'has_update_info', 
                  'has_metadata', 'has_feedback', 'has_register', 'has_preview']
    
    # 构建指标矩阵（仅对有数据的平台）
    valid_df = df[df['status'] == 'available'].copy()
    if len(valid_df) == 0:
        return None, None
    
    X = valid_df[indicators].values.astype(float)
    
    # 数据标准化（正向化）
    X_min = X.min(axis=0)
    X_max = X.max(axis=0)
    X_norm = (X - X_min) / (X_max - X_min + 1e-10)
    
    # 计算熵值
    p = X_norm / (X_norm.sum(axis=0) + 1e-10)
    e = -np.sum(p * np.log(p + 1e-10), axis=0) / np.log(len(valid_df))
    
    # 计算权重
    g = 1 - e
    w = g / g.sum()
    
    return w, indicators

def calculate_topsis(df, weights, indicators):
    """TOPSIS计算综合得分和排名"""
    valid_df = df[df['status'] == 'available'].copy()
    X = valid_df[indicators].values.astype(float)
    
    # 标准化
    X_min = X.min(axis=0)
    X_max = X.max(axis=0)
    X_norm = (X - X_min) / (X_max - X_min + 1e-10)
    
    # 加权
    X_weighted = X_norm * weights
    
    # 理想解
    V_plus = X_weighted.max(axis=0)
    V_minus = X_weighted.min(axis=0)
    
    # 距离
    D_plus = np.sqrt(((X_weighted - V_plus) ** 2).sum(axis=1))
    D_minus = np.sqrt(((X_weighted - V_minus) ** 2).sum(axis=1))
    
    # 相对贴近度
    C = D_minus / (D_plus + D_minus + 1e-10)
    
    valid_df['topsis_score'] = C
    valid_df['topsis_rank'] = valid_df['topsis_score'].rank(ascending=False).astype(int)
    
    return valid_df

def calculate_4e_scores(df):
    """计算4E维度得分"""
    valid_df = df[df['status'] == 'available'].copy()
    
    # 确保数值列存在且为数值类型
    for col in ['dataset_count', 'has_api', 'has_download', 'response_time', 'has_https', 
                'has_search', 'has_visualization', 'has_update_info', 'has_metadata', 
                'has_feedback', 'has_register', 'has_preview', 'app_count']:
        if col not in valid_df.columns:
            valid_df[col] = 0
        valid_df[col] = pd.to_numeric(valid_df[col], errors='coerce').fillna(0)
    
    # C1: 供给保障 (dataset_count, has_api, has_download)
    ds_max = valid_df['dataset_count'].max() if valid_df['dataset_count'].max() > 0 else 1
    valid_df['C1_supply'] = (
        (valid_df['dataset_count'] / ds_max) * 0.5 +
        valid_df['has_api'] * 0.25 +
        valid_df['has_download'] * 0.25
    )
    
    # C2: 平台服务 (response_time反向, has_https, has_search, has_visualization)
    rt_max = valid_df['response_time'].max() if valid_df['response_time'].max() > 0 else 1
    valid_df['C2_service'] = (
        ((rt_max - valid_df['response_time']) / rt_max) * 0.25 +
        valid_df['has_https'] * 0.25 +
        valid_df['has_search'] * 0.25 +
        valid_df['has_visualization'] * 0.25
    )
    
    # C3: 数据质量 (has_update_info, has_metadata, has_feedback)
    valid_df['C3_quality'] = (
        valid_df['has_update_info'] * 0.4 +
        valid_df['has_metadata'] * 0.3 +
        valid_df['has_feedback'] * 0.3
    )
    
    # C4: 利用效果 (has_register, has_preview, app_count)
    app_max = valid_df['app_count'].max() if valid_df['app_count'].max() > 0 else 1
    valid_df['C4_usage'] = (
        valid_df['has_register'] * 0.3 +
        valid_df['has_preview'] * 0.3 +
        (valid_df['app_count'] / app_max) * 0.4
    )
    
    return valid_df

def generate_verification_report(data, topsis_df, output_dir='data/verified_dataset'):
    """生成数据验证报告"""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    report = {
        'verification_metadata': {
            'generated_at': datetime.now().isoformat(),
            'verification_code': 'OGD-DS-V1-' + timestamp,
            'data_source': 'OGD-Collector Pro 三层架构采集系统',
            'collection_method': 'HTTP请求 + HTML解析 + 功能特征检测',
            'sample_definition': '31个省级行政区中建有独立数据开放平台的28个',
            'excluded': ['青海省(无独立平台)', '甘肃省(无独立平台)', '西藏自治区(无独立平台)'],
            'total_platforms': 31,
            'target_sample': 28,
            'successfully_collected': len([d for d in data if d['status'] == 'available' and d['target_sample']]),
            'failed_collection': len([d for d in data if d['status'] != 'available' and d['target_sample']]),
        },
        'collection_summary': [],
        'failed_platforms': [],
        'data_quality_checks': {},
        'topsis_results': [],
    }
    
    for d in data:
        if not d['target_sample']:
            continue
        entry = {
            'code': d['code'],
            'name': d['name'],
            'region': d['region'],
            'status': d['status'],
            'collected_at': d['collected_at'],
            'url': d['url'],
        }
        if d['status'] == 'available':
            report['collection_summary'].append(entry)
        else:
            report['failed_platforms'].append({
                **entry,
                'failure_reason': d['status_detail'],
                'http_status': d['http_status']
            })
    
    # TOPSIS结果
    if topsis_df is not None:
        for _, row in topsis_df.sort_values('topsis_rank').iterrows():
            report['topsis_results'].append({
                'rank': int(row['topsis_rank']),
                'province': row['name'],
                'code': row['code'],
                'region': row['region'],
                'topsis_score': round(float(row['topsis_score']), 4),
                'dataset_count': int(row['dataset_count'] or 0),
                'response_time': round(float(row['response_time'] or 0), 2),
            })
    
    # 保存报告
    report_path = output_dir / ('verification_report_%s.json' % timestamp)
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    return report, report_path

def export_data_tables(data, topsis_df, output_dir='data/verified_dataset'):
    """导出论文可用的数据表"""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 表1: 采集状态汇总
    status_data = []
    for d in data:
        if not d['target_sample']:
            continue
        status_data.append({
            '序号': len(status_data) + 1,
            '平台名称': d['name'],
            '所属区域': d['region'],
            '平台URL': d['url'],
            '采集状态': '成功' if d['status'] == 'available' else '失败',
            'HTTP状态': d['http_status'] or '-',
            '最新采集时间': (d['collected_at'] or '')[:19],
        })
    df_status = pd.DataFrame(status_data)
    df_status.to_csv(output_dir / ('table1_collection_status_%s.csv' % timestamp), index=False, encoding='utf-8-sig')
    
    # 表2: TOPSIS排名
    if topsis_df is not None:
        topsis_data = []
        for _, row in topsis_df.sort_values('topsis_rank').iterrows():
            topsis_data.append({
                '排名': int(row['topsis_rank']),
                '省级平台': row['name'],
                '所属区域': row['region'],
                'TOPSIS综合得分': round(float(row['topsis_score']), 4),
                '数据集数量': int(row['dataset_count'] or 0),
                '响应时间(s)': round(float(row['response_time'] or 0), 2),
            })
        df_topsis = pd.DataFrame(topsis_data)
        df_topsis.to_csv(output_dir / ('table2_topsis_ranking_%s.csv' % timestamp), index=False, encoding='utf-8-sig')
    
    return output_dir

def main():
    print("=" * 80)
    print("OGD-Collector Pro 经验证数据集生成")
    print("执行时间:", datetime.now().isoformat())
    print("=" * 80)
    
    # 1. 提取数据
    print("\n[1/5] 提取最新采集数据...")
    data = extract_latest_data()
    target_data = [d for d in data if d['target_sample']]
    success_count = len([d for d in target_data if d['status'] == 'available'])
    fail_count = len([d for d in target_data if d['status'] != 'available'])
    print("  目标样本: %d个省级平台" % len(target_data))
    print("  采集成功: %d个" % success_count)
    print("  采集失败: %d个" % fail_count)
    if fail_count > 0:
        print("  失败平台:", ', '.join([d['name'] for d in target_data if d['status'] != 'available']))
    
    # 2. 构建DataFrame
    print("\n[2/5] 构建分析数据集...")
    df = pd.DataFrame(target_data)
    available_df = df[df['status'] == 'available'].copy()
    print("  可用数据行数: %d" % len(available_df))
    
    # 3. 熵权TOPSIS
    print("\n[3/5] 计算熵权TOPSIS...")
    weights, indicators = calculate_entropy_weights(df)
    if weights is not None:
        print("  指标权重:")
        for ind, w in zip(indicators, weights):
            print("    %s: %.4f" % (ind, w))
        topsis_df = calculate_topsis(df, weights, indicators)
        print("  TOPSIS计算完成，最高得分: %.4f (%s)" % (
            topsis_df['topsis_score'].max(),
            topsis_df.loc[topsis_df['topsis_score'].idxmax(), 'name']
        ))
    else:
        topsis_df = None
        print("  数据不足，无法计算TOPSIS")
    
    # 4. 4E维度得分
    print("\n[4/5] 计算4E维度得分...")
    if len(available_df) > 0:
        scored_df = calculate_4e_scores(df)
        print("  4E维度得分计算完成")
    
    # 5. 生成验证报告和数据表
    print("\n[5/5] 生成验证报告和数据表...")
    report, report_path = generate_verification_report(data, topsis_df)
    export_data_tables(data, topsis_df)
    
    print("\n" + "=" * 80)
    print("数据集生成完成!")
    print("验证报告:", report_path)
    print("数据表目录: data/verified_dataset/")
    print("=" * 80)
    
    return report

if __name__ == '__main__':
    main()
