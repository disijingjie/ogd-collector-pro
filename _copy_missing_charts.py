import os
import shutil

expert_dir = "static/thesis_charts_expert"
v6_dir = "static/thesis_charts_v6"

new_charts = {
    "新增_数据口径幻觉漏斗图.png": "图1-4.png",
    "新增_文献趋势图.png": "图2-1.png",
    "新增_公共价值三角映射图.png": "图2-2.png",
    "新增_评估框架对比矩阵.png": "图2-3.png",
    "新增_混合方法嵌套逻辑图.png": "图4-3.png",
    "新增_DEMATEL热力图.png": "图6-6.png",
    "新增_核心发现框架图.png": "图8-1.png"
}

for expert_name, v6_name in new_charts.items():
    src = os.path.join(expert_dir, expert_name)
    dst = os.path.join(v6_dir, v6_name)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"OK: {v6_name}")
    else:
        print(f"FAIL: {expert_name} not found")
