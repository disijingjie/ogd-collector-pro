import os
import shutil

expert_dir = "static/thesis_charts_expert"
v6_dir = "static/thesis_charts_v6"

# 将新增的图表也复制过去，并按论文编号命名
new_charts = {
    "新增_TOPSIS排名图.png": "图5-5.png", # 假设放在第五章最后
    "新增_五维度雷达图.png": "图5-6.png",
}

for expert_name, v6_name in new_charts.items():
    src = os.path.join(expert_dir, expert_name)
    dst = os.path.join(v6_dir, v6_name)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"OK: {v6_name}")
    else:
        print(f"FAIL: {src}")
