import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 统一配色方案
COLORS = {
    'primary': '#1f77b4',     # 学术蓝
    'secondary': '#ff7f0e',   # 活力橙
    'accent': '#2ca02c',      # 增长绿
    'danger': '#d62728',      # 警示红
    'neutral': '#7f7f7f',     # 中性灰
    'bg_light': '#f8f9fa',    # 浅灰背景
    'text_main': '#333333',   # 主文本
    'text_sub': '#666666'     # 次文本
}

def draw_data_illusion_funnel():
    """图1-X：数据口径幻觉漏斗图"""
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    # 漏斗层级数据
    levels = [
        {"name": "宣传数据量\n(政策/新闻宣称)", "width": 80, "y": 80, "h": 15, "color": "#c6dbef", "val": "100%"},
        {"name": "目录挂载量\n(平台显示总量)", "width": 60, "y": 60, "h": 15, "color": "#6baed6", "val": "65%"},
        {"name": "有效数据集\n(可下载/可访问)", "width": 40, "y": 40, "h": 15, "color": "#2171b5", "val": "32%"},
        {"name": "高价值利用\n(API调用/实际应用)", "width": 20, "y": 20, "h": 15, "color": "#08306b", "val": "8%"}
    ]
    
    # 绘制漏斗
    for i, lvl in enumerate(levels):
        # 梯形顶点
        if i < len(levels) - 1:
            next_w = levels[i+1]["width"]
        else:
            next_w = lvl["width"] * 0.5
            
        x_left_top = 50 - lvl["width"]/2
        x_right_top = 50 + lvl["width"]/2
        x_left_bot = 50 - next_w/2
        x_right_bot = 50 + next_w/2
        
        y_top = lvl["y"] + lvl["h"]
        y_bot = lvl["y"]
        
        poly = patches.Polygon(
            [(x_left_bot, y_bot), (x_left_top, y_top), (x_right_top, y_top), (x_right_bot, y_bot)],
            closed=True, facecolor=lvl["color"], edgecolor='white', linewidth=2, alpha=0.9
        )
        ax.add_patch(poly)
        
        # 添加文字
        text_color = 'black' if i < 2 else 'white'
        ax.text(50, lvl["y"] + lvl["h"]/2, lvl["name"], 
                ha='center', va='center', fontsize=12, fontweight='bold', color=text_color)
        
        # 添加百分比标注 (在右侧)
        ax.text(x_right_top + 5, lvl["y"] + lvl["h"]/2, f"留存率: {lvl['val']}", 
                ha='left', va='center', fontsize=12, fontweight='bold', color=COLORS['text_main'])
        
        # 添加"数据流失"标注 (在左侧)
        if i < len(levels) - 1:
            loss = int(levels[i]["val"].strip('%')) - int(levels[i+1]["val"].strip('%'))
            ax.text(x_left_top - 5, lvl["y"] + lvl["h"]/2 - 10, f"流失: -{loss}%", 
                    ha='right', va='center', fontsize=11, color=COLORS['danger'], fontstyle='italic')

    # 添加标题
    plt.title("省级政府数据开放平台的“数据口径幻觉”漏斗模型", fontsize=16, fontweight='bold', pad=20)
    
    # 保存
    plt.tight_layout()
    plt.savefig('static/thesis_charts_expert/新增_数据口径幻觉漏斗图.png', dpi=300, bbox_inches='tight')
    print("生成: 新增_数据口径幻觉漏斗图.png")

if __name__ == '__main__':
    draw_data_illusion_funnel()
