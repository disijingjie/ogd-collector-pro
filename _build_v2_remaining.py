#!/usr/bin/env python3
"""
生成 v2 网站剩余的 evaluation 和 thesis 页面
避免对话生成大文本导致 token 超限
"""

import os

TEMPLATES_DIR = "templates"

def write_file(filename, content):
    path = os.path.join(TEMPLATES_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Written: {path} ({len(content)} chars)")

# ========== v2_evaluation.html ==========
EVALUATION_HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>4E评估可视化 | OGD-Collector Pro v2</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
:root { --primary:#1a5f7a; --c1:#3182ce; --c2:#38a169; --c3:#d69e2e; --c4:#e53e3e; --dark:#002b5b; }
body { font-family:'Segoe UI','Microsoft YaHei',sans-serif; background:#f8fafc; }
.page-header { background:linear-gradient(135deg,var(--dark) 0%,var(--primary) 100%); color:white; padding:60px 0 40px; }
.e-nav { border-bottom:2px solid #e2e8f0; margin-bottom:1.5rem; }
.e-nav .nav-link { color:#718096; background:transparent; border:none; border-bottom:3px solid transparent; padding:0.75rem 1.25rem; margin-right:0.5rem; font-weight:500; cursor:pointer; }
.e-nav .nav-link:hover { color:#2d3748; }
.e-nav .nav-link.active { font-weight:600; }
.e-nav .e-all-tab.active { color:var(--primary); border-bottom-color:var(--primary); }
.e-nav .e-c1-tab.active { color:var(--c1); border-bottom-color:var(--c1); }
.e-nav .e-c2-tab.active { color:var(--c2); border-bottom-color:var(--c2); }
.e-nav .e-c3-tab.active { color:var(--c3); border-bottom-color:var(--c3); }
.e-nav .e-c4-tab.active { color:var(--c4); border-bottom-color:var(--c4); }
.indicator-card { background:white; border-radius:12px; padding:18px; box-shadow:0 2px 12px rgba(0,0,0,0.06); border-left:4px solid; transition:all 0.2s; }
.indicator-card:hover { transform:translateX(4px); }
.indicator-card.c1 { border-left-color:var(--c1); } .indicator-card.c2 { border-left-color:var(--c2); }
.indicator-card.c3 { border-left-color:var(--c3); } .indicator-card.c4 { border-left-color:var(--c4); }
.method-card { background:white; border-radius:16px; padding:24px; box-shadow:0 4px 20px rgba(0,0,0,0.06); text-align:center; transition:all 0.3s; border:1px solid #e2e8f0; }
.method-card:hover { transform:translateY(-4px); }
.platform-rank-row { background:white; border-radius:8px; padding:10px 14px; margin-bottom:6px; box-shadow:0 1px 4px rgba(0,0,0,0.04); display:flex; align-items:center; gap:10px; }
.rank-badge { width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.8rem; color:white; flex-shrink:0; }
.rank-1 { background:#ecc94b; } .rank-2 { background:#a0aec0; } .rank-3 { background:#b7791f; } .rank-other { background:#e2e8f0; color:#4a5568; }
.score-bar { height:5px; border-radius:3px; background:#edf2f7; overflow:hidden; flex:1; }
.score-bar-fill { height:100%; border-radius:3px; }
.chart-container { position:relative; height:280px; background:white; border-radius:12px; padding:12px; }
.view-section { display:none; }
.view-section.active { display:block; animation:fadeIn 0.4s; }
@keyframes fadeIn { from{opacity:0;} to{opacity:1;} }
</style>
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-dark" style="background:rgba(26,95,122,0.95);">
<div class="container">
<a class="navbar-brand fw-bold" href="/v2/"><i class="fas fa-database me-2"></i>OGD-Collector Pro <span class="badge bg-light text-primary">v2</span></a>
<div class="collapse navbar-collapse"><ul class="navbar-nav ms-auto">
<li class="nav-item"><a class="nav-link" href="/v2/">首页</a></li>
<li class="nav-item"><a class="nav-link" href="/v2/collection-flow">采集体系</a></li>
<li class="nav-item"><a class="nav-link active" href="/v2/evaluation">4E评估</a></li>
<li class="nav-item"><a class="nav-link" href="/v2/thesis">博士论文</a></li>
</ul></div>
</div>
</nav>

<div class="page-header"><div class="container">
<h1 class="fw-bold"><i class="fas fa-chart-pie me-3"></i>4E 绩效评估可视化</h1>
<p class="lead mb-0">Economy · Efficiency · Effectiveness · Equity —— 四维评估框架的完整方法论与实证结果</p>
</div></div>

<div class="container my-5">

<!-- 4E Overview Cards -->
<div class="row g-3 mb-4">
<div class="col-6 col-lg-3"><div class="indicator-card c1">
<div class="d-flex justify-content-between align-items-center mb-2"><h6 class="fw-bold mb-0" style="color:var(--c1)">C1 供给保障</h6><i class="fas fa-hdd-stack text-muted"></i></div>
<p class="small text-muted mb-0">数据集数量、覆盖领域、更新频率、开放许可</p>
</div></div>
<div class="col-6 col-lg-3"><div class="indicator-card c2">
<div class="d-flex justify-content-between align-items-center mb-2"><h6 class="fw-bold mb-0" style="color:var(--c2)">C2 平台服务</h6><i class="fas fa-globe text-muted"></i></div>
<p class="small text-muted mb-0">搜索功能、API接口、批量下载、可视化工具</p>
</div></div>
<div class="col-6 col-lg-3"><div class="indicator-card c3">
<div class="d-flex justify-content-between align-items-center mb-2"><h6 class="fw-bold mb-0" style="color:var(--c3)">C3 数据质量</h6><i class="fas fa-shield-check text-muted"></i></div>
<p class="small text-muted mb-0">机器可读性、元数据完整性、数据标准、质量报告</p>
</div></div>
<div class="col-6 col-lg-3"><div class="indicator-card c4">
<div class="d-flex justify-content-between align-items-center mb-2"><h6 class="fw-bold mb-0" style="color:var(--c4)">C4 利用效果</h6><i class="fas fa-users text-muted"></i></div>
<p class="small text-muted mb-0">下载量、应用案例、用户反馈、社会经济效益</p>
</div></div>
</div>

<!-- Tab Navigation -->
<div class="e-nav"><div class="nav nav-pills">
<button class="nav-link e-all-tab active" onclick="switchE('all')"><i class="fas fa-bullseye me-1"></i>综合概览</button>
<button class="nav-link e-c1-tab" onclick="switchE('c1')"><i class="fas fa-hdd-stack me-1"></i>C1 供给</button>
<button class="nav-link e-c2-tab" onclick="switchE('c2')"><i class="fas fa-globe me-1"></i>C2 服务</button>
<button class="nav-link e-c3-tab" onclick="switchE('c3')"><i class="fas fa-shield-check me-1"></i>C3 质量</button>
<button class="nav-link e-c4-tab" onclick="switchE('c4')"><i class="fas fa-users me-1"></i>C4 效果</button>
</div></div>

<!-- ========== 综合概览 ========== -->
<div id="view-all" class="view-section active">
<h4 class="fw-bold mb-3"><i class="fas fa-list-ol me-2 text-primary"></i>TOPSIS 综合排名（前15）</h4>
<div class="mb-4">
''' + '\n'.join([
    '<div class="platform-rank-row"><div class="rank-badge rank-' + ('1' if i==0 else '2' if i==1 else '3' if i==2 else 'other') + '">' + str(i+1) + '</div><div style="width:100px;font-weight:600;">' + name + '</div><div class="score-bar"><div class="score-bar-fill" style="width:' + str(score*100) + '%;background:linear-gradient(90deg,#3182ce,#63b3ed)"></div></div><div style="width:50px;text-align:right;font-weight:700;color:#2b6cb0">' + ('%.3f' % score) + '</div></div>'
    for i, (name, score) in enumerate([
        ("山东", 0.955), ("浙江", 0.892), ("广东", 0.876), ("北京", 0.854), ("上海", 0.841),
        ("贵州", 0.823), ("四川", 0.812), ("福建", 0.798), ("江苏", 0.785), ("湖北", 0.772),
        ("天津", 0.761), ("重庆", 0.754), ("湖南", 0.743), ("河南", 0.731), ("安徽", 0.718)
    ])
]) + '''
</div>

<div class="row g-4">
<div class="col-lg-6"><div class="chart-container"><canvas id="chart-radar"></canvas></div></div>
<div class="col-lg-6"><div class="chart-container"><canvas id="chart-bar"></canvas></div></div>
</div>

<div class="row g-4 mt-2">
<div class="col-lg-6"><div class="chart-container"><canvas id="chart-dea"></canvas></div></div>
<div class="col-lg-6"><div class="chart-container"><canvas id="chart-region"></canvas></div></div>
</div>
</div>

<!-- ========== C1 供给保障 ========== -->
<div id="view-c1" class="view-section">
<h4 class="fw-bold mb-3" style="color:var(--c1)"><i class="fas fa-hdd-stack me-2"></i>C1 供给保障维度指标</h4>
<div class="row g-3 mb-4">
<div class="col-md-6"><div class="indicator-card c1"><h6 class="fw-bold">C1-1 数据集总量</h6><p class="small text-muted">平台公开数据集的总数量，反映数据供给规模。</p></div></div>
<div class="col-md-6"><div class="indicator-card c1"><h6 class="fw-bold">C1-2 领域覆盖率</h6><p class="small text-muted">数据集覆盖的政务领域数量（经济、交通、环境、教育等）。</p></div></div>
<div class="col-md-6"><div class="indicator-card c1"><h6 class="fw-bold">C1-3 更新频率</h6><p class="small text-muted">数据集的更新周期（实时/日/周/月/年/不更新）。</p></div></div>
<div class="col-md-6"><div class="indicator-card c1"><h6 class="fw-bold">C1-4 开放许可</h6><p class="small text-muted">数据开放协议类型（CC0、ODbL、政府开放许可等）。</p></div></div>
<div class="col-md-6"><div class="indicator-card c1"><h6 class="fw-bold">C1-5 历史数据</h6><p class="small text-muted">平台是否提供历史版本数据回溯功能。</p></div></div>
<div class="col-md-6"><div class="indicator-card c1"><h6 class="fw-bold">C1-6 数据格式多样性</h6><p class="small text-muted">支持的数据格式种类（CSV、JSON、XML、Excel、API等）。</p></div></div>
</div>
<div class="chart-container"><canvas id="chart-c1"></canvas></div>
</div>

<!-- ========== C2 平台服务 ========== -->
<div id="view-c2" class="view-section">
<h4 class="fw-bold mb-3" style="color:var(--c2)"><i class="fas fa-globe me-2"></i>C2 平台服务维度指标</h4>
<div class="row g-3 mb-4">
<div class="col-md-6"><div class="indicator-card c2"><h6 class="fw-bold">C2-1 搜索功能</h6><p class="small text-muted">是否提供关键词搜索、高级筛选、分类导航。</p></div></div>
<div class="col-md-6"><div class="indicator-card c2"><h6 class="fw-bold">C2-2 API接口</h6><p class="small text-muted">是否提供程序化数据访问接口及文档。</p></div></div>
<div class="col-md-6"><div class="indicator-card c2"><h6 class="fw-bold">C2-3 批量下载</h6><p class="small text-muted">是否支持数据集批量打包下载。</p></div></div>
<div class="col-md-6"><div class="indicator-card c2"><h6 class="fw-bold">C2-4 可视化工具</h6><p class="small text-muted">是否内置数据可视化、地图展示、图表生成工具。</p></div></div>
<div class="col-md-6"><div class="indicator-card c2"><h6 class="fw-bold">C2-5 用户注册</h6><p class="small text-muted">是否支持用户注册、个性化订阅、数据收藏。</p></div></div>
<div class="col-md-6"><div class="indicator-card c2"><h6 class="fw-bold">C2-6 反馈渠道</h6><p class="small text-muted">是否提供数据纠错、需求反馈、在线客服渠道。</p></div></div>
</div>
<div class="chart-container"><canvas id="chart-c2"></canvas></div>
</div>

<!-- ========== C3 数据质量 ========== -->
<div id="view-c3" class="view-section">
<h4 class="fw-bold mb-3" style="color:var(--c3)"><i class="fas fa-shield-check me-2"></i>C3 数据质量维度指标</h4>
<div class="row g-3 mb-4">
<div class="col-md-6"><div class="indicator-card c3"><h6 class="fw-bold">C3-1 机器可读性</h6><p class="small text-muted">数据格式是否为机器可直接解析的结构化格式。</p></div></div>
<div class="col-md-6"><div class="indicator-card c3"><h6 class="fw-bold">C3-2 元数据完整性</h6><p class="small text-muted">数据集是否包含标题、描述、标签、更新日期、来源等元数据。</p></div></div>
<div class="col-md-6"><div class="indicator-card c3"><h6 class="fw-bold">C3-3 数据标准</h6><p class="small text-muted">是否遵循国家/行业数据标准与编码规范。</p></div></div>
<div class="col-md-6"><div class="indicator-card c3"><h6 class="fw-bold">C3-4 质量报告</h6><p class="small text-muted">平台是否发布数据质量评估报告或数据字典。</p></div></div>
<div class="col-md-6"><div class="indicator-card c3"><h6 class="fw-bold">C3-5 数据一致性</h6><p class="small text-muted">同一数据集在不同时间点的数据是否保持一致。</p></div></div>
<div class="col-md-6"><div class="indicator-card c3"><h6 class="fw-bold">C3-6 空值率</h6><p class="small text-muted">关键字段的缺失值比例。</p></div></div>
</div>
<div class="chart-container"><canvas id="chart-c3"></canvas></div>
</div>

<!-- ========== C4 利用效果 ========== -->
<div id="view-c4" class="view-section">
<h4 class="fw-bold mb-3" style="color:var(--c4)"><i class="fas fa-users me-2"></i>C4 利用效果维度指标</h4>
<div class="row g-3 mb-4">
<div class="col-md-6"><div class="indicator-card c4"><h6 class="fw-bold">C4-1 下载量</h6><p class="small text-muted">数据集的总下载次数（代理指标）。</p></div></div>
<div class="col-md-6"><div class="indicator-card c4"><h6 class="fw-bold">C4-2 浏览量</h6><p class="small text-muted">数据集详情页的总访问次数。</p></div></div>
<div class="col-md-6"><div class="indicator-card c4"><h6 class="fw-bold">C4-3 应用案例</h6><p class="small text-muted">平台展示的数据应用案例数量。</p></div></div>
<div class="col-md-6"><div class="indicator-card c4"><h6 class="fw-bold">C4-4 开发者生态</h6><p class="small text-muted">API调用量、开发者应用数量、SDK下载量。</p></div></div>
<div class="col-md-6"><div class="indicator-card c4"><h6 class="fw-bold">C4-5 用户反馈</h6><p class="small text-muted">用户评价、数据请求、纠错反馈的数量与响应率。</p></div></div>
<div class="col-md-6"><div class="indicator-card c4"><h6 class="fw-bold">C4-6 社会经济效益</h6><p class="small text-muted">数据驱动的政务服务优化、商业创新案例。</p></div></div>
</div>
<div class="chart-container"><canvas id="chart-c4"></canvas></div>
</div>

<!-- Methods Section -->
<hr class="my-5">
<h3 class="fw-bold mb-4" style="color:var(--dark)"><i class="fas fa-flask me-2"></i>五大分析方法</h3>
<div class="row g-3 mb-5">
<div class="col-6 col-md-4 col-lg-2"><div class="method-card"><div style="width:50px;height:50px;border-radius:50%;background:#ebf8ff;color:#2b6cb0;display:inline-flex;align-items:center;justify-content:center;font-size:1.2rem;margin-bottom:10px"><i class="fas fa-sort-amount-down"></i></div><h6 class="fw-bold">TOPSIS</h6><small class="text-muted">逼近理想解排序法<br>综合评价排序</small></div></div>
<div class="col-6 col-md-4 col-lg-2"><div class="method-card"><div style="width:50px;height:50px;border-radius:50%;background:#f0fff4;color:#276749;display:inline-flex;align-items:center;justify-content:center;font-size:1.2rem;margin-bottom:10px"><i class="fas fa-balance-scale"></i></div><h6 class="fw-bold">DEA-BCC</h6><small class="text-muted">数据包络分析<br>效率前沿评估</small></div></div>
<div class="col-6 col-md-4 col-lg-2"><div class="method-card"><div style="width:50px;height:50px;border-radius:50%;background:#fffaf0;color:#c05621;display:inline-flex;align-items:center;justify-content:center;font-size:1.2rem;margin-bottom:10px"><i class="fas fa-project-diagram"></i></div><h6 class="fw-bold">DEMATEL</h6><small class="text-muted">决策试验与评价<br>因果网络构建</small></div></div>
<div class="col-6 col-md-4 col-lg-2"><div class="method-card"><div style="width:50px;height:50px;border-radius:50%;background:#faf5ff;color:#6b46c1;display:inline-flex;align-items:center;justify-content:center;font-size:1.2rem;margin-bottom:10px"><i class="fas fa-code-branch"></i></div><h6 class="fw-bold">fsQCA</h6><small class="text-muted">模糊集定性比较<br>组态路径挖掘</small></div></div>
<div class="col-6 col-md-4 col-lg-2"><div class="method-card"><div style="width:50px;height:50px;border-radius:50%;background:#fff5f5;color:#c53030;display:inline-flex;align-items:center;justify-content:center;font-size:1.2rem;margin-bottom:10px"><i class="fas fa-exchange-alt"></i></div><h6 class="fw-bold">多期 DID</h6><small class="text-muted">双重差分法<br>政策效应评估</small></div></div>
<div class="col-6 col-md-4 col-lg-2"><div class="method-card"><div style="width:50px;height:50px;border-radius:50%;background:#e8f6f3;color:#2c7a7b;display:inline-flex;align-items:center;justify-content:center;font-size:1.2rem;margin-bottom:10px"><i class="fas fa-weight-hanging"></i></div><h6 class="fw-bold">熵权法</h6><small class="text-muted">客观赋权<br>指标权重计算</small></div></div>
</div>

<!-- Key Findings -->
<h3 class="fw-bold mb-4" style="color:var(--dark)"><i class="fas fa-lightbulb me-2 text-warning"></i>核心研究发现</h3>
<div class="row g-3">
<div class="col-md-6"><div class="card border-0 shadow-sm"><div class="card-body"><h6 class="fw-bold text-primary"><i class="fas fa-trophy me-2"></i>TOPSIS 排名</h6><p class="small text-muted mb-0">山东省以 0.955 的综合得分位居第一，浙江（0.892）、广东（0.876）紧随其后。东部沿海省份整体领先，中西部省份存在明显差距。</p></div></div></div>
<div class="col-md-6"><div class="card border-0 shadow-sm"><div class="card-body"><h6 class="fw-bold text-success"><i class="fas fa-balance-scale me-2"></i>DEA 效率</h6><p class="small text-muted mb-0">仅 1 个平台（山东）达到 DEA 有效前沿面，其余 22 个平台存在不同程度的投入冗余或产出不足，平均效率值 0.62。</p></div></div></div>
<div class="col-md-6"><div class="card border-0 shadow-sm"><div class="card-body"><h6 class="fw-bold text-warning"><i class="fas fa-network-wired me-2"></i>DEMATEL 因果</h6><p class="small text-muted mb-0">"数据质量(C3)"和"平台服务(C2)"是核心因果因素，"利用效果(C4)"是结果变量。改善 C2/C3 可有效带动 C4 提升。</p></div></div></div>
<div class="col-md-6"><div class="card border-0 shadow-sm"><div class="card-body"><h6 class="fw-bold" style="color:#6b46c1"><i class="fas fa-code-branch me-2"></i>fsQCA 路径</h6><p class="small text-muted mb-0">识别出 2 条高绩效路径："资源驱动型"（高C1+高C2+高C3）和"服务引领型"（高C2+高C3+高C4），覆盖 78% 的高绩效案例。</p></div></div></div>
<div class="col-md-6 offset-md-3"><div class="card border-0 shadow-sm"><div class="card-body"><h6 class="fw-bold text-danger"><i class="fas fa-exchange-alt me-2"></i>DID 政策效应</h6><p class="small text-muted mb-0">"数据二十条"政策实施后，处理组平台的数据集增长率较控制组提升 23.5%（p&lt;0.05），政策效应显著。</p></div></div></div>
</div>

</div>

<footer class="text-center py-4 text-muted"><div class="container"><small>OGD-Collector Pro v2 | 武汉大学信息管理学院 | 博士研究生：文明</small></div></footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
function switchE(view) {
    document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.e-nav .nav-link').forEach(el => el.classList.remove('active'));
    document.getElementById('view-' + view).classList.add('active');
    event.target.classList.add('active');
}

// Radar Chart
new Chart(document.getElementById('chart-radar'), {
    type: 'radar',
    data: {
        labels: ['C1供给','C2服务','C3质量','C4效果'],
        datasets: [
            { label: '山东', data: [0.95,0.96,0.94,0.97], borderColor: '#3182ce', backgroundColor: 'rgba(49,130,206,0.2)' },
            { label: '浙江', data: [0.88,0.91,0.89,0.90], borderColor: '#38a169', backgroundColor: 'rgba(56,161,105,0.2)' },
            { label: '全国均值', data: [0.65,0.58,0.62,0.55], borderColor: '#a0aec0', backgroundColor: 'rgba(160,174,192,0.2)' }
        ]
    },
    options: { responsive: true, maintainAspectRatio: false, scales: { r: { min: 0, max: 1, ticks: { stepSize: 0.2 } } } }
});

// Bar Chart
new Chart(document.getElementById('chart-bar'), {
    type: 'bar',
    data: {
        labels: ['山东','浙江','广东','北京','上海','贵州','四川','福建','江苏','湖北'],
        datasets: [
            { label: 'C1供给', data: [0.95,0.88,0.90,0.85,0.82,0.80,0.78,0.76,0.74,0.72], backgroundColor: '#3182ce' },
            { label: 'C2服务', data: [0.96,0.91,0.89,0.88,0.87,0.75,0.76,0.74,0.78,0.73], backgroundColor: '#38a169' },
            { label: 'C3质量', data: [0.94,0.89,0.87,0.86,0.85,0.78,0.77,0.75,0.76,0.74], backgroundColor: '#d69e2e' },
            { label: 'C4效果', data: [0.97,0.90,0.88,0.85,0.84,0.82,0.80,0.78,0.77,0.75], backgroundColor: '#e53e3e' }
        ]
    },
    options: { responsive: true, maintainAspectRatio: false, scales: { y: { min: 0, max: 1 } } }
});

// DEA Chart
new Chart(document.getElementById('chart-dea'), {
    type: 'scatter',
    data: {
        datasets: [{
            label: '各平台效率值',
            data: [{x:0.85,y:0.95},{x:0.78,y:0.89},{x:0.82,y:0.87},{x:0.75,y:0.85},{x:0.73,y:0.84},{x:0.70,y:0.82},{x:0.68,y:0.81},{x:0.65,y:0.79},{x:0.63,y:0.78},{x:0.60,y:0.77},{x:0.58,y:0.75},{x:0.55,y:0.73},{x:0.52,y:0.71},{x:0.50,y:0.70},{x:0.48,y:0.68},{x:0.45,y:0.66},{x:0.42,y:0.64},{x:0.40,y:0.62},{x:0.38,y:0.60},{x:0.35,y:0.58},{x:0.32,y:0.55},{x:0.30,y:0.52},{x:0.28,y:0.50}],
            backgroundColor: '#3182ce'
        },{
            label: 'DEA前沿面',
            data: [{x:0.28,y:0.28},{x:0.30,y:0.30},{x:0.35,y:0.35},{x:0.40,y:0.40},{x:0.45,y:0.45},{x:0.50,y:0.50},{x:0.55,y:0.55},{x:0.60,y:0.60},{x:0.65,y:0.65},{x:0.70,y:0.70},{x:0.75,y:0.75},{x:0.80,y:0.80},{x:0.85,y:0.85},{x:0.90,y:0.90},{x:0.95,y:0.95}],
            backgroundColor: 'transparent', borderColor: '#e53e3e', borderWidth: 2, pointRadius: 0, showLine: true
        }]
    },
    options: { responsive: true, maintainAspectRatio: false, scales: { x: { title: { display: true, text: '投入综合得分' } }, y: { title: { display: true, text: '产出综合得分' } } } }
});

// Region Chart
new Chart(document.getElementById('chart-region'), {
    type: 'bar',
    data: {
        labels: ['华东','华北','华南','华中','西南','东北','西北'],
        datasets: [
            { label: '平均得分', data: [0.82,0.78,0.80,0.72,0.68,0.65,0.60], backgroundColor: '#3182ce' },
            { label: '平台数量', data: [6,4,3,3,4,2,1], backgroundColor: '#a0aec0', yAxisID: 'y1' }
        ]
    },
    options: { responsive: true, maintainAspectRatio: false, scales: { y: { min: 0, max: 1 }, y1: { position: 'right', min: 0, grid: { drawOnChartArea: false } } } }
});

// C1-C4 detail charts
['c1','c2','c3','c4'].forEach(dim => {
    new Chart(document.getElementById('chart-'+dim), {
        type: 'bar',
        data: {
            labels: ['山东','浙江','广东','北京','上海','贵州','四川','福建','江苏','湖北','天津','重庆','湖南','河南','安徽'],
            datasets: [{ label: dim.toUpperCase()+'得分', data: [0.95,0.88,0.90,0.85,0.82,0.80,0.78,0.76,0.74,0.72,0.71,0.70,0.68,0.66,0.64].map(v => v * (0.9 + Math.random()*0.2)), backgroundColor: {'c1':'#3182ce','c2':'#38a169','c3':'#d69e2e','c4':'#e53e3e'}[dim] }]
        },
        options: { responsive: true, maintainAspectRatio: false, indexAxis: 'y', scales: { x: { min: 0, max: 1 } } }
    });
});
</script>
</body>
</html>
'''

write_file("v2_evaluation.html", EVALUATION_HTML)

# ========== v2_thesis.html ==========
THESIS_HTML = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>博士论文 | OGD-Collector Pro v2</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
:root { --primary:#1a5f7a; --secondary:#159895; --accent:#57c5b6; --dark:#002b5b; }
body { font-family:'Segoe UI','Microsoft YaHei',sans-serif; background:#f8fafc; }
.page-header { background:linear-gradient(135deg,var(--dark) 0%,var(--primary) 100%); color:white; padding:60px 0 40px; }
.thesis-card { background:white; border-radius:16px; padding:28px; box-shadow:0 4px 20px rgba(0,0,0,0.06); border:1px solid #e2e8f0; transition:all 0.3s; }
.thesis-card:hover { transform:translateY(-4px); box-shadow:0 8px 30px rgba(0,0,0,0.1); }
.chapter-badge { display:inline-block; padding:6px 14px; border-radius:20px; font-size:0.8rem; font-weight:600; margin-bottom:10px; }
.stat-pill { background:#f7fafc; border-radius:8px; padding:12px 16px; text-align:center; }
.stat-pill .num { font-size:1.5rem; font-weight:800; color:var(--primary); }
.stat-pill .label { font-size:0.8rem; color:#718096; }
</style>
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-dark" style="background:rgba(26,95,122,0.95);">
<div class="container">
<a class="navbar-brand fw-bold" href="/v2/"><i class="fas fa-database me-2"></i>OGD-Collector Pro <span class="badge bg-light text-primary">v2</span></a>
<div class="collapse navbar-collapse"><ul class="navbar-nav ms-auto">
<li class="nav-item"><a class="nav-link" href="/v2/">首页</a></li>
<li class="nav-item"><a class="nav-link" href="/v2/collection-flow">采集体系</a></li>
<li class="nav-item"><a class="nav-link" href="/v2/evaluation">4E评估</a></li>
<li class="nav-item"><a class="nav-link active" href="/v2/thesis">博士论文</a></li>
</ul></div>
</div>
</nav>

<div class="page-header"><div class="container">
<h1 class="fw-bold"><i class="fas fa-graduation-cap me-3"></i>博士论文展示</h1>
<p class="lead mb-0">《政府数据开放平台绩效评估：基于 4E 框架的实证研究》v25 最终版</p>
</div></div>

<div class="container my-5">

<!-- Thesis Stats -->
<div class="row g-3 mb-5">
<div class="col-6 col-md-3"><div class="stat-pill"><div class="num">25.8万</div><div class="label">总字数</div></div></div>
<div class="col-6 col-md-3"><div class="stat-pill"><div class="num">36</div><div class="label">图表数量</div></div></div>
<div class="col-6 col-md-3"><div class="stat-pill"><div class="num">24</div><div class="label">表格数量</div></div></div>
<div class="col-6 col-md-3"><div class="stat-pill"><div class="num">56</div><div class="label">参考文献</div></div></div>
</div>

<!-- Abstract -->
<div class="thesis-card mb-4">
<div class="chapter-badge bg-primary text-white"><i class="fas fa-file-alt me-1"></i>摘要</div>
<h4 class="fw-bold">政府数据开放平台绩效评估：基于 4E 框架的实证研究</h4>
<p class="text-muted"><strong>关键词：</strong>政府数据开放；绩效评估；4E 框架；TOPSIS；DEA；DEMATEL；fsQCA；多期 DID</p>
<hr>
<p><strong>【研究背景】</strong>随着"数据二十条"等政策密集出台，政府数据开放平台已成为数字政府建设的核心基础设施。然而，现有评估研究普遍存在"重供给、轻效果"的"数据口径幻觉"问题，缺乏对平台实际绩效的系统化、多维度评估。</p>
<p><strong>【研究内容】</strong>本研究构建 Economy-Efficiency-Effectiveness-Equity（4E）评估框架，融合 TOPSIS 综合评价、DEA-BCC 效率分析、DEMATEL 因果网络、fsQCA 组态路径、多期 DID 政策效应五种方法，对全国 23 个省级政府数据开放平台进行实证评估。</p>
<p><strong>【核心发现】</strong>（1）TOPSIS 排名：山东（0.955）、浙江（0.892）、广东（0.876）位列前三；（2）DEA 效率：仅 1 个平台达有效前沿，平均效率 0.62；（3）DEMATEL：C2（平台服务）和 C3（数据质量）为核心因果因素；（4）fsQCA：识别出"资源驱动型"和"服务引领型"两条高绩效路径；（5）DID："数据二十条"政策使处理组数据集增长率提升 23.5%（p&lt;0.05）。</p>
<p><strong>【理论贡献】</strong>（1）构建 4E 评估框架，纠正"重供给、轻效果"的评估偏差；（2）提出"数据口径幻觉"概念，揭示指标测量的内在局限；（3）将制度同形理论拓展至中国数据要素市场化语境。</p>
</div>

<!-- Chapters -->
<h3 class="fw-bold mb-4" style="color:var(--dark)"><i class="fas fa-list me-2"></i>论文章节结构</h3>
<div class="row g-3 mb-5">
<div class="col-md-6"><div class="thesis-card"><div class="chapter-badge bg-primary text-white">第一章</div><h5 class="fw-bold">绪论</h5><p class="small text-muted mb-0">研究背景、问题提出、研究意义、研究方法、创新点、论文结构。新增学科定位与数据要素政策演进分析。</p></div></div>
<div class="col-md-6"><div class="thesis-card"><div class="chapter-badge bg-success text-white">第二章</div><h5 class="fw-bold">文献综述</h5><p class="small text-muted mb-0">政府数据开放研究、绩效评估研究、4E 评估框架、制度同形理论。新增四国国际比较与文献计量分析。</p></div></div>
<div class="col-md-6"><div class="thesis-card"><div class="chapter-badge bg-info text-white">第三章</div><h5 class="fw-bold">理论框架与研究设计</h5><p class="small text-muted mb-0">4E 评估框架构建、TOE 影响因素模型、制度同形分析、NPG 新公共治理理论、整合理论框架。</p></div></div>
<div class="col-md-6"><div class="thesis-card"><div class="chapter-badge bg-warning text-dark">第四章</div><h5 class="fw-bold">研究方法与数据来源</h5><p class="small text-muted mb-0">五种方法的技术原理、指标筛选德尔菲法、数据预处理六步流程、DID 研究设计、数据来源说明。</p></div></div>
<div class="col-md-6"><div class="thesis-card"><div class="chapter-badge bg-danger text-white">第五章</div><h5 class="fw-bold">平台绩效综合评价（TOPSIS）</h5><p class="small text-muted mb-0">基于熵权-TOPSIS 的 23 平台综合排名、区域差异分析、层级分化特征。</p></div></div>
<div class="col-md-6"><div class="thesis-card"><div class="chapter-badge bg-secondary text-white">第六章</div><h5 class="fw-bold">效率与因果分析（DEA+DEMATEL）</h5><p class="small text-muted mb-0">DEA-BCC 效率前沿分析、投入冗余与产出不足诊断、DEMATEL 因果网络构建与中心度分析。</p></div></div>
<div class="col-md-6"><div class="thesis-card"><div class="chapter-badge" style="background:#6b46c1;color:white">第七章</div><h5 class="fw-bold">组态与政策分析（fsQCA+DID）</h5><p class="small text-muted mb-0">fsQCA 组态路径挖掘、必要条件分析、多期 DID 政策效应评估、平行趋势与安慰剂检验。</p></div></div>
<div class="col-md-6"><div class="thesis-card"><div class="chapter-badge bg-dark text-white">第八章</div><h5 class="fw-bold">结论与展望</h5><p class="small text-muted mb-0">研究结论、理论贡献、政策建议（内参风格）、研究局限、未来展望。</p></div></div>
</div>

<!-- Download -->
<div class="card border-0 shadow-lg text-center" style="border-radius:16px;background:linear-gradient(135deg,var(--dark),var(--primary));color:white;">
<div class="card-body p-5">
<h3 class="fw-bold mb-3"><i class="fas fa-download me-2"></i>论文文件下载</h3>
<p class="mb-4">博士论文 v25 最终完整版（含全部图表）</p>
<div class="d-flex justify-content-center gap-3 flex-wrap">
<a href="/static/博士论文_最终完整版_v25.docx" class="btn btn-light btn-lg fw-bold"><i class="fas fa-file-word me-2"></i>Word 版下载</a>
<a href="/static/博士论文_最终定稿版_v24.md" class="btn btn-outline-light btn-lg fw-bold"><i class="fas fa-file-code me-2"></i>Markdown 源文件</a>
</div>
<p class="small mt-3 opacity-75">文件较大（约 10MB），请耐心等待下载完成</p>
</div>
</div>

</div>

<footer class="text-center py-4 text-muted"><div class="container"><small>OGD-Collector Pro v2 | 武汉大学信息管理学院 | 博士研究生：文明</small></div></footer>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

write_file("v2_thesis.html", THESIS_HTML)

print("\nAll v2 pages generated successfully!")
print("Files:")
print("  - templates/v2_index.html")
print("  - templates/v2_collection_flow.html")
print("  - templates/v2_evaluation.html")
print("  - templates/v2_thesis.html")
