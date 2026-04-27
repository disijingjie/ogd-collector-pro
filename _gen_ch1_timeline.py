import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def draw_global_timeline():
    """图1-1：全球政府数据开放平台发展历程"""
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    # 三个阶段背景
    phases = [
        {"name": "第一阶段：门户时代", "years": "2009-2012", "x": 15, "w": 25, "color": "#e6f2ff"},
        {"name": "第二阶段：区域合作", "years": "2013-2017", "x": 40, "w": 25, "color": "#fff0e6"},
        {"name": "第三阶段：价值深化", "years": "2018-至今", "x": 65, "w": 25, "color": "#e6ffe6"}
    ]
    
    for p in phases:
        rect = patches.FancyBboxPatch((p["x"], 60), p["w"], 30, boxstyle="round,pad=1", 
                                      facecolor=p["color"], edgecolor='gray', linewidth=1)
        ax.add_patch(rect)
        ax.text(p["x"]+p["w"]/2, 80, p["name"], ha='center', va='center', fontsize=14, fontweight='bold')
        ax.text(p["x"]+p["w"]/2, 73, p["years"], ha='center', va='center', fontsize=12, color='gray')
    
    # 关键节点
    events = [
        {"year": 2009, "event": "美国Data.gov上线", "x": 8, "y": 50},
        {"year": 2010, "event": "英国data.gov.uk上线", "x": 12, "y": 42},
        {"year": 2013, "event": "G8开放数据宪章", "x": 38, "y": 50},
        {"year": 2015, "event": "Open Data Charter签署", "x": 42, "y": 42},
        {"year": 2018, "event": "数据要素价值化", "x": 68, "y": 50},
        {"year": 2020, "event": "数据成为第五大要素", "x": 72, "y": 42},
        {"year": 2022, "event": "数据二十条出台", "x": 76, "y": 34},
    ]
    
    # 绘制时间轴线
    ax.plot([5, 95], [25, 25], color='#333', linewidth=2)
    
    # 绘制节点
    for e in events:
        # 节点圆点
        circle = patches.Circle((e["x"], 25), 1.5, facecolor='#1f77b4', edgecolor='white', linewidth=1)
        ax.add_patch(circle)
        
        # 年份标注
        ax.text(e["x"], 20, str(e["year"]), ha='center', va='center', fontsize=10, fontweight='bold')
        
        # 事件标注
        ax.text(e["x"], e["y"], e["event"], ha='center', va='center', fontsize=9, 
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#1f77b4", alpha=0.8))
        
        # 连接线
        ax.plot([e["x"], e["x"]], [25, e["y"]-3], color='#1f77b4', linewidth=1, linestyle='--', alpha=0.5)
    
    # 中国节点
    china_events = [
        {"year": 2017, "event": "贵阳上线\n全国首个省级平台", "x": 45, "y": 12},
        {"year": 2020, "event": "数据成为\n第五大生产要素", "x": 75, "y": 12},
    ]
    
    ax.text(50, 8, "中国发展节点", ha='center', va='center', fontsize=12, fontweight='bold', color='#d62728')
    for ce in china_events:
        circle = patches.Circle((ce["x"], 5), 1.2, facecolor='#d62728', edgecolor='white', linewidth=1)
        ax.add_patch(circle)
        ax.text(ce["x"], ce["y"], ce["event"], ha='center', va='center', fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", fc="#ffe6e6", ec="#d62728", alpha=0.8))
        ax.plot([ce["x"], ce["x"]], [5, ce["y"]-2], color='#d62728', linewidth=1, linestyle='--', alpha=0.5)
    
    # 标题
    plt.title("全球政府数据开放平台发展历程与关键节点", fontsize=18, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('static/thesis_charts_v6/图1-1.png', dpi=300, bbox_inches='tight')
    print("生成: 图1-1.png")

if __name__ == '__main__':
    draw_global_timeline()