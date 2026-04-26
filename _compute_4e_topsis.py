"""
基于数据库中的4E维度得分（score_c1-c4）+ 数据集数量 + 功能指标，
重新计算TOPSIS，构建完整的4E评估体系
"""
import sqlite3
import json
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime

DB_PATH = Path('data/ogd_database.db')

def load_data():
    """加载19个有维度得分的省级平台数据，使用v3采集的数据集数量"""
    # 加载v3采集结果（包含更准确的数据集数量）
    try:
        with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
            v3_results = json.load(f)
        v3_datasets = {r['code']: r.get('dataset_count', 0) or 0 
                       for r in v3_results if r.get('status') == 'success'}
        print(f"  加载v3数据集数量: {len(v3_datasets)}个平台")
    except FileNotFoundError:
        v3_datasets = {}
        print("  v3_collection_results.json未找到，使用数据库数据")
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            p.code, p.name, p.province, p.region, p.launch_year,
            cr.dataset_count, cr.app_count,
            cr.score_c1, cr.score_c2, cr.score_c3, cr.score_c4,
            cr.has_https, cr.has_search, cr.has_download, cr.has_api,
            cr.has_visualization, cr.has_update_info, cr.has_metadata, 
            cr.has_feedback, cr.has_register, cr.has_preview, cr.has_bulk_download,
            cr.response_time
        FROM platforms p
        JOIN (
            SELECT platform_code, MAX(id) as max_id 
            FROM collection_records 
            WHERE score_c1 IS NOT NULL AND score_c1 > 0
            GROUP BY platform_code
        ) latest ON p.code = latest.platform_code
        JOIN collection_records cr ON latest.max_id = cr.id
        WHERE p.tier = '省级'
        ORDER BY p.code
    """)
    
    rows = cursor.fetchall()
    data = []
    for r in rows:
        d = dict(r)
        code = d['code']
        # 优先使用v3采集的数据集数量
        if code in v3_datasets and v3_datasets[code] > 0:
            d['dataset_count'] = v3_datasets[code]
        else:
            d['dataset_count'] = int(d.get('dataset_count') or 0)
        d['app_count'] = int(d.get('app_count') or 0)
        d['score_c1'] = float(d.get('score_c1') or 0)
        d['score_c2'] = float(d.get('score_c2') or 0)
        d['score_c3'] = float(d.get('score_c3') or 0)
        d['score_c4'] = float(d.get('score_c4') or 0)
        d['response_time'] = float(d.get('response_time') or 3000)
        for ind in ['has_https', 'has_search', 'has_download', 'has_api',
                    'has_visualization', 'has_update_info', 'has_metadata',
                    'has_feedback', 'has_register', 'has_preview', 'has_bulk_download']:
            d[ind] = int(d.get(ind) or 0)
        data.append(d)
    
    conn.close()
    return data

def compute_4e_indicators(data):
    """构建完整的4E指标体系"""
    df = pd.DataFrame(data)
    n = len(df)
    
    # E1 供给保障 (Supply)
    # - 数据集数量 (对数标准化，避免极端值主导)
    df['dataset_count_log'] = np.log1p(df['dataset_count'])
    max_log = df['dataset_count_log'].max()
    df['E1_dataset'] = df['dataset_count_log'] / max_log if max_log > 0 else 0
    # - 供给保障维度得分
    df['E1_score'] = df['score_c1']
    # - 综合供给指标
    df['E1'] = (df['E1_dataset'] * 0.5 + df['E1_score'] * 0.5)
    
    # E2 平台服务 (Service)
    # - 平台服务维度得分
    df['E2_score'] = df['score_c2']
    # - 功能完备度 (11个功能指标之和/11)
    func_cols = ['has_https', 'has_search', 'has_download', 'has_api',
                 'has_visualization', 'has_update_info', 'has_metadata',
                 'has_feedback', 'has_register', 'has_preview', 'has_bulk_download']
    df['E2_func'] = df[func_cols].sum(axis=1) / len(func_cols)
    # - 响应速度 (反转标准化)
    max_rt = df['response_time'].max()
    df['E2_speed'] = 1 - (df['response_time'] / max_rt) if max_rt > 0 else 0
    # - 综合平台服务指标
    df['E2'] = (df['E2_score'] * 0.5 + df['E2_func'] * 0.3 + df['E2_speed'] * 0.2)
    
    # E3 数据质量 (Quality)
    # - 数据质量维度得分
    df['E3_score'] = df['score_c3']
    # - 元数据完整性
    df['E3_meta'] = df['has_metadata']
    # - 更新信息
    df['E3_update'] = df['has_update_info']
    # - 综合质量指标（降低score_c3权重，因为二值化严重）
    df['E3'] = (df['E3_score'] * 0.4 + df['E3_meta'] * 0.3 + df['E3_update'] * 0.3)
    
    # E4 利用效果 (Usage)
    # - 利用效果维度得分
    df['E4_score'] = df['score_c4']
    # - 应用数量 (标准化)
    max_apps = df['app_count'].max()
    df['E4_app'] = df['app_count'] / max_apps if max_apps > 0 else 0
    # - 综合利用效果指标
    df['E4'] = (df['E4_score'] * 0.7 + df['E4_app'] * 0.3)
    
    # E5 公平性 (Equity) - 基于已有指标推导
    # - 免费开放程度 (所有平台都是免费，设为1)
    df['E5_open'] = 1.0
    # - 无障碍访问 (有https视为基本无障碍)
    df['E5_access'] = df['has_https']
    # - 反馈渠道 (有反馈视为可参与)
    df['E5_feedback'] = df['has_feedback']
    # - 综合公平性指标
    df['E5'] = (df['E5_open'] * 0.4 + df['E5_access'] * 0.3 + df['E5_feedback'] * 0.3)
    
    return df

def topsis_4e(df):
    """基于4E维度的TOPSIS计算"""
    # 决策矩阵
    indicators = ['E1', 'E2', 'E3', 'E4', 'E5']
    X = df[indicators].values.astype(float)
    n = len(df)
    
    # 数据标准化（向量归一化）
    X_norm = X / np.sqrt((X**2).sum(axis=0))
    
    # 使用等权重（各维度同等重要）
    # 理由：4E框架的理论设计认为四个维度同等重要
    # E5公平性作为补充维度，权重略低
    w = np.array([0.22, 0.22, 0.22, 0.22, 0.12])
    
    print("4E维度权重（理论等权重）:")
    for ind, weight in zip(indicators, w):
        print(f"  {ind}: {weight:.4f}")
    
    # 加权标准化
    V = X_norm * w
    
    # 理想解
    V_plus = V.max(axis=0)
    V_minus = V.min(axis=0)
    
    # 距离
    D_plus = np.sqrt(((V - V_plus) ** 2).sum(axis=1))
    D_minus = np.sqrt(((V - V_minus) ** 2).sum(axis=1))
    
    # TOPSIS得分
    C = D_minus / (D_plus + D_minus + 1e-10)
    
    df['topsis_score'] = C
    df['topsis_rank'] = df['topsis_score'].rank(ascending=False).astype(int)
    df['weights'] = [w.tolist()] * len(df)
    
    return df

def classify_tier(score):
    """根据得分划分梯队"""
    if score >= 0.7:
        return '第一梯队'
    elif score >= 0.4:
        return '第二梯队'
    else:
        return '第三梯队'

def export_results(df):
    """导出结果"""
    output_dir = Path('data/verified_dataset')
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 排序
    df_sorted = df.sort_values('topsis_score', ascending=False)
    
    # 添加梯队
    df_sorted['tier'] = df_sorted['topsis_score'].apply(classify_tier)
    
    # 导出CSV
    export_cols = ['code', 'name', 'province', 'region', 'topsis_score', 'topsis_rank', 'tier',
                   'E1', 'E2', 'E3', 'E4', 'E5',
                   'E1_score', 'E2_score', 'E3_score', 'E4_score',
                   'dataset_count', 'app_count']
    df_sorted[export_cols].to_csv(output_dir / f'table_topsis_4e_{timestamp}.csv', 
                                   index=False, encoding='utf-8-sig')
    
    # 打印结果
    print("\n=== 4E-TOPSIS排名 ===")
    print(f"{'排名':<4} {'平台':<10} {'得分':<8} {'梯队':<8} {'E1供给':<7} {'E2服务':<7} {'E3质量':<7} {'E4利用':<7} {'E5公平':<7}")
    print("-" * 70)
    for _, row in df_sorted.iterrows():
        print(f"{row['topsis_rank']:<4} {row['name']:<10} {row['topsis_score']:<8.3f} "
              f"{row['tier']:<8} {row['E1']:<7.3f} {row['E2']:<7.3f} "
              f"{row['E3']:<7.3f} {row['E4']:<7.3f} {row['E5']:<7.3f}")
    
    print(f"\n结果已保存到: {output_dir}/table_topsis_4e_{timestamp}.csv")
    return df_sorted

def main():
    print("=" * 80)
    print("基于4E维度的TOPSIS重新计算")
    print("=" * 80)
    
    # 1. 加载数据
    print("\n[1/4] 加载平台数据...")
    data = load_data()
    print(f"  加载平台数: {len(data)}")
    
    # 2. 构建4E指标
    print("\n[2/4] 构建4E指标体系...")
    df = compute_4e_indicators(data)
    print("  E1=供给保障(数据集+维度得分)")
    print("  E2=平台服务(维度得分+功能完备度+响应速度)")
    print("  E3=数据质量(维度得分+元数据+更新)")
    print("  E4=利用效果(维度得分+应用数量)")
    print("  E5=公平性(开放+无障碍+反馈)")
    
    # 3. TOPSIS计算
    print("\n[3/4] 计算熵权TOPSIS...")
    df = topsis_4e(df)
    
    # 4. 导出
    print("\n[4/4] 导出结果...")
    df = export_results(df)
    
    print("\n" + "=" * 80)
    print("4E-TOPSIS计算完成!")
    print("=" * 80)

if __name__ == '__main__':
    main()
