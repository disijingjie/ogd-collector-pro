#!/usr/bin/env python3
"""从论文提取图表信息，生成 thesis.html"""
import re
from pathlib import Path

THESIS_MD = Path(__file__).parent.parent / "博士论文_图片编号最终版.md"
OUTPUT = Path(__file__).parent / "templates" / "thesis.html"

# 读取论文
content = THESIS_MD.read_text(encoding="utf-8")
lines = content.splitlines()

# 提取所有图表标题和说明
charts = []
# 匹配模式：图X-X 标题 或 图X-X(a) 标题
pattern = re.compile(r'^(图\d+-\d+[a-z]?)\s+(.+)$')

for i, line in enumerate(lines):
    m = pattern.match(line.strip())
    if m:
        chart_id, title = m.groups()
        # 转换为文件名格式
        fname = chart_id.replace("(", "").replace(")", "") + ".png"
        # 提取前后说明文字（前5行到后10行）
        desc_lines = []
        for j in range(max(0, i-5), min(len(lines), i+12)):
            if j == i:
                continue
            l = lines[j].strip()
            if l and not l.startswith("!") and not l.startswith("Figure") and not l.startswith("**Figure"):
                if len(l) > 20 and not l.startswith("[^"):
                    desc_lines.append(l)
        description = " ".join(desc_lines[:3])  # 取最多3句
        # 清理 markdown 格式
        description = re.sub(r'\[\^\d+\]', '', description)
        description = re.sub(r'\*\*', '', description)
        description = description[:300] + "..." if len(description) > 300 else description

        charts.append({
            'id': chart_id,
            'fname': fname,
            'title': title,
            'description': description,
            'chapter': int(chart_id[1:chart_id.index('-')])
        })

# 按章节分组
chapters = {}
for c in charts:
    ch = c['chapter']
    if ch not in chapters:
        chapters[ch] = []
    chapters[ch].append(c)

chapter_names = {
    1: "第一章 绪论",
    2: "第二章 理论基础",
    3: "第三章 评估框架构建",
    4: "第四章 指标体系",
    5: "第五章 实证研究",
    6: "第六章 问题诊断与fsQCA分析",
}

# 读取论文各章节开头内容作为摘要
chapter_abstracts = {}
for ch_num, ch_name in chapter_names.items():
    # 简单提取该章节附近的内容
    idx = content.find(f"## {ch_num}.")
    if idx < 0:
        idx = content.find(f"第{ch_num}章")
    if idx >= 0:
        snippet = content[idx:idx+800]
        # 清理 markdown
        snippet = re.sub(r'!\[.*?\]\(.*?\)', '', snippet)
        snippet = re.sub(r'\[\^\d+\]', '', snippet)
        snippet = re.sub(r'#+ ', '', snippet)
        snippet = re.sub(r'\*\*', '', snippet)
        lines_abs = [l.strip() for l in snippet.splitlines() if l.strip() and len(l.strip()) > 30][:4]
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
                    <div style="font-size:2.5rem;font-weight:700;">''' + str(len(charts)) + '''</div>
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
        <!-- 研究概览 -->
        <div class="tab-pane fade show active" id="overview">
            <div class="chapter-section">
                <h2><i class="bi bi-journal-bookmark-fill me-2"></i>研究概览</h2>
                <div class="row">
                    <div class="col-lg-6">
                        <p style="line-height:1.8;color:#4a5568;">
                            本研究聚焦<strong>"政府数据开放平台数据资源利用的评价与优化"</strong>，
                            旨在回答三个核心问题：如何科学评价平台数据资源利用绩效？哪些因素影响绩效？如何优化不同层级、区域的平台？
                        </p>
                        <p style="line-height:1.8;color:#4a5568;">
                            研究构建<strong>"环境-效率-效果-演化"（4E）四维评估框架</strong>，
                            将fsQCA方法引入政府数据开放评价领域，覆盖<strong>31个省级、13个副省级、287个地级市</strong>平台，
                            形成包含4个一级维度、12个二级指标、36个三级指标的三层架构评估体系。
                        </p>
                    </div>
                    <div class="col-lg-6">
                        <div class="row g-3">
                            <div class="col-6"><div class="p-3 text-center" style="background:linear-gradient(135deg,#c6f6d5,#9ae6b4);border-radius:10px;"><div style="font-size:1.8rem;font-weight:700;color:#22543d;">331</div><div style="color:#276749;font-size:0.85rem;">平台样本</div></div></div>
                            <div class="col-6"><div class="p-3 text-center" style="background:linear-gradient(135deg,#feebc8,#fbd38d);border-radius:10px;"><div style="font-size:1.8rem;font-weight:700;color:#744210;">36</div><div style="color:#744210;font-size:0.85rem;">评估指标</div></div></div>
                            <div class="col-6"><div class="p-3 text-center" style="background:linear-gradient(135deg,#fed7d7,#fc8181);border-radius:10px;"><div style="font-size:1.8rem;font-weight:700;color:#742a2a;">504</div><div style="color:#742a2a;font-size:0.85rem;">参考文献</div></div></div>
                            <div class="col-6"><div class="p-3 text-center" style="background:linear-gradient(135deg,#e9d8fd,#b794f4);border-radius:10px;"><div style="font-size:1.8rem;font-weight:700;color:#44337a;">8</div><div style="color:#44337a;font-size:0.85rem;">章节结构</div></div></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
'''

# 各章节
for ch in sorted(chapters.keys()):
    ch_name = chapter_names.get(ch, f"第{ch}章")
    abstract = chapter_abstracts.get(ch, "")
    html += f'''
        <!-- {ch_name} -->
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
                                <div class="chart-title">{c['id']} {c['title']}</div>
                                <div class="chart-desc">{c['description']}</div>
                                <div class="chart-meta">
                                    <span class="chart-tag">{ch_name}</span>
                                    <span class="text-muted small"><i class="bi bi-image me-1"></i>点击查看大图</span>
                                </div>
                            </div>
                        </div>
                    </div>
'''
    html += '''                </div>
            </div>
        </div>
'''

# 全部图表
html += '''
        <!-- 全部图表 -->
        <div class="tab-pane fade" id="allcharts">
            <div class="chapter-section">
                <h2><i class="bi bi-images me-2"></i>全部论文图表</h2>
                <div class="row">
'''
for c in charts:
    ch_name = chapter_names.get(c['chapter'], f"第{c['chapter']}章")
    html += f'''
                    <div class="col-md-4">
                        <div class="chart-card">
                            <img src="/static/thesis_charts/{c['fname']}" alt="{c['title']}" loading="lazy" style="max-height:220px;object-fit:cover;">
                            <div class="chart-body">
                                <div class="chart-title" style="font-size:0.95rem;">{c['id']} {c['title']}</div>
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
print(f"[OK] 生成 thesis.html，共 {len(charts)} 张图表")
for ch in sorted(chapters.keys()):
    print(f"  第{ch}章: {len(chapters[ch])} 张")
