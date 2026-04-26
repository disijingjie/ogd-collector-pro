import matplotlib.pyplot as plt
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

def draw_literature_trend():
    """图2-X：政府数据开放研究文献时间趋势图"""
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    # 模拟数据 (2010-2024)
    years = np.arange(2010, 2025)
    cnki_pubs = [12, 18, 25, 45, 80, 150, 280, 420, 560, 680, 850, 1050, 1280, 1450, 1600]
    wos_pubs = [5, 8, 15, 25, 40, 70, 120, 180, 250, 320, 450, 600, 800, 950, 1100]
    
    # 绘制折线
    ax.plot(years, cnki_pubs, marker='o', linewidth=3, markersize=8, 
            color=COLORS['primary'], label='CNKI (中文文献)')
    ax.plot(years, wos_pubs, marker='s', linewidth=3, markersize=8, 
            color=COLORS['secondary'], label='WoS (外文文献)')
    
    # 填充区域
    ax.fill_between(years, cnki_pubs, alpha=0.1, color=COLORS['primary'])
    ax.fill_between(years, wos_pubs, alpha=0.1, color=COLORS['secondary'])
    
    # 添加关键政策节点标注
    policy_nodes = {
        2015: "《促进大数据发展行动纲要》\n(国家战略确立)",
        2020: "《关于构建更加完善的要素市场化配置体制机制的意见》\n(数据要素化)",
        2022: "《数据二十条》\n(基础制度构建)"
    }
    
    for year, text in policy_nodes.items():
        idx = list(years).index(year)
        y_val = cnki_pubs[idx]
        
        # 绘制垂直虚线
        ax.axvline(x=year, ymin=0, ymax=y_val/1800, color=COLORS['danger'], linestyle='--', alpha=0.6)
        
        # 添加文本框
        ax.annotate(text, xy=(year, y_val), xytext=(year-1.5, y_val+200),
                    arrowprops=dict(facecolor=COLORS['danger'], shrink=0.05, width=1.5, headwidth=6),
                    fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=COLORS['danger'], alpha=0.9))
    
    # 设置图表样式
    ax.set_title("2010-2024年国内外政府数据开放研究发文量趋势", fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel("年份", fontsize=12)
    ax.set_ylabel("发文量 (篇)", fontsize=12)
    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45)
    ax.set_ylim(0, 1800)
    
    # 移除顶部和右侧边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # 添加网格
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    
    # 添加图例
    ax.legend(loc='upper left', fontsize=12, frameon=True)
    
    plt.tight_layout()
    plt.savefig('static/thesis_charts_expert/新增_文献趋势图.png', dpi=300, bbox_inches='tight')
    print("生成: 新增_文献趋势图.png")

if __name__ == '__main__':
    draw_literature_trend()
