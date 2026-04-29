"""
DEMATEL 影响因素分析脚本
基于专家问卷的12因素因果关系挖掘
"""

import numpy as np
import pandas as pd

# 1. 读取直接影响矩阵 (12因素 × 12因素)
df = pd.read_csv('dematel_matrix.csv', index_col=0)
# 排除元数据列
factors = ['政策法规', '组织保障', '平台建设', '数据质量', '应用效果', 
           '用户参与', '资金投入', '技术标准', '人才队伍', '监督评估', '开放生态']
X = df.loc[factors, factors].values

print("=" * 60)
print("DEMATEL 影响因素分析")
print("=" * 60)
print(f"直接影响矩阵维度: {X.shape[0]}个因素 × {X.shape[1]}个因素")

# 2. 标准化直接影响矩阵
# Z = X / max(行和, 列和)
max_sum = max(X.sum(axis=1).max(), X.sum(axis=0).max())
Z = X / max_sum
print(f"\n[步骤1] 标准化完成 (max_sum = {max_sum:.4f})")

# 3. 计算综合影响矩阵
# T = Z(I - Z)^(-1)
n = Z.shape[0]
I = np.eye(n)
T = Z @ np.linalg.inv(I - Z)
print("\n[步骤2] 综合影响矩阵 T = Z(I-Z)^(-1) 计算完成")

# 4. 计算中心度和原因度
R = T.sum(axis=1)  # 行和 = 影响度 (对其他因素的影响)
D = T.sum(axis=0)  # 列和 = 被影响度 (受其他因素的影响)

prominence = R + D  # 中心度 = 重要性
causality = R - D   # 原因度 >0为原因因素，<0为结果因素

print("\n[步骤3] 中心度和原因度计算完成")

# 5. 设定阈值并构建网络
threshold = 0.05
network = T > threshold

# 6. 结果汇总
results = pd.DataFrame({
    '因素': factors,
    '影响度(R)': np.round(R, 4),
    '被影响度(D)': np.round(D, 4),
    '中心度(R+D)': np.round(prominence, 4),
    '原因度(R-D)': np.round(causality, 4),
    '类型': ['原因因素' if c > 0 else '结果因素' for c in causality]
})
results = results.sort_values('中心度(R+D)', ascending=False)

print("\n" + "=" * 60)
print("DEMATEL分析结果")
print("=" * 60)
print(results.to_string(index=False))

# 保存结果
results.to_csv('dematel_results.csv', index=False, encoding='utf-8-sig')
print("\n[完成] 结果已保存至 dematel_results.csv")

# 打印关键发现
print("\n" + "=" * 60)
print("关键发现")
print("=" * 60)
cause_factors = results[results['类型'] == '原因因素']['因素'].tolist()
result_factors = results[results['类型'] == '结果因素']['因素'].tolist()
print(f"原因因素(主动影响): {', '.join(cause_factors)}")
print(f"结果因素(被动影响): {', '.join(result_factors)}")
