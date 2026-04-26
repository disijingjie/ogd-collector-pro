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

def draw_evaluation_framework_comparison():
    """图2-X：4E vs 开放数林 vs ODB评估维度对比矩阵"""
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.axis('off')
    
    # 定义矩阵数据
    frameworks = ["复旦大学「开放数林」\n(准备度/平台/数据/利用)", 
                  "万维网基金会「ODB」\n(准备度/实施/影响)", 
                  "本研究「4E框架」\n(供给/平台/质量/利用/动态)"]
    
    dimensions = ["政策与制度环境", "平台建设与功能", "数据数量与质量", "数据利用与生态", "动态演进与反馈"]
    
    # 权重热力值 (模拟)
    # 0: 无/极少, 1: 较少, 2: 中等, 3: 较多, 4: 核心焦点
    weights = np.array([
        [3, 2, 4],  # 政策环境
        [3, 1, 3],  # 平台功能
        [4, 3, 3],  # 数据质量
        [2, 4, 4],  # 利用生态
        [0, 0, 3]   # 动态演进
    ])
    
    # 绘制热力图矩阵
    cax = ax.imshow(weights, cmap='Blues', aspect='auto', alpha=0.8)
    
    # 添加网格线
    ax.set_xticks(np.arange(len(frameworks)) - 0.5, minor=True)
    ax.set_yticks(np.arange(len(dimensions)) - 0.5, minor=True)
    ax.grid(which="minor", color="white", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)
    
    # 移除主刻度线
    ax.tick_params(top=False, bottom=False, left=False, right=False, labelleft=True, labelbottom=True)
    
    # 设置刻度标签
    ax.set_xticks(np.arange(len(frameworks)))
    ax.set_xticklabels(frameworks, fontsize=12, fontweight='bold')
    ax.set_yticks(np.arange(len(dimensions)))
    ax.set_yticklabels(dimensions, fontsize=12, fontweight='bold')
    
    # 开启坐标轴显示
    ax.axis('on')
    
    # 隐藏边框
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # 在单元格中添加文本说明
    text_data = [
        ["准备度(30%)", "Readiness(35%)", "供给保障(E1)"],
        ["平台层(20%)", "Implementation(涵盖)", "平台支撑(E2)"],
        ["数据层(30%)", "Implementation(涵盖)", "数据质量(E3)"],
        ["利用层(20%)", "Impact(30%)", "利用效果(E4)"],
        ["无专门维度", "无专门维度", "动态演进(E5)"]
    ]
    
    for i in range(len(dimensions)):
        for j in range(len(frameworks)):
            val = weights[i, j]
            text_color = 'white' if val > 2 else 'black'
            font_weight = 'bold' if val == 4 else 'normal'
            
            ax.text(j, i, text_data[i][j], ha="center", va="center", color=text_color, 
                    fontsize=11, fontweight=font_weight)
            
            # 添加高亮标记 (针对4E框架的优势)
            if j == 2 and val >= 3:
                rect = patches.Rectangle((j-0.45, i-0.45), 0.9, 0.9, fill=False, 
                                         edgecolor=COLORS['secondary'], linewidth=3, zorder=5)
                ax.add_patch(rect)

    # 添加标题
    plt.title("4E框架与主流政府数据开放评估体系的维度对比矩阵", fontsize=16, fontweight='bold', pad=20)
    
    # 添加图例说明
    plt.figtext(0.5, 0.01, "注：颜色深浅代表该维度在评估体系中的权重和关注程度；橙色边框突出本研究4E框架的核心特色与优势。", 
                ha="center", fontsize=11, color=COLORS['text_sub'])
    
    plt.tight_layout()
    plt.savefig('static/thesis_charts_expert/新增_评估框架对比矩阵.png', dpi=300, bbox_inches='tight')
    print("生成: 新增_评估框架对比矩阵.png")

if __name__ == '__main__':
    draw_evaluation_framework_comparison()
