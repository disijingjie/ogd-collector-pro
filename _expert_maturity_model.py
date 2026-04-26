import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

COLORS = {
    'primary': '#1a5276',   # 学术蓝
    'success': '#1e8449',   # 深绿
    'warning': '#d35400',   # 橙色
    'danger': '#922b21',    # 深红
    'bg_light': '#f8f9f9',
    'text_main': '#2c3e50',
    'text_sub': '#5d6d7e',
    'grid': '#e5e7e9'
}

output_dir = "static/thesis_charts_expert"

# ==========================================
# 9. 图7-1：政府数据开放平台成熟度模型 (阶梯图)
# ==========================================
def draw_maturity_model():
    print("正在绘制：图7-1 政府数据开放平台成熟度模型...")
    fig, ax = plt.subplots(figsize=(14, 10), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.axis('off')
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    stages = [
        ("第一阶段\n基础级", "数据目录展示\n文件下载\n单向发布", COLORS['danger']),
        ("第二阶段\n发展级", "结构化数据\n基础检索\n偶尔更新", COLORS['warning']),
        ("第三阶段\n规范级", "元数据标准\nAPI接口\n定期更新", COLORS['primary']),
        ("第四阶段\n优化级", "机器可读\n用户互动\n应用展示", '#8e44ad'),
        ("第五阶段\n引领级", "数据沙箱\n授权运营\n价值共创", COLORS['success'])
    ]
    
    # 绘制阶梯
    for i, (title, desc, color) in enumerate(stages):
        x = 10 + i * 16
        y = 10 + i * 14
        w = 16
        h = 14
        
        # 阶梯块
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", 
                                      facecolor=color, edgecolor='white', linewidth=2, alpha=0.85)
        ax.add_patch(rect)
        
        # 阶段标题
        ax.text(x + w/2, y + h - 3, title, ha='center', va='top', fontsize=18, fontweight='bold', color='white')
        
        # 阶段描述
        ax.text(x + w/2, y + h/2 - 2, desc, ha='center', va='center', fontsize=14, color='white', linespacing=1.6)
        
        # 向上箭头 (除了最后一个)
        if i < len(stages) - 1:
            ax.annotate('', xy=(x + w + 8, y + h + 7), xytext=(x + w/2 + 4, y + h + 2),
                        arrowprops=dict(facecolor=COLORS['text_sub'], edgecolor='none', width=3, headwidth=10))

    # 绘制坐标轴
    ax.annotate('', xy=(95, 5), xytext=(5, 5), arrowprops=dict(arrowstyle="->", color=COLORS['text_main'], lw=2))
    ax.annotate('', xy=(5, 90), xytext=(5, 5), arrowprops=dict(arrowstyle="->", color=COLORS['text_main'], lw=2))
    
    ax.text(95, 2, '时间演进 / 运营深度', fontsize=16, fontweight='bold', color=COLORS['text_main'], ha='right')
    ax.text(2, 92, '数据价值 / 开放水平', fontsize=16, fontweight='bold', color=COLORS['text_main'], ha='left')

    plt.title('图7-1 政府数据开放平台成熟度模型', fontsize=26, fontweight='bold', pad=30, color=COLORS['text_main'])
    plt.tight_layout()
    plt.savefig(f'{output_dir}/图7-1.png', bbox_inches='tight', dpi=300)
    plt.close()

if __name__ == '__main__':
    draw_maturity_model()
    print("图7-1 生成完毕！")
