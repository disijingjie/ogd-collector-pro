"""
基于22个平台的11个可完整采集指标，完成TOPSIS/DEA/DEMATEL/fsQCA四种方法计算
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sqlite3
import json
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import linprog
from pathlib import Path
from datetime import datetime

DB_PATH = Path('data/ogd_database.db')

# 11个可完整采集的二值指标
BINARY_INDICATORS = [
    'has_https', 'has_search', 'has_download', 'has_api', 
    'has_visualization', 'has_update_info', 'has_metadata', 
    'has_feedback', 'has_register', 'has_preview', 'has_bulk_download'
]

def load_data():
    """加载22个成功采集平台的最新数据"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 获取成功采集的平台
    cursor.execute("""
        SELECT p.code, p.name, p.region, p.launch_year,
               cr.has_https, cr.has_search, cr.has_download, cr.has_api,
               cr.has_visualization, cr.has_update_info, cr.has_metadata,
               cr.has_feedback, cr.has_register, cr.has_preview, cr.has_bulk_download,
               cr.dataset_count, cr.response_time, cr.collected_at
        FROM platforms p
        JOIN (
            SELECT platform_code, MAX(id) as max_id 
            FROM collection_records 
            WHERE status='available'
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
        # 确保所有二值指标为数值
        for ind in BINARY_INDICATORS:
            d[ind] = int(d.get(ind, 0) or 0)
        d['dataset_count'] = int(d.get('dataset_count', 0) or 0)
        d['response_time'] = float(d.get('response_time', 0) or 0)
        d['launch_year'] = int(d.get('launch_year', 2018) or 2018)
        data.append(d)
    
    conn.close()
    return data

def topsis_binary_only(data):
    """基于11个二值指标重新计算TOPSIS"""
    df = pd.DataFrame(data)
    n = len(df)
    
    # 构建决策矩阵（仅11个二值指标）
    X = df[BINARY_INDICATORS].values.astype(float)
    
    # 数据标准化（正向化，所有指标都是正向的）
    # 对于二值指标，直接使用原始值（0或1），因为已经标准化
    
    # 熵权法计算权重
    # 为避免全0或全1列导致的问题，添加微小扰动
    X_entropy = X + 0.001
    p = X_entropy / X_entropy.sum(axis=0)
    e = -np.sum(p * np.log(p), axis=0) / np.log(n)
    g = 1 - e
    w = g / g.sum()
    
    # TOPSIS计算
    X_weighted = X * w
    V_plus = X_weighted.max(axis=0)
    V_minus = X_weighted.min(axis=0)
    
    D_plus = np.sqrt(((X_weighted - V_plus) ** 2).sum(axis=1))
    D_minus = np.sqrt(((X_weighted - V_minus) ** 2).sum(axis=1))
    C = D_minus / (D_plus + D_minus + 1e-10)
    
    df['topsis_score'] = C
    df['topsis_rank'] = df['topsis_score'].rank(ascending=False).astype(int)
    
    return df, w

def dea_bcc(data, topsis_df):
    """DEA-BCC模型计算效率值"""
    # 投入指标
    # I1: 平台运营年限（2026 - launch_year + 1）
    # I2: 功能完善度（11个二值指标之和）
    # I3: 数据集数量（有值就用，0值保留）
    # 产出指标: TOPSIS综合得分
    
    df = topsis_df.copy()
    df['operating_years'] = 2026 - df['launch_year'] + 1
    df['function_score'] = df[BINARY_INDICATORS].sum(axis=1)
    
    n = len(df)
    efficiencies = []
    
    for i in range(n):
        # 当前DMU的投入和产出
        x1 = df.iloc[i]['operating_years']
        x2 = df.iloc[i]['function_score']
        x3 = max(df.iloc[i]['dataset_count'], 1)  # 避免0
        y1 = df.iloc[i]['topsis_score']
        
        # BCC模型（投入导向）
        # min θ
        # s.t. Σλ_j * x_jk ≤ θ * x_k0  (k=1,2,3)
        #      Σλ_j * y_jr ≥ y_r0      (r=1)
        #      Σλ_j = 1
        #      λ_j ≥ 0
        
        c = [1.0] + [0.0] * n  # 目标函数系数: [θ, λ1, λ2, ..., λn]
        
        # 不等式约束: A_ub @ x ≤ b_ub
        A_ub = []
        b_ub = []
        
        # 投入约束1: Σλ_j * x1_j ≤ θ * x1_0  =>  -x1_0 * θ + Σλ_j * x1_j ≤ 0
        row1 = [-x1] + df['operating_years'].tolist()
        A_ub.append(row1)
        b_ub.append(0)
        
        # 投入约束2: Σλ_j * x2_j ≤ θ * x2_0
        row2 = [-x2] + df['function_score'].tolist()
        A_ub.append(row2)
        b_ub.append(0)
        
        # 投入约束3: Σλ_j * x3_j ≤ θ * x3_0
        row3 = [-x3] + [max(v, 1) for v in df['dataset_count'].tolist()]
        A_ub.append(row3)
        b_ub.append(0)
        
        # 产出约束: -Σλ_j * y_j ≤ -y_0  =>  Σλ_j * y_j ≥ y_0
        row4 = [0] + [-v for v in df['topsis_score'].tolist()]
        A_ub.append(row4)
        b_ub.append(-y1)
        
        # 等式约束: Σλ_j = 1
        A_eq = [[0] + [1.0] * n]
        b_eq = [1.0]
        
        # 边界条件
        bounds = [(0, None)] + [(0, None)] * n
        
        try:
            result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, 
                           bounds=bounds, method='highs')
            theta = result.x[0] if result.success else 1.0
        except Exception:
            theta = 1.0
        
        efficiencies.append(theta)
    
    df['dea_efficiency'] = efficiencies
    
    # 计算纯技术效率（PTE）和规模效率（SE）
    # 简化处理：假设规模报酬可变（BCC）的效率即为综合效率
    # 纯技术效率通过CCR模型计算
    df['pte'] = df['dea_efficiency']  # 简化：BCC效率作为综合效率
    df['se'] = 1.0  # 简化处理
    
    return df

def dematel_analysis(data, topsis_df):
    """DEMATEL方法分析影响因素（基于理论推导的直接影响矩阵）"""
    # 四个维度：C1供给保障, C2平台服务, C3数据质量, C4利用效果
    # 基于理论和文献推导的直接影响关系：
    # - C1影响C2（供给保障为平台服务提供基础）
    # - C1影响C3（数据供给为质量管控提供对象）
    # - C1影响C4（供给保障是利用效果的前提）
    # - C2影响C3（平台服务支持质量检测和反馈）
    # - C2影响C4（平台服务降低利用门槛）
    # - C3影响C4（数据质量是利用效果的基础）
    # - C4不影响其他（利用效果是最终结果）
    
    dimensions = ['C1', 'C2', 'C3', 'C4']
    dimension_names = ['供给保障(C1)', '平台服务(C2)', '数据质量(C3)', '利用效果(C4)']
    n_dim = len(dimensions)
    
    # 理论推导的直接影响矩阵（行→列）
    Z = np.array([
        [0.0, 0.7, 0.5, 0.6],   # C1→[C1,C2,C3,C4]
        [0.0, 0.0, 0.4, 0.7],   # C2→[C1,C2,C3,C4]
        [0.0, 0.2, 0.0, 0.6],   # C3→[C1,C2,C3,C4]
        [0.0, 0.0, 0.0, 0.0],   # C4→[C1,C2,C3,C4]
    ])
    
    # 归一化
    Z_max = Z.max()
    if Z_max > 0:
        Z_norm = Z / Z_max
    else:
        Z_norm = Z
    
    # 综合影响矩阵 T = Z(I - Z)^(-1)
    I = np.eye(n_dim)
    try:
        T = Z_norm @ np.linalg.inv(I - Z_norm)
    except np.linalg.LinAlgError:
        T = Z_norm
    
    # 计算中心度和原因度
    R = T.sum(axis=1)
    C = T.sum(axis=0)
    center = R + C
    cause = R - C
    
    dematel_results = {
        'dimensions': dimensions,
        'direct_matrix': Z.tolist(),
        'total_matrix': T.tolist(),
        'R': R.tolist(),
        'C': C.tolist(),
        'center': center.tolist(),
        'cause': cause.tolist(),
        'dimension_names': dimension_names
    }
    
    return dematel_results

def fsqca_analysis(data, topsis_df):
    """fsQCA分析：构建真值表和组态路径"""
    df = topsis_df.copy()
    
    # 构建条件变量（4E维度）
    df['C1_supply'] = (df['has_api'] + df['has_bulk_download']) / 2
    df['C2_service'] = (df['has_https'] + df['has_search'] + df['has_download'] + df['has_visualization']) / 4
    df['C3_quality'] = (df['has_update_info'] + df['has_metadata'] + df['has_feedback']) / 3
    df['C4_usage'] = (df['has_register'] + df['has_preview']) / 2
    
    # 结果变量：高绩效（TOPSIS得分高于中位数）
    median_score = df['topsis_score'].median()
    df['high_performance'] = (df['topsis_score'] >= median_score).astype(int)
    
    # 校准锚点（基于三分位数）
    conditions = ['C1_supply', 'C2_service', 'C3_quality', 'C4_usage']
    
    for col in conditions:
        q33 = df[col].quantile(0.33)
        q50 = df[col].quantile(0.50)
        q67 = df[col].quantile(0.67)
        
        # 将连续值校准为模糊集隶属度
        def calibrate(x):
            if x <= q33:
                return 0.0
            elif x >= q67:
                return 1.0
            else:
                return (x - q33) / (q67 - q33)
        
        df[col + '_fs'] = df[col].apply(calibrate)
    
    # 构建真值表（简化版）
    # 将每个条件变量二值化（0.5为阈值）
    for col in conditions:
        df[col + '_bin'] = (df[col + '_fs'] >= 0.5).astype(int)
    
    # 统计各组态的频次
    config_cols = [c + '_bin' for c in conditions]
    config_df = df.groupby(config_cols).agg({
        'high_performance': ['sum', 'count'],
        'name': lambda x: list(x)
    }).reset_index()
    config_df.columns = config_cols + ['high_perf_count', 'total_count', 'provinces']
    config_df['consistency'] = config_df['high_perf_count'] / config_df['total_count']
    config_df['coverage'] = config_df['high_perf_count'] / df['high_performance'].sum()
    
    # 筛选一致性≥0.8的组态
    valid_configs = config_df[config_df['consistency'] >= 0.8].copy()
    valid_configs = valid_configs.sort_values('consistency', ascending=False)
    
    fsqca_results = {
        'median_score': float(median_score),
        'high_perf_count': int(df['high_performance'].sum()),
        'low_perf_count': int((1 - df['high_performance']).sum()),
        'configurations': valid_configs.to_dict('records'),
        'all_configurations': config_df.to_dict('records')
    }
    
    return fsqca_results

def export_results(data, topsis_df, dea_df, dematel_results, fsqca_results):
    """导出所有计算结果"""
    output_dir = Path('data/verified_dataset')
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # TOPSIS结果
    topsis_export = topsis_df[['code', 'name', 'region', 'topsis_score', 'topsis_rank'] + BINARY_INDICATORS].copy()
    topsis_export.to_csv(output_dir / ('table_topsis_binary_%s.csv' % timestamp), index=False, encoding='utf-8-sig')
    
    # DEA结果
    dea_export = dea_df[['code', 'name', 'region', 'topsis_score', 'dea_efficiency', 'operating_years', 'function_score']].copy()
    dea_export.to_csv(output_dir / ('table_dea_%s.csv' % timestamp), index=False, encoding='utf-8-sig')
    
    # DEMATEL结果
    with open(output_dir / ('dematel_results_%s.json' % timestamp), 'w', encoding='utf-8') as f:
        json.dump(dematel_results, f, ensure_ascii=False, indent=2)
    
    # fsQCA结果
    with open(output_dir / ('fsqca_results_%s.json' % timestamp), 'w', encoding='utf-8') as f:
        json.dump(fsqca_results, f, ensure_ascii=False, indent=2)
    
    # 综合报告
    report = {
        'computed_at': datetime.now().isoformat(),
        'sample_size': len(data),
        'indicators': BINARY_INDICATORS,
        'topsis_weights': {ind: float(w) for ind, w in zip(BINARY_INDICATORS, topsis_df.attrs.get('weights', []))},
        'dematel_summary': {
            'center': {name: float(v) for name, v in zip(dematel_results['dimension_names'], dematel_results['center'])},
            'cause': {name: float(v) for name, v in zip(dematel_results['dimension_names'], dematel_results['cause'])}
        },
        'fsqca_summary': {
            'high_performance_count': fsqca_results['high_perf_count'],
            'valid_configurations': len(fsqca_results['configurations'])
        }
    }
    
    with open(output_dir / ('analysis_report_%s.json' % timestamp), 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("结果已导出到:", output_dir)
    return report

def main():
    print("=" * 80)
    print("四种方法综合计算（基于11个可完整采集指标）")
    print("=" * 80)
    
    # 1. 加载数据
    print("\n[1/5] 加载22个平台数据...")
    data = load_data()
    print("  加载平台数:", len(data))
    for d in data:
        print("  %s: %s (%s)" % (d['code'], d['name'], d['region']))
    
    # 2. TOPSIS（仅11个二值指标）
    print("\n[2/5] 计算熵权TOPSIS（11个二值指标）...")
    topsis_df, weights = topsis_binary_only(data)
    topsis_df.attrs['weights'] = weights
    print("  指标权重:")
    for ind, w in zip(BINARY_INDICATORS, weights):
        print("    %s: %.4f" % (ind, w))
    print("  排名TOP5:")
    for _, row in topsis_df.sort_values('topsis_rank').head(5).iterrows():
        print("    #%2d %s: %.4f (功能分=%d/%d)" % (
            row['topsis_rank'], row['name'], row['topsis_score'],
            row[BINARY_INDICATORS].sum(), len(BINARY_INDICATORS)
        ))
    
    # 3. DEA-BCC
    print("\n[3/5] 计算DEA-BCC效率...")
    dea_df = dea_bcc(data, topsis_df)
    efficient_count = (dea_df['dea_efficiency'] >= 0.999).sum()
    print("  DEA有效平台数: %d/%d" % (efficient_count, len(dea_df)))
    print("  平均效率: %.4f" % dea_df['dea_efficiency'].mean())
    print("  效率TOP5:")
    for _, row in dea_df.sort_values('dea_efficiency', ascending=False).head(5).iterrows():
        print("    %s: %.4f (运营%d年, 功能%d分)" % (
            row['name'], row['dea_efficiency'], row['operating_years'], row['function_score']
        ))
    
    # 4. DEMATEL
    print("\n[4/5] DEMATEL影响因素分析...")
    dematel_results = dematel_analysis(data, topsis_df)
    print("  中心度排名:")
    for name, center in sorted(zip(dematel_results['dimension_names'], dematel_results['center']), 
                                key=lambda x: x[1], reverse=True):
        print("    %s: %.4f" % (name, center))
    print("  原因度（正值=原因因素，负值=结果因素）:")
    for name, cause in zip(dematel_results['dimension_names'], dematel_results['cause']):
        factor_type = "原因因素" if cause > 0 else "结果因素"
        print("    %s: %.4f (%s)" % (name, cause, factor_type))
    
    # 5. fsQCA
    print("\n[5/5] fsQCA组态分析...")
    fsqca_results = fsqca_analysis(data, topsis_df)
    print("  高绩效平台数: %d" % fsqca_results['high_perf_count'])
    print("  有效组态数（一致性≥0.8）: %d" % len(fsqca_results['configurations']))
    print("  高绩效组态:")
    for cfg in fsqca_results['configurations'][:5]:
        config_bits = '%d%d%d%d' % (cfg['C1_supply_bin'], cfg['C2_service_bin'], cfg['C3_quality_bin'], cfg['C4_usage_bin'])
        print("    组态 %s: 一致性=%.2f, 覆盖度=%.2f, 案例=%s" % (
            config_bits, cfg['consistency'], cfg['coverage'], cfg['provinces']
        ))
    
    # 6. 导出
    print("\n[6/6] 导出结果...")
    report = export_results(data, topsis_df, dea_df, dematel_results, fsqca_results)
    
    print("\n" + "=" * 80)
    print("四种方法计算完成!")
    print("=" * 80)

if __name__ == '__main__':
    main()
