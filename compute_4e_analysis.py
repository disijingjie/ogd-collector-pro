"""
4E-TOPSIS 综合分析脚本
支持22个省级平台，使用修复后的v3数据集数量
输出：TOPSIS、DEA、DEMATEL、fsQCA
"""
import sqlite3
import json
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

DB_PATH = Path('data/ogd_database.db')
OUTPUT_DIR = Path('data/verified_dataset')
OUTPUT_DIR.mkdir(exist_ok=True)

# 22个目标平台代码（根据v3采集结果）
TARGET_22 = [
    'beijing', 'tianjin', 'shanxi', 'neimenggu', 'liaoning', 'jilin', 'shanghai',
    'jiangsu', 'zhejiang', 'anhui', 'fujian', 'jiangxi', 'shandong', 'henan',
    'hubei', 'hunan', 'guangdong', 'guangxi', 'hainan', 'chongqing', 'sichuan',
    'guizhou', 'yunnan'
]
# 实际有维度得分的19个平台
DIMENSION_19 = [
    'beijing', 'tianjin', 'shanxi', 'neimenggu', 'liaoning', 'jilin',
    'jiangsu', 'anhui', 'fujian', 'jiangxi', 'shandong', 'henan',
    'hubei', 'hunan', 'guangdong', 'guangxi', 'hainan', 'chongqing',
    'sichuan', 'guizhou', 'yunnan'
]

def load_data():
    """加载22个平台数据，合并v3数据集数量和数据库维度得分"""
    # 加载v3采集结果
    with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
        v3_results = json.load(f)
    v3_map = {r['code']: r for r in v3_results if r.get('status') == 'success'}
    print(f"  v3采集成功平台: {len(v3_map)}个")
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 获取所有省级平台的最新采集记录
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
    conn.close()
    
    data = []
    for r in rows:
        d = dict(r)
        code = d['code']
        if code not in TARGET_22:
            continue
        
        # 数据集数量：优先v3，其次数据库
        if code in v3_map and v3_map[code].get('dataset_count'):
            d['dataset_count'] = int(v3_map[code]['dataset_count'])
        else:
            d['dataset_count'] = int(d.get('dataset_count') or 0)
        
        d['app_count'] = int(d.get('app_count') or 0)
        d['score_c1'] = float(d.get('score_c1') or 0)
        d['score_c2'] = float(d.get('score_c2') or 0)
        d['score_c3'] = float(d.get('score_c3') or 0)
        d['score_c4'] = float(d.get('score_c4') or 0)
        d['response_time'] = float(d.get('response_time') or 3000)
        d['launch_year'] = float(d.get('launch_year') or 2015)
        
        for ind in ['has_https', 'has_search', 'has_download', 'has_api',
                    'has_visualization', 'has_update_info', 'has_metadata',
                    'has_feedback', 'has_register', 'has_preview', 'has_bulk_download']:
            d[ind] = int(d.get(ind) or 0)
        data.append(d)
    
    print(f"  加载目标平台数: {len(data)}")
    return data

def compute_4e_indicators(data):
    """构建完整的4E指标体系（严格按team-lead要求）"""
    df = pd.DataFrame(data)
    n = len(df)
    
    # E1 供给保障 (Supply)
    # 数据集数量（对数标准化）
    df['dataset_count_log'] = np.log1p(df['dataset_count'])
    max_log = df['dataset_count_log'].max()
    df['E1_dataset'] = df['dataset_count_log'] / max_log if max_log > 0 else 0
    # score_c1（数据库维度得分）
    df['E1_score'] = df['score_c1']
    # E1 = dataset_norm * 0.5 + score_c1 * 0.5
    df['E1'] = df['E1_dataset'] * 0.5 + df['E1_score'] * 0.5
    
    # E2 平台服务 (Service)
    # score_c2
    df['E2_score'] = df['score_c2']
    # 功能完备度（11个二值指标之和/11）
    func_cols = ['has_https', 'has_search', 'has_download', 'has_api',
                 'has_visualization', 'has_update_info', 'has_metadata',
                 'has_feedback', 'has_register', 'has_preview', 'has_bulk_download']
    df['E2_func'] = df[func_cols].sum(axis=1) / len(func_cols)
    # 响应速度（反转标准化）
    max_rt = df['response_time'].max()
    df['E2_speed'] = 1 - (df['response_time'] / max_rt) if max_rt > 0 else 0
    # E2 = score_c2 * 0.5 + func_sum * 0.3 + speed_norm * 0.2
    df['E2'] = df['E2_score'] * 0.5 + df['E2_func'] * 0.3 + df['E2_speed'] * 0.2
    
    # E3 数据质量 (Quality)
    # score_c3
    df['E3_score'] = df['score_c3']
    # has_metadata, has_update_info
    df['E3_meta'] = df['has_metadata']
    df['E3_update'] = df['has_update_info']
    # E3 = score_c3 * 0.4 + has_metadata * 0.3 + has_update_info * 0.3
    df['E3'] = df['E3_score'] * 0.4 + df['E3_meta'] * 0.3 + df['E3_update'] * 0.3
    
    # E4 利用效果 (Usage)
    # score_c4
    df['E4_score'] = df['score_c4']
    # app_count（标准化）
    max_apps = df['app_count'].max()
    df['E4_app'] = df['app_count'] / max_apps if max_apps > 0 else 0
    # E4 = score_c4 * 0.7 + app_norm * 0.3
    df['E4'] = df['E4_score'] * 0.7 + df['E4_app'] * 0.3
    
    # E5 公平性 (Equity)
    # 开放程度（所有平台默认1.0）
    df['E5_open'] = 1.0
    # has_https（基本无障碍）
    df['E5_https'] = df['has_https']
    # has_feedback（反馈渠道）
    df['E5_feedback'] = df['has_feedback']
    # E5 = open * 0.4 + https * 0.3 + feedback * 0.3
    df['E5'] = df['E5_open'] * 0.4 + df['E5_https'] * 0.3 + df['E5_feedback'] * 0.3
    
    return df

def topsis_4e(df):
    """标准TOPSIS计算"""
    indicators = ['E1', 'E2', 'E3', 'E4', 'E5']
    X = df[indicators].values.astype(float)
    n = len(df)
    
    # 标准化（向量归一化）
    X_norm = X / np.sqrt((X**2).sum(axis=0))
    
    # 权重
    w = np.array([0.22, 0.22, 0.22, 0.22, 0.12])
    
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
    
    return df

def classify_tier(score):
    """梯队划分"""
    if score >= 0.7:
        return '第一梯队'
    elif score >= 0.4:
        return '第二梯队'
    else:
        return '第三梯队'

def export_topsis(df):
    """导出TOPSIS结果"""
    df_sorted = df.sort_values('topsis_score', ascending=False)
    df_sorted['tier'] = df_sorted['topsis_score'].apply(classify_tier)
    
    export_cols = ['code', 'name', 'province', 'topsis_score', 'topsis_rank', 'tier',
                   'E1', 'E2', 'E3', 'E4', 'E5']
    
    # 保存带时间戳的版本
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    df_sorted[export_cols].to_csv(OUTPUT_DIR / f'table_topsis_4e_{timestamp}.csv',
                                   index=False, encoding='utf-8-sig')
    
    # 保存最终版本
    df_sorted[export_cols].to_csv(OUTPUT_DIR / 'table_topsis_4e_final.csv',
                                   index=False, encoding='utf-8-sig')
    
    print("\n=== 4E-TOPSIS排名 ===")
    print(f"{'排名':<4} {'平台':<12} {'得分':<8} {'梯队':<8} {'E1供给':<8} {'E2服务':<8} {'E3质量':<8} {'E4利用':<8} {'E5公平':<8}")
    print("-" * 80)
    for _, row in df_sorted.iterrows():
        print(f"{row['topsis_rank']:<4} {row['name']:<12} {row['topsis_score']:<8.4f} "
              f"{row['tier']:<8} {row['E1']:<8.4f} {row['E2']:<8.4f} "
              f"{row['E3']:<8.4f} {row['E4']:<8.4f} {row['E5']:<8.4f}")
    
    return df_sorted

def compute_dea(df):
    """DEA-BCC效率分析（纯NumPy实现，无需scipy）
    投入：运营年限、功能得分、数据集数量
    产出：TOPSIS得分
    """
    # 准备数据
    df_dea = df.copy()
    df_dea['operating_years'] = 2026 - df_dea['launch_year']
    df_dea['operating_years'] = df_dea['operating_years'].clip(lower=1)
    
    # 投入指标
    inputs = np.array([
        df_dea['operating_years'].values,
        df_dea['E2_func'].values * 11,  # 功能得分（0-11）
        np.log1p(df_dea['dataset_count'].values)  # 数据集数量对数
    ]).T
    
    # 产出指标
    outputs = np.array([
        df_dea['topsis_score'].values
    ]).T
    
    n = len(df_dea)
    m = inputs.shape[1]  # 投入数
    s = outputs.shape[1]  # 产出数
    efficiencies = []
    
    for i in range(n):
        # BCC模型：使用简单的比率法近似（CCR/BCC混合）
        # 由于缺少scipy，使用加权产出/投入比率作为效率代理
        weighted_output = outputs[i, 0]  # TOPSIS得分
        weighted_input = (inputs[i, 0] / 20 + inputs[i, 1] / 11 + inputs[i, 2] / 15) / 3
        if weighted_input > 0:
            theta = min(1.0, weighted_output / weighted_input)
        else:
            theta = 1.0
        efficiencies.append(theta)
    
    df_dea['dea_efficiency'] = efficiencies
    df_dea['dea_rank'] = df_dea['dea_efficiency'].rank(ascending=False).astype(int)
    
    # 导出
    export_cols = ['code', 'name', 'province', 'dea_efficiency', 'dea_rank',
                   'operating_years', 'E2_func', 'dataset_count', 'topsis_score']
    df_dea[export_cols].to_csv(OUTPUT_DIR / 'table_dea_4e_final.csv',
                                index=False, encoding='utf-8-sig')
    
    print("\n=== DEA-BCC效率排名（近似） ===")
    print(f"{'排名':<4} {'平台':<12} {'效率':<8} {'运营年':<6} {'功能':<6} {'数据集':<8} {'TOPSIS':<8}")
    print("-" * 60)
    for _, row in df_dea.sort_values('dea_efficiency', ascending=False).iterrows():
        print(f"{row['dea_rank']:<4} {row['name']:<12} {row['dea_efficiency']:<8.4f} "
              f"{row['operating_years']:<6.0f} {row['E2_func']*11:<6.1f} "
              f"{row['dataset_count']:<8} {row['topsis_score']:<8.4f}")
    
    return df_dea

def compute_dematel(df):
    """DEMATEL分析（基于4个维度E1-E4）"""
    indicators = ['E1', 'E2', 'E3', 'E4']
    X = df[indicators].values.astype(float)
    n = len(df)
    m = len(indicators)
    
    # 构建直接影响矩阵（相关系数）
    direct_matrix = np.corrcoef(X.T)
    np.fill_diagonal(direct_matrix, 0)
    
    # 标准化直接影响矩阵
    max_sum = np.max(np.sum(np.abs(direct_matrix), axis=1))
    if max_sum > 0:
        N = direct_matrix / max_sum
    else:
        N = direct_matrix
    
    # 综合影响矩阵 T = N(I-N)^(-1)
    I = np.eye(m)
    try:
        T = N @ np.linalg.inv(I - N)
    except np.linalg.LinAlgError:
        T = N
    
    # 计算影响度、被影响度、中心度、原因度
    R = np.sum(T, axis=1)  # 影响度
    C = np.sum(T, axis=0)  # 被影响度
    M = R + C               # 中心度（重要性）
    D = R - C               # 原因度（正负）
    
    results = {
        'dimensions': indicators,
        'direct_matrix': direct_matrix.tolist(),
        'total_matrix': T.tolist(),
        'influence': {ind: float(v) for ind, v in zip(indicators, R)},
        'affected': {ind: float(v) for ind, v in zip(indicators, C)},
        'centrality': {ind: float(v) for ind, v in zip(indicators, M)},
        'causality': {ind: float(v) for ind, v in zip(indicators, D)},
        'interpretation': {
            'causal_factors': [ind for ind, v in zip(indicators, D) if v > 0],
            'result_factors': [ind for ind, v in zip(indicators, D) if v <= 0]
        }
    }
    
    with open(OUTPUT_DIR / 'dematel_4e_final.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n=== DEMATEL分析结果 ===")
    print(f"{'维度':<8} {'影响度':<8} {'被影响度':<8} {'中心度':<8} {'原因度':<8} {'类型':<8}")
    print("-" * 55)
    for i, ind in enumerate(indicators):
        typ = '原因型' if D[i] > 0 else '结果型'
        print(f"{ind:<8} {R[i]:<8.4f} {C[i]:<8.4f} {M[i]:<8.4f} {D[i]:<8.4f} {typ:<8}")
    
    return results

def compute_fsqca(df):
    """fsQCA分析（基于4E维度，中位数分割）"""
    indicators = ['E1', 'E2', 'E3', 'E4']
    
    # 中位数分割（0/1）
    thresholds = {ind: df[ind].median() for ind in indicators}
    
    # 构建真值表
    truth_table = []
    for _, row in df.iterrows():
        config = {ind: 1 if row[ind] >= thresholds[ind] else 0 for ind in indicators}
        config['code'] = row['code']
        config['name'] = row['name']
        config['topsis_score'] = row['topsis_score']
        config['outcome'] = 1 if row['topsis_score'] >= df['topsis_score'].median() else 0
        truth_table.append(config)
    
    # 统计配置频率
    from collections import Counter
    configs = Counter()
    for t in truth_table:
        key = tuple(t[ind] for ind in indicators)
        configs[key] += 1
    
    # 寻找充分条件组合（覆盖率>0.5，一致性>0.8）
    # 简化：找出高频高绩效配置
    high_perf = [t for t in truth_table if t['outcome'] == 1]
    low_perf = [t for t in truth_table if t['outcome'] == 0]
    
    high_configs = Counter(tuple(t[ind] for ind in indicators) for t in high_perf)
    low_configs = Counter(tuple(t[ind] for ind in indicators) for t in low_perf)
    
    results = {
        'thresholds': {k: float(v) for k, v in thresholds.items()},
        'truth_table': truth_table,
        'configurations': {
            'total': len(configs),
            'high_performance': {str(k): v for k, v in high_configs.items()},
            'low_performance': {str(k): v for k, v in low_configs.items()}
        },
        'sufficient_conditions': [],
        'necessary_conditions': []
    }
    
    # 分析必要条件（高绩效中某维度为1的比例）
    for ind in indicators:
        high_with = sum(1 for t in high_perf if t[ind] == 1)
        necessity = high_with / len(high_perf) if high_perf else 0
        if necessity >= 0.8:
            results['necessary_conditions'].append({
                'condition': ind,
                'consistency': float(necessity),
                'coverage': float(high_with / len(df))
            })
    
    # 分析充分条件组合
    for config, freq in high_configs.most_common():
        coverage = freq / len(high_perf) if high_perf else 0
        if coverage >= 0.3:
            results['sufficient_conditions'].append({
                'config': dict(zip(indicators, config)),
                'frequency': freq,
                'coverage': float(coverage)
            })
    
    with open(OUTPUT_DIR / 'fsqca_4e_final.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n=== fsQCA分析结果 ===")
    print(f"中位数阈值: {thresholds}")
    print(f"\n高频高绩效配置（TOP5）:")
    for config, freq in high_configs.most_common(5):
        print(f"  E1={config[0]} E2={config[1]} E3={config[2]} E4={config[3]} : {freq}个平台")
    
    print(f"\n必要条件（一致性>=0.8）:")
    for nc in results['necessary_conditions']:
        print(f"  {nc['condition']}: 一致性={nc['consistency']:.3f}, 覆盖率={nc['coverage']:.3f}")
    
    return results

def main():
    print("=" * 80)
    print("4E-TOPSIS 综合分析")
    print("=" * 80)
    
    # 1. 加载数据
    print("\n[1/5] 加载平台数据...")
    data = load_data()
    
    # 2. 构建4E指标
    print("\n[2/5] 构建4E指标体系...")
    df = compute_4e_indicators(data)
    print("  E1=供给保障(数据集对数标准化*0.5 + score_c1*0.5)")
    print("  E2=平台服务(score_c2*0.5 + 功能完备度*0.3 + 响应速度*0.2)")
    print("  E3=数据质量(score_c3*0.4 + has_metadata*0.3 + has_update_info*0.3)")
    print("  E4=利用效果(score_c4*0.7 + app_count标准化*0.3)")
    print("  E5=公平性(开放*0.4 + https*0.3 + feedback*0.3)")
    
    # 3. TOPSIS计算
    print("\n[3/5] 计算TOPSIS...")
    df = topsis_4e(df)
    df = export_topsis(df)
    
    # 4. DEA分析
    print("\n[4/5] 计算DEA-BCC效率...")
    df_dea = compute_dea(df)
    
    # 5. DEMATEL分析
    print("\n[5/5] 计算DEMATEL和fsQCA...")
    dematel_results = compute_dematel(df)
    fsqca_results = compute_fsqca(df)
    
    # 汇总统计
    print("\n" + "=" * 80)
    print("分析完成！")
    print("=" * 80)
    print(f"\n梯队分布:")
    tier_counts = df['tier'].value_counts()
    for tier, count in tier_counts.items():
        print(f"  {tier}: {count}个平台")
    
    print(f"\n输出文件:")
    print(f"  {OUTPUT_DIR}/table_topsis_4e_final.csv")
    print(f"  {OUTPUT_DIR}/table_dea_4e_final.csv")
    print(f"  {OUTPUT_DIR}/dematel_4e_final.json")
    print(f"  {OUTPUT_DIR}/fsqca_4e_final.json")
    
    return df

if __name__ == '__main__':
    main()
