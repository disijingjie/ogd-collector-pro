import pandas as pd

df = pd.read_csv('data/verified_dataset/table_topsis_4e_final.csv')
# 取前23个为有效样本
df23 = df.head(23).copy()
print('23个有效样本平台:')
for i, row in df23.iterrows():
    print(f"{i+1}. {row['province']} (score:{row['topsis_score']:.3f}, rank:{row['topsis_rank']})")

print('\n被排除的8个平台:')
df8 = df.tail(8).copy()
for i, row in df8.iterrows():
    print(f"{i+24}. {row['province']} (score:{row['topsis_score']:.3f})")
