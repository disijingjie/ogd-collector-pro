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
# 6. 图4-1：研究技术路线图 (泳道图重绘)
# ==========================================
def draw_tech_route():
    print("正在绘制：图4-1 研究技术路线...")
    fig, ax = plt.subplots(figsize=(14, 20), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.axis('off')
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    def draw_box(x, y, w, h, text, facecolor, edgecolor, textcolor='white', fontsize=16, fontweight='bold', style="round,pad=0.3"):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle=style, 
                                      facecolor=facecolor, edgecolor=edgecolor, linewidth=2, alpha=0.95)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', 
                color=textcolor, fontsize=fontsize, fontweight=fontweight, linespacing=1.5)
        return x + w/2, y, x + w/2, y + h

    def draw_arrow(x1, y1, x2, y2, color=COLORS['text_sub']):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor=color, edgecolor=color, width=3, headwidth=12, headlength=12, shrink=0.05))
                    
    # --- 左侧大阶段框 (泳道1) ---
    stages = [
        ("第一阶段\n理论构建", 85),
        ("第二阶段\n框架设计", 70),
        ("第三阶段\n数据采集", 55),
        ("第四阶段\n绩效评估", 40),
        ("第五阶段\n机制分析", 25),
        ("第六阶段\n对策设计", 10)
    ]
    
    for text, y in stages:
        draw_box(5, y, 15, 8, text, COLORS['primary'], COLORS['primary'], fontsize=18)
        
    # 左侧主线箭头
    for i in range(len(stages)-1):
        draw_arrow(12.5, stages[i][1], 12.5, stages[i+1][1]+8, color=COLORS['primary'])

    # --- 右侧具体步骤框 (泳道2) ---
    
    # 阶段1: 理论构建
    draw_box(25, 85, 20, 8, "公共价值理论\n(战略/授权/运作)", COLORS['bg_light'], COLORS['primary'], COLORS['text_main'], 16, 'normal')
    draw_box(50, 85, 20, 8, "文献综述\n(现状与不足)", COLORS['bg_light'], COLORS['primary'], COLORS['text_main'], 16, 'normal')
    draw_box(75, 85, 20, 8, "提出研究问题\n(评估/机制/对策)", COLORS['bg_light'], COLORS['primary'], COLORS['text_main'], 16, 'normal')
    draw_arrow(45, 89, 50, 89)
    draw_arrow(70, 89, 75, 89)
    draw_arrow(60, 85, 60, 78) # 向下

    # 阶段2: 框架设计
    draw_box(25, 70, 20, 8, "4E评估框架\n(5个一级维度)", COLORS['bg_light'], COLORS['success'], COLORS['text_main'], 16, 'normal')
    draw_box(50, 70, 20, 8, "指标体系构建\n(24个具体指标)", COLORS['bg_light'], COLORS['success'], COLORS['text_main'], 16, 'normal')
    draw_box(75, 70, 20, 8, "组合赋权模型\n(AHP-熵权法)", COLORS['bg_light'], COLORS['success'], COLORS['text_main'], 16, 'normal')
    draw_arrow(45, 74, 50, 74)
    draw_arrow(70, 74, 75, 74)
    draw_arrow(60, 70, 60, 63) # 向下

    # 阶段3: 数据采集
    draw_box(25, 55, 20, 8, "自动化数据采集\n(Python爬虫)", COLORS['bg_light'], COLORS['warning'], COLORS['text_main'], 16, 'normal')
    draw_box(50, 55, 20, 8, "人工辅助核验\n(交叉验证)", COLORS['bg_light'], COLORS['warning'], COLORS['text_main'], 16, 'normal')
    draw_box(75, 55, 20, 8, "数据清洗与标准化\n(23个有效样本)", COLORS['bg_light'], COLORS['warning'], COLORS['text_main'], 16, 'normal')
    draw_arrow(45, 59, 50, 59)
    draw_arrow(70, 59, 75, 59)
    draw_arrow(60, 55, 60, 48) # 向下
    
    # 阶段4: 绩效评估
    draw_box(25, 40, 20, 8, "TOPSIS综合绩效\n(测度综合得分)", COLORS['bg_light'], COLORS['danger'], COLORS['text_main'], 16, 'normal')
    draw_box(50, 40, 20, 8, "DEA-BCC效率评估\n(测度资源配置效率)", COLORS['bg_light'], COLORS['danger'], COLORS['text_main'], 16, 'normal')
    draw_box(75, 40, 20, 8, "四象限类型学划分\n(标杆/潜力/节约/困境)", COLORS['bg_light'], COLORS['danger'], COLORS['text_main'], 16, 'normal')
    draw_arrow(45, 44, 50, 44)
    draw_arrow(70, 44, 75, 44)
    draw_arrow(60, 40, 60, 33) # 向下

    # 阶段5: 机制分析
    draw_box(25, 25, 20, 8, "影响因素识别\n(TOE框架6因素)", COLORS['bg_light'], '#8e44ad', COLORS['text_main'], 16, 'normal')
    draw_box(50, 25, 20, 8, "DEMATEL因果分析\n(识别核心因素)", COLORS['bg_light'], '#8e44ad', COLORS['text_main'], 16, 'normal')
    draw_box(75, 25, 20, 8, "fsQCA组态分析\n(揭示高绩效路径)", COLORS['bg_light'], '#8e44ad', COLORS['text_main'], 16, 'normal')
    draw_arrow(45, 29, 50, 29)
    draw_arrow(70, 29, 75, 29)
    draw_arrow(60, 25, 60, 18) # 向下

    # 阶段6: 对策设计
    draw_box(25, 10, 20, 8, "成熟度模型构建\n(五阶段演进)", COLORS['bg_light'], COLORS['primary'], COLORS['text_main'], 16, 'normal')
    draw_box(50, 10, 20, 8, "差异化优化策略\n(SWOT矩阵)", COLORS['bg_light'], COLORS['primary'], COLORS['text_main'], 16, 'normal')
    draw_box(75, 10, 20, 8, "实施路线图设计\n(短/中/长期)", COLORS['bg_light'], COLORS['primary'], COLORS['text_main'], 16, 'normal')
    draw_arrow(45, 14, 50, 14)
    draw_arrow(70, 14, 75, 14)

    # 阶段与步骤之间的连接虚线
    for y in [85, 70, 55, 40, 25, 10]:
        ax.plot([20, 25], [y+4, y+4], color=COLORS['text_sub'], linestyle='--', linewidth=1.5)

    plt.title('图4-1 研究技术路线', fontsize=26, fontweight='bold', pad=30, color=COLORS['text_main'])
    plt.tight_layout()
    plt.savefig(f'{output_dir}/图4-1.png', bbox_inches='tight', dpi=300)
    plt.close()

if __name__ == '__main__':
    draw_tech_route()
    print("图4-1 生成完毕！")
