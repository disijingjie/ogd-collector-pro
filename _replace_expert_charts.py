import os
import shutil

print("开始整理并替换论文图表...")

expert_dir = "static/thesis_charts_expert"
v6_dir = "static/thesis_charts_v6"

# 需要替换的图表映射
replacements = {
    "图3-1.png": "图3-1.png",
    "图4-1.png": "图4-1.png",
    "图5-3.png": "图5-3.png",
    "图6-1.png": "图6-1.png",
    "图7-1.png": "图7-1.png",
    "图7-2.png": "图7-2.png",
    "图7-3.png": "图7-3.png",
}

# 复制专家级图表覆盖v6中的旧图
for expert_name, v6_name in replacements.items():
    src = os.path.join(expert_dir, expert_name)
    dst = os.path.join(v6_dir, v6_name)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"OK: {v6_name}")
    else:
        print(f"FAIL: {src}")

print("图表替换完成！")
