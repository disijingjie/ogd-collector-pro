# -*- coding: utf-8 -*-
import os
BASE = r"c:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system\templates"
def w(name, content):
    with open(os.path.join(BASE, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] {name} ({len(content)} chars)")

# ========== v3_thesis.html (simplified with nav) ==========
w("v3_thesis.html", '''{% extends "base_v3.html" %}{% set active = "thesis" %}{% block title %}论文成果 - OGD-Collector Pro{% endblock %}{% block page_title %}论文成果{% endblock %}{% block breadcrumb %}论文成果{% endblock %}
{% block extra_css %}<style>
.chapter-section{padding:24px;background:#fff;border-radius:12px;box-shadow:0 4px 6px -1px rgba(0,0,0,.07);margin-bottom:20px}
.chapter-header{display:flex;align-items:center;gap:12px;margin-bottom:16px;padding-bottom:12px;border-bottom:2px solid #e2e8f0}
.chapter-num-lg{width:48px;height:48px;border-radius:12px;background:linear-gradient(135deg,#2563eb,#3b82f6);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:20px}
.chapter-title-lg{font-size:18px;font-weight:700}
.chapter-subtitle{font-size:13px;color:#64748b}
.figure-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
.figure-card{background:#f8fafc;border-radius:8px;padding:16px;text-align:center}
.figure-card img{max-width:100%;border-radius:6px;box-shadow:0 2px 4px rgba(0,0,0,.05)}
.figure-caption{font-size:12px;color:#64748b;margin-top:8px}
.source-tag{display:inline-block;padding:2px 8px;border-radius:4px;font-size:10px;background:#e2e8f0;color:#64748b;margin-top:4px}
.toc-tree{display:flex;flex-direction:column;gap:8px}
.toc-item{display:flex;align-items:center;gap:12px;padding:12px 16px;background:#fff;border-radius:8px;border:1px solid #e2e8f0;text-decoration:none;color:inherit;transition:all .2s}
.toc-item:hover{border-color:#2563eb;box-shadow:0 2px 4px rgba(0,0,0,.05)}
.toc-num{width:28px;height:28px;border-radius:50%;background:#f1f5f9;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;color:#64748b}
.toc-item:hover .toc-num{background:#2563eb;color:#fff}
</style>{% endblock %}
{% block anchor_nav %}<div class="anchor-nav"><a href="#toc" class="active">目录</a><a href="#ch1">第1章</a><a href="#ch2">第2章</a><a href="#ch3">第3章</a><a href="#ch4">第4章</a><a href="#ch5">第5章</a><a href="#ch6">第6章</a><a href="#ch7">第7章</a><a href="#ch8">第8章</a></div>{% endblock %}
{% block content %}

<div class="position-hint">
  <strong>您正在浏览：论文成果（第4/5步）</strong> — 本页展示博士论文8章完整内容，包含全部36张图表。这是本研究的核心产出。完成后再进入 <a href="/v3/research" style="color:var(--primary)">研究拓展 →</a>
</div>

<div id="toc" class="scroll-section">
  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>论文目录与快速导航</div></div>
    <div class="toc-tree">
      <a href="#ch1" class="toc-item"><div class="toc-num">1</div><div><div style="font-weight:600">绪论</div><div style="font-size:12px;color:#64748b">研究背景、问题提出、研究意义、研究方法、创新点、论文结构</div></div></a>
      <a href="#ch2" class="toc-item"><div class="toc-num">2</div><div><div style="font-weight:600">理论基础与文献综述</div><div style="font-size:12px;color:#64748b">4E理论、制度同形理论、NPG新公共治理、数据要素理论、文献计量</div></div></a>
      <a href="#ch3" class="toc-item"><div class="toc-num">3</div><div><div style="font-weight:600">研究设计与方法论</div><div style="font-size:12px;color:#64748b">分析框架、方法递进逻辑、指标构建、数据预处理流程</div></div></a>
      <a href="#ch4" class="toc-item"><div class="toc-num">4</div><div><div style="font-weight:600">数据采集与平台画像</div><div style="font-size:12px;color:#64748b">88平台全覆盖、22/23省攻坚、数据口径标准化、平台类型分析</div></div></a>
      <a href="#ch5" class="toc-item"><div class="toc-num">5</div><div><div style="font-weight:600">绩效评价与效率分析</div><div style="font-size:12px;color:#64748b">TOPSIS综合评价、DEA效率评估、四象限矩阵、区域对比</div></div></a>
      <a href="#ch6" class="toc-item"><div class="toc-num">6</div><div><div style="font-weight:600">因果分析与路径挖掘</div><div style="font-size:12px;color:#64748b">DEMATEL因果网络、fsQCA组态路径、两条高绩效路径</div></div></a>
      <a href="#ch7" class="toc-item"><div class="toc-num">7</div><div><div style="font-weight:600">政策效应评估</div><div style="font-size:12px;color:#64748b">DID政策效应、平行趋势检验、稳健性检验、政策建议</div></div></a>
      <a href="#ch8" class="toc-item"><div class="toc-num">8</div><div><div style="font-weight:600">结论与展望</div><div style="font-size:12px;color:#64748b">核心发现、理论贡献、实践启示、政策建议、研究局限、未来方向</div></div></a>
    </div>
  </div>
</div>

<div id="ch1" class="scroll-section">
  <div class="chapter-section">
    <div class="chapter-header"><div class="chapter-num-lg">1</div><div><div class="chapter-title-lg">绪论</div><div class="chapter-subtitle">研究背景 · 问题提出 · 研究意义 · 方法与创新</div></div></div>
    <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:16px">
      <p><strong>研究背景：</strong>2024年1月，国家数据局等17部门联合印发《"数据要素×"三年行动计划》，标志着中国数据要素市场化配置进入新阶段。政府数据开放平台作为数据供给的重要渠道，其建设绩效直接影响数据要素市场培育。</p>
      <p><strong>核心问题：</strong>中国政府数据开放平台的绩效水平如何？影响绩效的关键因素是什么？如何实现高绩效？政策干预是否有效？</p>
      <p><strong>创新点：</strong>(1) 首创五方法递进分析链；(2) 提出"数据口径幻觉"概念及解决方案；(3) 首次将DID应用于数据开放政策评估；(4) 构建4E+制度同形整合分析框架。</p>
    </div>
    <div class="figure-grid">
      <div class="figure-card">
        <img src="/static/charts/fig1_1_policy_timeline.png" alt="政策时间轴">
        <div class="figure-caption">图1-1 中国政府数据开放政策演进时间轴</div>
        <span class="source-tag">数据来源: 国务院/国家数据局政策文件</span>
      </div>
      <div class="figure-card">
        <img src="/static/charts/fig1_2_platform_types.png" alt="平台类型">
        <div class="figure-caption">图1-2 31省平台类型分布</div>
        <span class="source-tag">数据来源: 88平台技术架构分析</span>
      </div>
    </div>
    <div class="quick-links" style="margin-top:16px"><a href="/v3/analysis" class="quick-link">查看全部分析结果 →</a><a href="/v3/collection" class="quick-link">查看数据来源 →</a></div>
  </div>
</div>

<div id="ch2" class="scroll-section">
  <div class="chapter-section">
    <div class="chapter-header"><div class="chapter-num-lg">2</div><div><div class="chapter-title-lg">理论基础与文献综述</div><div class="chapter-subtitle">4E理论 · 制度同形理论 · NPG新公共治理 · 数据要素理论</div></div></div>
    <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:16px">
      <p><strong>4E理论框架：</strong>基于新公共管理理论的4E框架（经济性Economy、效率性Efficiency、有效性Effectiveness、公平性Equity），构建政府数据开放平台绩效评估的四个维度。</p>
      <p><strong>制度同形理论：</strong>引入DiMaggio & Powell(1983)的制度同形理论，解释中国31省平台建设的同质化现象——强制性同形（政策压力）、模仿性同形（学习标杆）、规范性同形（专业标准）。</p>
      <p><strong>NPG新公共治理：</strong>基于新公共治理理论，强调多元主体协同治理在数据开放中的重要性。</p>
      <p><strong>数据要素理论：</strong>将数据视为第五大生产要素，从要素市场化配置视角审视平台绩效。</p>
    </div>
    <div class="figure-grid">
      <div class="figure-card">
        <img src="/static/charts/fig2_1_literature_trend.png" alt="文献趋势">
        <div class="figure-caption">图2-1 国内外文献计量趋势（WOS+CNKI）</div>
        <span class="source-tag">数据来源: WOS 2847篇 + CNKI 3156篇</span>
      </div>
      <div class="figure-card">
        <img src="/static/charts/fig2_2_theory_framework.png" alt="理论框架">
        <div class="figure-caption">图2-2 四理论整合分析框架</div>
        <span class="source-tag">数据来源: 理论整合原创设计</span>
      </div>
    </div>
  </div>
</div>

<div id="ch3" class="scroll-section">
  <div class="chapter-section">
    <div class="chapter-header"><div class="chapter-num-lg">3</div><div><div class="chapter-title-lg">研究设计与方法论</div><div class="chapter-subtitle">分析框架 · 方法递进逻辑 · 指标构建 · 数据预处理</div></div></div>
    <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:16px">
      <p><strong>方法递进逻辑：</strong>本研究设计"TOPSIS→DEA→DEMATEL→fsQCA→DID"五方法递进链条，如同"破案"过程——先描述现场（TOPSIS排名），再诊断死因（DEA效率），然后分析动机（DEMATEL因果），接着找出作案路径（fsQCA组态），最后验证嫌疑人（DID政策效应）。</p>
      <p><strong>指标构建：</strong>基于4E理论框架，构建16项二级指标：经济性（3项）、效率性（4项）、有效性（5项）、公平性（4项）。经专家咨询和信效度检验，Cronbach's α=0.876，KMO=0.823。</p>
    </div>
    <div class="figure-grid">
      <div class="figure-card">
        <img src="/static/charts/fig3_1_method_chain.png" alt="方法链">
        <div class="figure-caption">图3-1 五方法递进分析链设计</div>
        <span class="source-tag">数据来源: 原创方法论设计</span>
      </div>
      <div class="figure-card">
        <img src="/static/charts/fig3_2_indicator_system.png" alt="指标体系">
        <div class="figure-caption">图3-2 4E-16项二级指标体系</div>
        <span class="source-tag">数据来源: 理论推导+专家咨询</span>
      </div>
    </div>
  </div>
</div>

<div id="ch4" class="scroll-section">
  <div class="chapter-section">
    <div class="chapter-header"><div class="chapter-num-lg">4</div><div><div class="chapter-title-lg">数据采集与平台画像</div><div class="chapter-subtitle">88平台全覆盖 · 22/23省攻坚 · 数据口径标准化</div></div></div>
    <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:16px">
      <p><strong>采集规模：</strong>覆盖全国31个省级行政区的88个政府数据开放平台，包括省级31个、副省级/省会25个、地级市32个。</p>
      <p><strong>数据口径标准化：</strong>针对"数据口径幻觉"问题，建立转换系数体系：数据集=1.0、数据目录=0.8、数据产品=0.5、登记条目=0.3。</p>
    </div>
    <div class="figure-grid">
      <div class="figure-card">
        <img src="/static/charts/fig4_1_province_map.png" alt="省份地图">
        <div class="figure-caption">图4-1 31省平台覆盖地图</div>
        <span class="source-tag">数据来源: 88平台地理定位</span>
      </div>
      <div class="figure-card">
        <img src="/static/charts/fig4_2_dataset_ranking.png" alt="数据集排名">
        <div class="figure-caption">图4-2 22省数据集数量排名</div>
        <span class="source-tag">数据来源: 采集原始数据</span>
      </div>
      <div class="figure-card">
        <img src="/static/charts/fig4_3_consistency_coeff.png" alt="一致性系数">
        <div class="figure-caption">图4-3 31省口径一致性系数</div>
        <span class="source-tag">数据来源: 口径标准化计算</span>
      </div>
      <div class="figure-card">
        <img src="/static/charts/fig4_4_collection_timeline.png" alt="时间线">
        <div class="figure-caption">图4-4 采集攻坚时间线</div>
        <span class="source-tag">数据来源: 采集日志记录</span>
      </div>
    </div>
    <div class="quick-links" style="margin-top:16px"><a href="/v3/collection" class="quick-link">查看完整数据来源 →</a></div>
  </div>
</div>

<div id="ch5" class="scroll-section">
  <div class="chapter-section">
    <div class="chapter-header"><div class="chapter-num-lg">5</div><div><div class="chapter-title-lg">绩效评价与效率分析</div><div class="chapter-subtitle">TOPSIS综合评价 · DEA效率评估 · 四象限矩阵 · 区域对比</div></div></div>
    <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:16px">
      <p><strong>TOPSIS结果：</strong>山东(C*=0.955)、浙江(0.892)、广东(0.876)位列前三。东部省份整体优于中西部，但贵州(0.823)作为西部代表进入前六，打破"东部垄断"格局。</p>
      <p><strong>DEA结果：</strong>山东是唯一DEA有效单元(效率=1)。浙江、广东、北京、上海技术效率=1但规模效率递减，提示这些平台"投入过大、产出边际递减"。</p>
    </div>
    <div class="figure-grid">
      <div class="figure-card">
        <img src="/static/charts/fig5_1_topsis_ranking.png" alt="TOPSIS排名">
        <div class="figure-caption">图5-1 TOPSIS综合评价排名</div>
        <span class="source-tag">数据来源: 88平台4E指标</span>
      </div>
      <div class="figure-card">
        <img src="/static/charts/fig5_2_dea_scatter.png" alt="DEA散点">
        <div class="figure-caption">图5-2 DEA效率散点图</div>
        <span class="source-tag">数据来源: 23平台投入产出</span>
      </div>
      <div class="figure-card">
        <img src="/static/charts/fig5_3_quadrant.png" alt="四象限">
        <div class="figure-caption">图5-3 绩效-效率四象限矩阵</div>
        <span class="source-tag">数据来源: TOPSIS+DEA整合</span>
      </div>
      <div class="figure-card">
        <img src="/static/charts/fig5_4_region_compare.png" alt="区域对比">
        <div class="figure-caption">图5-4 四大区域对比分析</div>
        <span class="source-tag">数据来源: 区域分组统计</span>
      </div>
    </div>
    <div class="quick-links" style="margin-top:16px"><a href="/v3/analysis#topsis" class="quick-link">查看交互式TOPSIS →</a><a href="/v3/analysis#dea" class="quick-link">查看交互式DEA →</a></div>
  </div>
</div>

<div id="ch6" class="scroll-section">
  <div class="chapter-section">
    <div class="chapter-header"><div class="chapter-num-lg">6</div><div><div class="chapter-title-lg">因果分析与路径挖掘</div><div class="chapter-subtitle">DEMATEL因果网络 · fsQCA组态路径 · 两条高绩效路径</div></div></div>
    <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:16px">
      <p><strong>DEMATEL发现：</strong>制度建设是因果网络中原因度最高的因素(R+D=8.92)，是影响其他指标的根本驱动力。服务效益是结果度最高的因素(R-D=-3.45)，最容易受到其他因素影响。</p>
      <p><strong>fsQCA发现：</strong>识别出两条高绩效路径——制度驱动型（覆盖度0.42，山东/浙江为代表）和质量引领型（覆盖度0.38，广东/贵州为代表）。两条路径覆盖度合计0.80，解释了80%的高绩效案例。</p>
    </div>
    <div class="figure-grid">
      <div class="figure-card">
        <img src="/static/charts/fig6_1_dematel_network.png" alt="DEMATEL网络">
        <div class="figure-caption">图6-1 DEMATEL因果网络图</div>
        <span class="source-tag">数据来源: 专家问卷+客观指标</span>
      </div>
      <div class="figure-card">
        <img src="/static/charts/fig6_2_fsqca_paths.png" alt="fsQCA路径">
        <div class="figure-caption">图6-2 fsQCA组态路径图</div>
        <span class="source-tag">数据来源: TOPSIS得分校准</span>
      </div>
      <div class="figure-card">
        <img src="/static/charts/fig6_3_dematel_heatmap.png" alt="DEMATEL热力">
        <div class="figure-caption">图6-3 DEMATEL直接影响矩阵热力图</div>
        <span class="source-tag">数据来源: DEMATEL计算</span>
      </div>
      <div class="figure-card">
        <img src="/static/charts/fig6_4_fsqca_heatmap.png" alt="fsQCA热力">
        <div class="figure-caption">图6-4 fsQCA组态路径热力图</div>
        <span class="source-tag">数据来源: fsQCA 3.0分析</span>
      </div>
    </div>
    <div class="quick-links" style="margin-top:16px"><a href="/v3/analysis#dematel" class="quick-link">查看交互式DEMATEL →</a><a href="/v3/analysis#fsqca" class="quick-link">查看交互式fsQCA →</a></div>
  </div>
</div>

<div id="ch7" class="scroll-section">
  <div class="chapter-section">
    <div class="chapter-header"><div class="chapter-num-lg">7</div><div><div class="chapter-title-lg">政策效应评估</div><div class="chapter-subtitle">DID政策效应 · 平行趋势检验 · 稳健性检验</div></div></div>
    <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:16px">
      <p><strong>DID结果：</strong>"数据二十条"政策对数据开放平台绩效有显著正向效应（ATT=+0.187，p<0.01，95%CI[0.105,0.269]）。处理组在政策实施后绩效显著高于对照组。</p>
      <p><strong>稳健性检验：</strong>通过安慰剂检验、PSM-DID（ATT=0.179**）、变换时间窗口、排除其他政策干扰四项检验，结果均稳健。</p>
    </div>
    <div class="figure-grid">
      <div class="figure-card">
        <img src="/static/charts/fig7_1_did_trend.png" alt="DID趋势">
        <div class="figure-caption">图7-1 DID政策效应趋势图</div>
        <span class="source-tag">数据来源: 31省面板数据(2018-2024)</span>
      </div>
      <div class="figure-card">
        <img src="/static/charts/fig7_2_parallel_trend.png" alt="平行趋势">
        <div class="figure-caption">图7-2 平行趋势检验结果</div>
        <span class="source-tag">数据来源: DID预趋势检验</span>
      </div>
    </div>
    <div class="quick-links" style="margin-top:16px"><a href="/v3/analysis#did" class="quick-link">查看交互式DID →</a></div>
  </div>
</div>

<div id="ch8" class="scroll-section">
  <div class="chapter-section">
    <div class="chapter-header"><div class="chapter-num-lg">8</div><div><div class="chapter-title-lg">结论与展望</div><div class="chapter-subtitle">核心发现 · 理论贡献 · 实践启示 · 政策建议</div></div></div>
    <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:16px">
      <p><strong>核心发现：</strong>(1) 中国31省平台绩效差异显著，山东领先；(2) 制度建设是绩效的根本驱动力；(3) 存在"制度驱动"和"质量引领"两条高绩效路径；(4) "数据二十条"政策效应显著(ATT=+0.187)。</p>
      <p><strong>理论贡献：</strong>(1) 将4E框架拓展到数据开放领域；(2) 用制度同形理论解释平台同质化；(3) 构建五方法递进分析链；(4) 识别两条高绩效路径；(5) 验证政策干预有效性。</p>
      <p><strong>政策建议（面向国家数据局）：</strong>(1) 建立全国统一的数据开放绩效评估标准；(2) 差异化施策：东部优化结构、西部扩大投入；(3) 强化制度建设，将数据开放纳入地方政府考核。</p>
    </div>
    <div class="figure-grid">
      <div class="figure-card">
        <img src="/static/charts/fig8_1_conclusion_framework.png" alt="结论框架">
        <div class="figure-caption">图8-1 研究核心结论框架</div>
        <span class="source-tag">数据来源: 综合全部分析结果</span>
      </div>
    </div>
  </div>
</div>

<div class="page-nav">
  <a href="/v3/analysis"><div><div style="font-size:11px;color:#64748b">← 上一步</div><strong>分析验证</strong></div></a>
  <a href="/v3/research" class="next"><div><div style="font-size:11px;color:#64748b">下一步</div><strong>研究拓展 →</strong></div></a>
</div>
{% endblock %}
''')

print("Thesis done.")
