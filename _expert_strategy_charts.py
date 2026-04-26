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
# 7. 图7-2：差异化优化策略矩阵 (SWOT重绘)
# ==========================================
def draw_swot_matrix():
    print("正在绘制：图7-2 差异化优化策略矩阵...")
    fig, ax = plt.subplots(figsize=(16, 12), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.axis('off')
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    # 绘制坐标轴
    ax.annotate('', xy=(100, 50), xytext=(0, 50), arrowprops=dict(arrowstyle="->", color=COLORS['text_main'], lw=2))
    ax.annotate('', xy=(50, 100), xytext=(50, 0), arrowprops=dict(arrowstyle="->", color=COLORS['text_main'], lw=2))
    
    ax.text(98, 47, '效率 (DEA)', fontsize=18, fontweight='bold', color=COLORS['text_main'], ha='right')
    ax.text(52, 98, '绩效 (TOPSIS)', fontsize=18, fontweight='bold', color=COLORS['text_main'], ha='left')
    
    def draw_quadrant(x, y, w, h, title, strategy, points, color, bg_color):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", 
                                      facecolor=bg_color, edgecolor=color, linewidth=2, alpha=0.8)
        ax.add_patch(rect)
        
        # 标题
        ax.text(x + w/2, y + h - 3, title, ha='center', va='top', fontsize=22, fontweight='bold', color=color)
        ax.text(x + w/2, y + h - 8, strategy, ha='center', va='top', fontsize=18, fontweight='bold', color=color)
        
        # 分割线
        ax.plot([x+2, x+w-2], [y+h-11, y+h-11], color=color, linestyle='-', linewidth=1, alpha=0.5)
        
        # 策略点
        for i, point in enumerate(points):
            ax.text(x + 5, y + h - 16 - i*5, f"● {point}", ha='left', va='top', fontsize=16, color=COLORS['text_main'], linespacing=1.5)

    # 第一象限：标杆型 (高绩效，高效率)
    points_1 = ["推进数据要素价值化", "授权运营创新试点", "输出标杆经验", "参与国际标准制定"]
    draw_quadrant(55, 55, 40, 40, "标杆型平台", "SO策略：发挥优势 · 抓住机遇", points_1, COLORS['success'], '#e8f8f5')
    ax.text(75, 58, "代表：山东、广东、浙江", ha='center', fontsize=14, style='italic', color=COLORS['success'])

    # 第二象限：潜力型 (高绩效，低效率)
    points_2 = ["优化资源配置效率", "补齐数据质量短板", "培育应用生态", "加强制度保障"]
    draw_quadrant(5, 55, 40, 40, "潜力型平台", "WO策略：克服劣势 · 抓住机遇", points_2, COLORS['warning'], '#fef5e7')
    ax.text(25, 58, "代表：四川、辽宁、北京", ha='center', fontsize=14, style='italic', color=COLORS['warning'])

    # 第三象限：困境型 (低绩效，低效率)
    points_3 = ["外部支援与对口帮扶", "建立基本数据开放能力", "省级专项政策支持", "借鉴先行省份经验"]
    draw_quadrant(5, 5, 40, 40, "困境型平台", "WT策略：克服劣势 · 规避威胁", points_3, COLORS['danger'], '#fdedec')
    ax.text(25, 8, "代表：黑龙江、山西等12省", ha='center', fontsize=14, style='italic', color=COLORS['danger'])

    # 第四象限：节约型 (低绩效，高效率)
    points_4 = ["适度增加资源投入", "扩大数据集规模", "提升平台功能", "保持效率优势"]
    draw_quadrant(55, 5, 40, 40, "节约型平台", "ST策略：发挥优势 · 规避威胁", points_4, COLORS['primary'], '#ebf5fb')
    ax.text(75, 8, "代表：天津、山西", ha='center', fontsize=14, style='italic', color=COLORS['primary'])

    plt.title('图7-2 差异化优化策略矩阵', fontsize=28, fontweight='bold', pad=30, color=COLORS['text_main'])
    plt.tight_layout()
    plt.savefig(f'{output_dir}/图7-2.png', bbox_inches='tight', dpi=300)
    plt.close()

# ==========================================
# 8. 图7-3：差异化策略实施路线图 (甘特图重绘)
# ==========================================
def draw_roadmap():
    print("正在绘制：图7-3 差异化策略实施路线图...")
    fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.axis('off')
    
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    # 绘制时间轴
    ax.annotate('', xy=(95, 85), xytext=(5, 85), arrowprops=dict(facecolor=COLORS['text_sub'], edgecolor='none', width=8, headwidth=20))
    
    # 时间节点
    ax.text(20, 88, "短期 (1年)\n基础建设与规范化", ha='center', fontsize=18, fontweight='bold', color=COLORS['text_main'])
    ax.text(50, 88, "中期 (3年)\n生态培育与价值释放", ha='center', fontsize=18, fontweight='bold', color=COLORS['text_main'])
    ax.text(80, 88, "长期 (5年)\n模式创新与引领发展", ha='center', fontsize=18, fontweight='bold', color=COLORS['text_main'])
    
    ax.plot([20, 20], [10, 85], color=COLORS['grid'], linestyle='--', linewidth=2)
    ax.plot([50, 50], [10, 85], color=COLORS['grid'], linestyle='--', linewidth=2)
    ax.plot([80, 80], [10, 85], color=COLORS['grid'], linestyle='--', linewidth=2)

    def draw_task_bar(x, y, w, h, text, color):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", 
                                      facecolor=color, edgecolor='white', linewidth=1, alpha=0.9)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=14, color='white', fontweight='bold')

    # 标杆型路径
    ax.text(5, 75, "标杆型", fontsize=18, fontweight='bold', color=COLORS['success'], va='center')
    draw_task_bar(25, 72, 20, 6, "高价值数据集开放", COLORS['success'])
    draw_task_bar(48, 72, 25, 6, "授权运营生态构建", COLORS['success'])
    draw_task_bar(75, 72, 18, 6, "国际标准输出", COLORS['success'])
    
    # 潜力型路径
    ax.text(5, 55, "潜力型", fontsize=18, fontweight='bold', color=COLORS['warning'], va='center')
    draw_task_bar(10, 52, 25, 6, "数据质量专项治理", COLORS['warning'])
    draw_task_bar(38, 52, 25, 6, "应用场景孵化", COLORS['warning'])
    draw_task_bar(65, 52, 25, 6, "数据要素市场化", COLORS['warning'])
    
    # 节约型路径
    ax.text(5, 35, "节约型", fontsize=18, fontweight='bold', color=COLORS['primary'], va='center')
    draw_task_bar(15, 32, 25, 6, "平台功能升级", COLORS['primary'])
    draw_task_bar(42, 32, 25, 6, "跨部门数据整合", COLORS['primary'])
    draw_task_bar(69, 32, 20, 6, "特色主题应用", COLORS['primary'])
    
    # 困境型路径
    ax.text(5, 15, "困境型", fontsize=18, fontweight='bold', color=COLORS['danger'], va='center')
    draw_task_bar(10, 12, 30, 6, "管理办法出台与平台重建", COLORS['danger'])
    draw_task_bar(42, 12, 25, 6, "基础数据集覆盖", COLORS['danger'])
    draw_task_bar(69, 12, 20, 6, "初步形成利用生态", COLORS['danger'])

    plt.title('图7-3 差异化策略实施路线图', fontsize=26, fontweight='bold', pad=30, color=COLORS['text_main'])
    plt.tight_layout()
    plt.savefig(f'{output_dir}/图7-3.png', bbox_inches='tight', dpi=300)
    plt.close()

if __name__ == '__main__':
    draw_swot_matrix()
    draw_roadmap()
    print("策略图表生成完毕！")
