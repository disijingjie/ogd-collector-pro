import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.patches import Polygon

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
# 4. 新增：五维度雷达图 (山东 vs 全国均值)
# ==========================================
def draw_radar_chart():
    print("正在绘制：新增 五维度雷达图...")
    fig = plt.figure(figsize=(10, 10), dpi=300)
    fig.patch.set_facecolor('white')
    
    # 数据
    categories = ['供给保障(E1)', '平台服务(E2)', '数据质量(E3)', '利用效果(E4)', '公平性(E5)']
    N = len(categories)
    
    # 假设数据 (基于论文v15中描述的山东优势)
    shandong = [0.95, 0.82, 1.00, 0.98, 0.95]
    national_avg = [0.65, 0.55, 0.84, 0.42, 0.60]
    
    # 角度
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    shandong += shandong[:1]
    national_avg += national_avg[:1]
    
    # 极坐标图
    ax = plt.subplot(111, polar=True)
    ax.set_facecolor('white')
    
    # 设置雷达图的起始角度和方向
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # 绘制轴线和网格
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=16, fontweight='bold', color=COLORS['text_main'])
    
    # 调整标签位置，避免与图表重叠
    for label, angle in zip(ax.get_xticklabels(), angles[:-1]):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')
            
    # 设置Y轴网格
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], color=COLORS['text_sub'], fontsize=10)
    ax.set_ylim(0, 1.1)
    
    # 绘制全国均值 (虚线，无填充)
    ax.plot(angles, national_avg, linewidth=2, linestyle='--', color=COLORS['text_sub'], label='全国均值')
    
    # 绘制山东 (实线，带填充)
    ax.plot(angles, shandong, linewidth=2.5, linestyle='-', color=COLORS['success'], label='山东省 (标杆)')
    ax.fill(angles, shandong, color=COLORS['success'], alpha=0.15)
    
    # 添加图例
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1), fontsize=14, frameon=False)
    
    plt.title('山东省与全国均值 4E 五维度得分对比', fontsize=22, fontweight='bold', pad=40, color=COLORS['text_main'])
    plt.tight_layout()
    plt.savefig(f'{output_dir}/新增_五维度雷达图.png', bbox_inches='tight', dpi=300)
    plt.close()

if __name__ == '__main__':
    draw_radar_chart()
    print("雷达图生成完毕！")
