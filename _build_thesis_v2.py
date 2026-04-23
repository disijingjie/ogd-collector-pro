#!/usr/bin/env python3
"""从论文提取图表信息并匹配所有图片文件，生成完整 thesis.html"""
import re
from pathlib import Path

THESIS_MD = Path(__file__).parent.parent / "博士论文_图片编号最终版.md"
CHARTS_DIR = Path(__file__).parent / "static" / "thesis_charts"
OUTPUT = Path(__file__).parent / "templates" / "thesis.html"

content = THESIS_MD.read_text(encoding="utf-8")
lines = content.splitlines()

# 1. 从论文提取图表标题
titles = {}  # fname -> title
descriptions = {}  # fname -> description

# 匹配标准格式：图X-X 标题
pattern1 = re.compile(r'^(图\d+-\d+[a-z]?)\s+(.+)$')
# 匹配加粗格式：**图X-X 标题**
pattern2 = re.compile(r'^\*\*(图\d+-\d+[a-z]?)\s+(.+?)\*\*$')
# 匹配Figure行后的中文标题（fallback）
pattern3 = re.compile(r'^\*\*Figure\s+\d+-\d+\s+.+?\*\*$')

for i, line in enumerate(lines):
    line_stripped = line.strip()
    m = pattern1.match(line_stripped)
    if not m:
        m = pattern2.match(line_stripped)
    if m:
        chart_id, title = m.groups()
        fname = chart_id.replace("(", "").replace(")", "") + ".png"
        titles[fname] = title.strip('*').strip()
        # 提取说明
        desc_lines = []
        for j in range(max(0, i-4), min(len(lines), i+10)):
            if j == i:
                continue
            l = lines[j].strip()
            if l and not l.startswith("!") and not l.startswith("Figure") and not l.startswith("**Figure") and not pattern1.match(l) and not pattern2.match(l):
                if len(l) > 20 and not l.startswith("[") and not l.startswith("#"):
                    desc_lines.append(l)
        desc = " ".join(desc_lines[:2])
        desc = re.sub(r'\[\^\d+\]', '', desc)
        desc = re.sub(r'\*\*', '', desc)
        descriptions[fname] = desc[:350] + "..." if len(desc) > 350 else desc

# 2. 扫描所有图片文件
all_images = sorted([f.name for f in CHARTS_DIR.glob("图*.png")])

# 手动补充一些缺失的标题（基于论文内容分析）
manual_titles = {
    "图1-10.png": "研究内容与逻辑框架（详细版）",
    "图1-11.png": "研究技术路线图",
    "图1-12.png": "研究创新点与特色结构（详细版）",
    "图3-4.png": "整合分析框架全景图",
    "图3-5.png": "基于4E框架的政府数据开放平台数据利用绩效评估指标体系",
    "图3-6.png": "4E框架指标体系详细结构",
    "图5-7.png": "政府数据开放平台数据利用绩效时间趋势(2020-2024)",
    "图6-2.png": "fsQCA组态路径分析结果",
    "图6-4.png": "政府数据开放平台数据利用绩效影响因素DEMATEL因果图",
}
manual_desc = {
    "图1-10.png": "本研究包括八章，遵循'概念界定-理论构建-指标设计-实证评估-问题诊断-对策优化'的逻辑主线。",
    "图1-11.png": "研究技术路线图展示了从文献综述、理论构建到数据采集、实证分析、问题诊断与对策建议的完整研究流程。",
    "图1-12.png": "研究创新点包括评估范式创新、方法创新、指标体系创新与理论整合创新四个方面。",
    "图3-4.png": "整合分析框架实现了公共价值理论、4E框架与TOE框架的'三位一体'整合，形成完整的理论-分析体系。",
    "图3-5.png": "基于4E框架构建的政府数据开放平台数据利用绩效评估指标体系，包含4个一级维度、12个二级指标、36个三级指标。",
    "图3-6.png": "4E框架指标体系详细结构图展示了从环境(Economy)、效率(Efficiency)、效果(Effectiveness)到演化(Evolution)的完整指标层级。",
    "图5-7.png": "2020-2024年间30个省级政府数据开放平台数据利用绩效的时间趋势变化，揭示了绩效的动态演化特征。",
    "图6-2.png": "fsQCA组态路径分析结果展示了高绩效平台的多重等效路径，揭示了制度、技术、数据与生态条件的组态效应。",
    "图6-4.png": "DEMATEL因果图揭示了政府数据开放平台数据利用绩效影响因素的因果网络结构与中心度关系。",
}

titles.update(manual_titles)
descriptions.update(manual_desc)

# 按章节分组
chapter_names = {
    1: "第一章 绪论",
    2: "第二章 理论基础",
    3: "第三章 评估框架与指标体系",
    4: "第四章 指标体系详情",
    5: "第五章 实证研究",
    6: "第六章 问题诊断与fsQCA分析",
}

chapters = {}
for img in all_images:
    m = re.match(r'图(\d+)-(\d+)', img)
    if m:
        ch = int(m.group(1))
        if ch not in chapters:
            chapters[ch] = []
        chapters[ch].append({
            'fname': img,
            'title': titles.get(img, img.replace('.png', '')),
            'description': descriptions.get(img, "论文核心图表，展示研究的关键发现与分析结果。"),
        })

# 读取各章节摘要
chapter_abstracts = {}
for ch_num in chapter_names:
    idx = content.find(f"## {ch_num}.")
    if idx < 0:
        idx = content.find(f"第{ch_num}章")
    if idx >= 0:
        snippet = content[idx:idx+900]
        snippet = re.sub(r'!\[.*?\]\(.*?\)', '', snippet)
        snippet = re.sub(r'\[\^\d+\]', '', snippet)
        snippet = re.sub(r'#+ ', '', snippet)
        snippet = re.sub(r'\*\*', '', snippet)
        lines_abs = [l.strip() for l in snippet.splitlines() if l.strip() and len(l.strip()) > 25][:5]
        chapter_abstracts[ch_num] = " ".join(lines_abs)
    else:
        chapter_abstracts[ch_num] = ""

# 生成 HTML
html = '''{% extends "base.html" %}
{% block title %}论文成果展示 | OGD-Collector Pro{% endblock %}
{% block extra_css %}
<style>
.thesis-hero {
    background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%);
    color: white;
    padding: 50px 0;
    margin-bottom: 30px;
}
.thesis-hero h1 { font-size: 2.2rem; font-weight: 700; }
.thesis-hero .subtitle { font-size: 1.1rem; opacity: 0.9; }
.thesis-hero .meta { font-size: 0.9rem; opacity: 0.8; }

.chapter-section {
    background: white;
    border-radius: 12px;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border: 1px solid #e2e8f0;
}
.chapter-section h2 {
    color: #1e3a5f;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 3px solid #3182ce;
}
.chapter-abstract {
    background: #f7fafc;
    border-radius: 8px;
    padding: 18px;
    margin-bottom: 25px;
    color: #4a5568;
    line-height: 1.8;
    font-size: 0.95rem;
}

.chart-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border: 1px solid #e2e8f0;
    margin-bottom: 25px;
    transition: transform 0.2s, box-shadow 0.2s;
}
.chart-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}
.chart-card img {
    width: 100%;
    height: auto;
    display: block;
    background: #f7fafc;
    cursor: zoom-in;
}
.chart-body {
    padding: 20px;
}
.chart-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #2c5282;
    margin-bottom: 10px;
}
.chart-desc {
    color: #4a5568;
    font-size: 0.9rem;
    line-height: 1.7;
}
.chart-meta {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.chart-tag {
    background: #ebf8ff;
    color: #2c5282;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}
.nav-pills .nav-link {
    color: #4a5568; font-weight: 500; padding: 10px 18px;
    border-radius: 8px; margin-right: 5px; font-size: 0.9rem;
}
.nav-pills .nav-link.active {
    background: #1e3a5f; color: white;
}
.nav-pills .nav-link:hover:not(.active) {
    background: #e2e8f0;
}
.content-reader {
    background: #fff;
    border-radius: 12px;
    padding: 30px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border: 1px solid #e2e8f0;
}
.content-reader h3 {
    color: #1e3a5f;
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 15px;
}
.content-text {
    line-height: 1.9;
    color: #2d3748;
    font-size: 0.95rem;
    text-align: justify;
}
</style>
{% endblock %}

{% block content %}
<div class="thesis-hero">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-8">
                <h1>政府数据开放平台数据资源利用的评价与优化研究</h1>
                <p class="subtitle">基于三层架构的4E评估框架与fsQCA方法</p>
                <div class="meta">
                    <p>作者：文明 | 武汉大学信息管理学院 博士研究生</p>
                    <p>指导教师：陈传夫 教授</p>
                </div>
            </div>
            <div class="col-lg-4 text-end">
                <div class="d-inline-block text-center px-4 py-3" style="background:rgba(255,255,255,0.1);border-radius:12px;">
                    <div style="font-size:2.5rem;font-weight:700;">''' + str(len(all_images)) + '''</div>
                    <div style="opacity:0.8;">张核心图表</div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="container">
    <ul class="nav nav-pills mb-4" id="thesisTab" role="tablist">
        <li class="nav-item"><button class="nav-link active" data-bs-toggle="pill" data-bs-target="#overview">研究概览</button></li>
'''
for ch in sorted(chapters.keys()):
    html += f'        <li class="nav-item"><button class="nav-link" data-bs-toggle="pill" data-bs-target="#ch{ch}">{chapter_names.get(ch, f"第{ch}章")}</button></li>\n'
html += '''        <li class="nav-item"><button class="nav-link" data-bs-toggle="pill" data-bs-target="#allcharts">全部图表</button></li>
    </ul>

    <div class="tab-content">
        <div class="tab-pane fade show active" id="overview">
            <div class="chapter-section">
                <h2><i class="bi bi-journal-bookmark-fill me-2"></i>研究概览</h2>
                <div class="row">
                    <div class="col-lg-7">
                        <div class="content-text">
                            <p>本研究聚焦<strong>"政府数据开放平台数据资源利用的评价与优化"</strong>，旨在回答三个核心问题：</p>
                            <ol>
                                <li><strong>如何科学评价</strong>政府数据开放平台的数据资源利用绩效？</li>
                                <li><strong>哪些因素</strong>影响平台数据资源利用绩效？</li>
                                <li><strong>如何优化</strong>不同层级、不同区域平台的数据资源利用？</li>
                            </ol>
                            <p>研究构建<strong>"环境-效率-效果-演化"（4E）四维评估框架</strong>，将fsQCA方法引入政府数据开放评价领域，覆盖<strong>31个省级、13个副省级、287个地级市</strong>平台，形成包含4个一级维度、12个二级指标、36个三级指标的三层架构评估体系。</p>
                            <p>研究发现：我国政府数据开放正在经历"有数据无利用"的困境——数据从"不可获取"变为"可获取"，但并未从"可获取"进阶为"可利用"。副省级平台平均得分最高（0.623），省级次之（0.405），地级市已建平台平均0.318，尚有78.4%的地级市未建平台。</p>
                        </div>
                    </div>
                    <div class="col-lg-5">
                        <div class="row g-3">
                            <div class="col-6"><div class="p-3 text-center" style="background:linear-gradient(135deg,#c6f6d5,#9ae6b4);border-radius:10px;"><div style="font-size:1.8rem;font-weight:700;color:#22543d;">331</div><div style="color:#276749;font-size:0.85rem;">平台样本</div></div></div>
                            <div class="col-6"><div class="p-3 text-center" style="background:linear-gradient(135deg,#feebc8,#fbd38d);border-radius:10px;"><div style="font-size:1.8rem;font-weight:700;color:#744210;">36</div><div style="color:#744210;font-size:0.85rem;">评估指标</div></div></div>
                            <div class="col-6"><div class="p-3 text-center" style="background:linear-gradient(135deg,#fed7d7,#fc8181);border-radius:10px;"><div style="font-size:1.8rem;font-weight:700;color:#742a2a;">504</div><div style="color:#742a2a;font-size:0.85rem;">参考文献</div></div></div>
                            <div class="col-6"><div class="p-3 text-center" style="background:linear-gradient(135deg,#e9d8fd,#b794f4);border-radius:10px;"><div style="font-size:1.8rem;font-weight:700;color:#44337a;">8</div><div style="color:#44337a;font-size:0.85rem;">章节结构</div></div></div>
                        </div>
                        <div class="mt-3 p-3" style="background:#ebf8ff;border-radius:10px;">
                            <div class="small fw-semibold text-primary mb-2">研究创新点</div>
                            <div class="small text-muted">• 评估范式从"供给导向"向"效果导向"转型</div>
                            <div class="small text-muted">• fsQCA方法揭示多重并发因果机制</div>
                            <div class="small text-muted">• 三层架构指标体系覆盖331个平台</div>
                            <div class="small text-muted">• "制度-技术-数据-生态"四维解释框架</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
'''

for ch in sorted(chapters.keys()):
    ch_name = chapter_names.get(ch, f"第{ch}章")
    abstract = chapter_abstracts.get(ch, "")
    html += f'''
        <div class="tab-pane fade" id="ch{ch}">
            <div class="chapter-section">
                <h2>{ch_name}</h2>
                <div class="chapter-abstract">{abstract}</div>
                <div class="row">
'''
    for c in chapters[ch]:
        html += f'''
                    <div class="col-md-6">
                        <div class="chart-card">
                            <img src="/static/thesis_charts/{c['fname']}" alt="{c['title']}" loading="lazy">
                            <div class="chart-body">
                                <div class="chart-title">{c['fname'].replace('.png','')} {c['title']}</div>
                                <div class="chart-desc">{c['description']}</div>
                                <div class="chart-meta">
                                    <span class="chart-tag">{ch_name}</span>
                                    <span class="text-muted small"><i class="bi bi-zoom-in me-1"></i>点击放大</span>
                                </div>
                            </div>
                        </div>
                    </div>
'''
    html += '''                </div>
            </div>
        </div>
'''

html += '''
        <div class="tab-pane fade" id="allcharts">
            <div class="chapter-section">
                <h2><i class="bi bi-images me-2"></i>全部论文图表</h2>
                <div class="row">
'''
for ch in sorted(chapters.keys()):
    for c in chapters[ch]:
        ch_name = chapter_names.get(ch, f"第{ch}章")
        html += f'''
                    <div class="col-md-4">
                        <div class="chart-card">
                            <img src="/static/thesis_charts/{c['fname']}" alt="{c['title']}" loading="lazy" style="max-height:200px;object-fit:cover;">
                            <div class="chart-body">
                                <div class="chart-title" style="font-size:0.95rem;">{c['fname'].replace('.png','')} {c['title']}</div>
                                <div class="chart-meta">
                                    <span class="chart-tag">{ch_name}</span>
                                </div>
                            </div>
                        </div>
                    </div>
'''

html += '''                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
document.querySelectorAll('.chart-card img').forEach(img => {
    img.addEventListener('click', function() {
        const modal = document.createElement('div');
        modal.style.cssText = `position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.92);z-index:9999;display:flex;align-items:center;justify-content:center;cursor:zoom-out;overflow:auto;padding:40px;`;
        modal.innerHTML = `<img src="${this.src}" style="max-width:90%;max-height:90vh;object-fit:contain;border-radius:8px;box-shadow:0 20px 60px rgba(0,0,0,0.5);">`;
        modal.addEventListener('click', () => modal.remove());
        document.body.appendChild(modal);
    });
});
</script>
{% endblock %}
'''

OUTPUT.write_text(html, encoding="utf-8")
print(f"[OK] 生成 thesis.html，共 {len(all_images)} 张图表")
for ch in sorted(chapters.keys()):
    print(f"  第{ch}章: {len(chapters[ch])} 张")
for img in all_images:
    if img not in titles:
        print(f"  [WARN] 无标题: {img}")
