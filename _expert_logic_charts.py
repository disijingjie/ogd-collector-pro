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
    'purple': '#6c3483',    # 紫色
    'bg_light': '#f8f9f9',
    'text_main': '#2c3e50',
    'text_sub': '#5d6d7e',
    'grid': '#e5e7e9'
}

output_dir = "static/thesis_charts_expert"

# ==========================================
# 5. 图3-1：4E评估指标体系结构 (突破matplotlib排版限制)
# ==========================================
def draw_4e_framework():
    print("正在绘制：图3-1 4E评估指标体系结构...")
    # 使用超大画布
    fig, ax = plt.subplots(figsize=(24, 16), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.axis('off')
    
    # 坐标系范围：X(0-100), Y(0-100)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    # 绘制辅助函数
    def draw_box(x, y, w, h, text, color, text_color='white', fontsize=16, font_weight='bold'):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=0.5", 
                                      facecolor=color, edgecolor=COLORS['text_main'], linewidth=1.5, alpha=0.9)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', 
                color=text_color, fontsize=fontsize, fontweight=font_weight, linespacing=1.5)
        return x, y, w, h

    def draw_line(x1, y1, x2, y2, color=COLORS['text_main']):
        # 绘制直角折线
        mid_x = (x1 + x2) / 2
        ax.plot([x1, mid_x, mid_x, x2], [y1, y1, y2, y2], color=color, linewidth=2, zorder=0)
        
    # --- 第一层：总目标 ---
    draw_box(4, 45, 8, 10, "省级政府数据\n开放平台\n综合绩效评估", COLORS['primary'], fontsize=20)
    
    # --- 第二层：5个一级维度 (Y坐标：85, 65, 45, 25, 5) ---
    dim_y = [85, 65, 45, 25, 5]
    dim_colors = [COLORS['primary'], COLORS['success'], COLORS['warning'], COLORS['danger'], COLORS['purple']]
    dim_names = ["供给保障 (E1)", "平台服务 (E2)", "数据质量 (E3)", "利用效果 (E4)", "公平性 (E5)"]
    
    for i in range(5):
        draw_line(12, 50, 20, dim_y[i] + 4)
        draw_box(20, dim_y[i], 12, 8, dim_names[i], dim_colors[i], fontsize=18)
        
    # --- 第三层：9个二级维度 & 第四层：24个三级指标 ---
    
    # E1: 供给保障 (Y: 85)
    draw_line(32, 89, 40, 93)
    draw_box(40, 91, 12, 6, "数据规模 (E11)", COLORS['bg_light'], COLORS['text_main'], fontsize=16)
    draw_line(52, 94, 60, 97)
    draw_box(60, 95, 25, 4, "数据集总数 (E111)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')
    draw_line(52, 94, 60, 91)
    draw_box(60, 89, 25, 4, "数据容量大小 (E112)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')

    draw_line(32, 89, 40, 83)
    draw_box(40, 80, 12, 6, "覆盖广度 (E12)", COLORS['bg_light'], COLORS['text_main'], fontsize=16)
    draw_line(52, 83, 60, 85)
    draw_box(60, 83, 25, 4, "主题覆盖率 (E121)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')
    draw_line(52, 83, 60, 79)
    draw_box(60, 77, 25, 4, "部门覆盖率 (E122)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')

    # E2: 平台服务 (Y: 65)
    draw_line(32, 69, 40, 73)
    draw_box(40, 70, 12, 6, "获取便捷度 (E21)", COLORS['bg_light'], COLORS['text_main'], fontsize=16)
    draw_line(52, 73, 60, 75)
    draw_box(60, 73, 25, 4, "检索功能完备性 (E211)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')
    draw_line(52, 73, 60, 69)
    draw_box(60, 67, 25, 4, "数据预览功能 (E212)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')

    draw_line(32, 69, 40, 63)
    draw_box(40, 60, 12, 6, "技术支持度 (E22)", COLORS['bg_light'], COLORS['text_main'], fontsize=16)
    draw_line(52, 63, 60, 65)
    draw_box(60, 63, 25, 4, "API接口开放度 (E221)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')
    draw_line(52, 63, 60, 59)
    draw_box(60, 57, 25, 4, "开发者文档完备性 (E222)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')

    # E3: 数据质量 (Y: 45)
    draw_line(32, 49, 40, 53)
    draw_box(40, 50, 12, 6, "内在质量 (E31)", COLORS['bg_light'], COLORS['text_main'], fontsize=16)
    draw_line(52, 53, 60, 55)
    draw_box(60, 53, 25, 4, "数据准确率 (E311)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')
    draw_line(52, 53, 60, 49)
    draw_box(60, 47, 25, 4, "数据完整率 (E312)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')

    draw_line(32, 49, 40, 43)
    draw_box(40, 40, 12, 6, "外在质量 (E32)", COLORS['bg_light'], COLORS['text_main'], fontsize=16)
    draw_line(52, 43, 60, 45)
    draw_box(60, 43, 25, 4, "更新及时率 (E321)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')
    draw_line(52, 43, 60, 39)
    draw_box(60, 37, 25, 4, "机器可读格式占比 (E322)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')

    # E4: 利用效果 (Y: 25)
    draw_line(32, 29, 40, 33)
    draw_box(40, 30, 12, 6, "应用活跃度 (E41)", COLORS['bg_light'], COLORS['text_main'], fontsize=16)
    draw_line(52, 33, 60, 35)
    draw_box(60, 33, 25, 4, "数据集下载总量 (E411)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')
    draw_line(52, 33, 60, 29)
    draw_box(60, 27, 25, 4, "API调用总次数 (E412)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')

    draw_line(32, 29, 40, 23)
    draw_box(40, 20, 12, 6, "创新产出度 (E42)", COLORS['bg_light'], COLORS['text_main'], fontsize=16)
    draw_line(52, 23, 60, 25)
    draw_box(60, 23, 25, 4, "优秀应用案例数 (E421)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')
    draw_line(52, 23, 60, 19)
    draw_box(60, 17, 25, 4, "授权运营项目数 (E422)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')

    # E5: 公平性 (Y: 5)
    draw_line(32, 9, 40, 9)
    draw_box(40, 6, 12, 6, "包容与安全 (E51)", COLORS['bg_light'], COLORS['text_main'], fontsize=16)
    draw_line(52, 9, 60, 13)
    draw_box(60, 11, 25, 4, "无障碍访问支持度 (E511)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')
    draw_line(52, 9, 60, 7)
    draw_box(60, 5, 25, 4, "数据脱敏合规率 (E512)", 'white', COLORS['text_main'], fontsize=14, font_weight='normal')

    plt.title('图3-1 4E评估指标体系结构', fontsize=30, fontweight='bold', pad=40, color=COLORS['text_main'])
    plt.tight_layout()
    plt.savefig(f'{output_dir}/图3-1.png', bbox_inches='tight', dpi=300)
    plt.close()

if __name__ == '__main__':
    draw_4e_framework()
    print("图3-1 生成完毕！")
