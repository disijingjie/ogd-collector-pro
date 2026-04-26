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

def draw_public_value_triangle():
    """图2-X：公共价值三角框架映射图"""
    fig, ax = plt.subplots(figsize=(10, 9), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    # 三角形顶点坐标
    top = (50, 85)
    left = (20, 25)
    right = (80, 25)
    
    # 绘制主三角形
    triangle = patches.Polygon([top, left, right], closed=True, 
                               facecolor=COLORS['bg_light'], edgecolor=COLORS['primary'], 
                               linewidth=3, alpha=0.5)
    ax.add_patch(triangle)
    
    # 绘制顶点圆形
    circle_radius = 12
    
    # 顶部：战略目标 (Public Value)
    c_top = patches.Circle(top, circle_radius, facecolor=COLORS['primary'], edgecolor='white', linewidth=2, alpha=0.9, zorder=5)
    ax.add_patch(c_top)
    ax.text(top[0], top[1]+3, "战略目标\n(Public Value)", ha='center', va='center', color='white', fontsize=14, fontweight='bold', zorder=6)
    ax.text(top[0], top[1]-4, "映射: 4E利用效果", ha='center', va='center', color='yellow', fontsize=11, fontweight='bold', zorder=6)
    
    # 左下：授权环境 (Authorizing Environment)
    c_left = patches.Circle(left, circle_radius, facecolor=COLORS['secondary'], edgecolor='white', linewidth=2, alpha=0.9, zorder=5)
    ax.add_patch(c_left)
    ax.text(left[0], left[1]+3, "授权环境\n(Authorizing\nEnvironment)", ha='center', va='center', color='white', fontsize=12, fontweight='bold', zorder=6)
    ax.text(left[0], left[1]-5, "映射: 4E供给保障", ha='center', va='center', color='yellow', fontsize=11, fontweight='bold', zorder=6)
    
    # 右下：运作能力 (Operational Capacity)
    c_right = patches.Circle(right, circle_radius, facecolor=COLORS['accent'], edgecolor='white', linewidth=2, alpha=0.9, zorder=5)
    ax.add_patch(c_right)
    ax.text(right[0], right[1]+3, "运作能力\n(Operational\nCapacity)", ha='center', va='center', color='white', fontsize=12, fontweight='bold', zorder=6)
    ax.text(right[0], right[1]-5, "映射: 4E平台+质量", ha='center', va='center', color='yellow', fontsize=11, fontweight='bold', zorder=6)
    
    # 绘制连接线上的互动说明
    # 左侧边 (战略-授权)
    ax.text(30, 60, "合法性与支持\n(政策法规/领导力)", ha='center', va='center', fontsize=11, rotation=60, color=COLORS['text_main'],
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=COLORS['neutral'], alpha=0.8))
    
    # 右侧边 (战略-能力)
    ax.text(70, 60, "可行性与执行\n(技术/资金/人才)", ha='center', va='center', fontsize=11, rotation=-60, color=COLORS['text_main'],
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=COLORS['neutral'], alpha=0.8))
    
    # 底部边 (授权-能力)
    ax.text(50, 25, "资源配置与动员\n(跨部门协同/社会参与)", ha='center', va='center', fontsize=11, color=COLORS['text_main'],
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=COLORS['neutral'], alpha=0.8))
            
    # 中心文本
    ax.text(50, 45, "政府数据开放\n价值创造机制", ha='center', va='center', fontsize=16, fontweight='bold', color=COLORS['text_main'])

    # 添加标题
    plt.title("公共价值三角框架与4E评估维度的理论映射", fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('static/thesis_charts_expert/新增_公共价值三角映射图.png', dpi=300, bbox_inches='tight')
    print("生成: 新增_公共价值三角映射图.png")

if __name__ == '__main__':
    draw_public_value_triangle()
