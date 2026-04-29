"""
TOPSIS 绩效评估分析脚本
基于4E框架的23个省级政府数据开放平台综合评价
"""

import numpy as np
import pandas as pd

# 1. 读取决策矩阵 (23平台 × 5维度)
# 维度: 经济性、效率性、有效性、公平性、环境性
df = pd.read_csv('4e_scores.csv')
X = df[['经济性_得分', '效率性_得分', '有效性_得分', '公平性_得分', '环境性_得分']].values

print("=" * 60)
print("TOPSIS 绩效评估分析")
print("=" * 60)
print(f"决策矩阵维度: {X.shape[0]}个平台 × {X.shape[1]}个维度")

# 2. 向量标准化
X_norm = X / np.sqrt((X**2).sum(axis=0))
print("\n[步骤1] 向量标准化完成")

# 3. 熵权法计算权重
# 计算比重
p = X_norm / X_norm.sum(axis=0)
# 计算信息熵
E = -np.sum(p * np.log(p + 1e-10), axis=0) / np.log(len(X))
# 计算权重
w = (1 - E) / (1 - E).sum()
print(f"\n[步骤2] 熵权法权重:")
for i, dim in enumerate(['经济性', '效率性', '有效性', '公平性', '环境性']):
    print(f"  {dim}: {w[i]:.4f}")

# 4. 加权标准化矩阵
V = X_norm * w
print("\n[步骤3] 加权标准化矩阵构建完成")

# 5. 确定正负理想解
V_pos = V.max(axis=0)  # 正理想解
V_neg = V.min(axis=0)  # 负理想解
print(f"\n[步骤4] 正理想解: {V_pos}")
print(f"         负理想解: {V_neg}")

# 6. 计算距离
D_pos = np.sqrt(((V - V_pos)**2).sum(axis=1))
D_neg = np.sqrt(((V - V_neg)**2).sum(axis=1))
print("\n[步骤5] 欧氏距离计算完成")

# 7. 计算相对贴近度
C = D_neg / (D_pos + D_neg)
print("\n[步骤6] 相对贴近度计算完成")

# 8. 排序
results = pd.DataFrame({
    '平台': df['平台名称'],
    'TOPSIS得分': np.round(C, 4),
    '排名': pd.Series(C).rank(ascending=False).astype(int)
})
results = results.sort_values('排名')

print("\n" + "=" * 60)
print("评估结果排名")
print("=" * 60)
print(results.to_string(index=False))

# 保存结果
results.to_csv('topsis_results.csv', index=False, encoding='utf-8-sig')
print("\n[完成] 结果已保存至 topsis_results.csv")
