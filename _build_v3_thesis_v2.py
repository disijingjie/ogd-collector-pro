content = '''{% extends "base_v3.html" %}{% set active = "thesis" %}{% block title %}论文成果 - OGD-Collector Pro{% endblock %}{% block page_title %}论文成果{% endblock %}{% block breadcrumb %}论文成果{% endblock %}
{% block anchor_nav %}<div class="anchor-nav"><a href="#overview" class="active">论文概览</a><a href="#findings">核心发现</a><a href="#chapters">章节导航</a><a href="#figures">图表索引</a></div>{% endblock %}
{% block content %}

<!-- 第一屏：论文概览 -->
<div id="overview" class="scroll-section">
  <div class="card">
    <div style="display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start">
      <div style="flex:1;min-width:300px">
        <div style="font-size:22px;font-weight:800;color:#1e293b;margin-bottom:8px">中国政府数据开放平台绩效评估研究</div>
        <div style="font-size:14px;color:#64748b;line-height:1.8;margin-bottom:12px">
          基于4E理论框架与多方法融合视角的实证分析<br>
          ——以31个省级政府数据开放平台为例
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px">
          <span class="badge" style="background:#dbeafe;color:#1d4ed8">博士论文</span>
          <span class="badge" style="background:#d1fae5;color:#065f46">武汉大学</span>
          <span class="badge" style="background:#fef3c7;color:#92400e">信息资源管理</span>
          <span class="badge" style="background:#fce7f3;color:#9d174d">2026年4月</span>
        </div>
        <div style="padding:12px;background:#f0f9ff;border-radius:8px;border-left:4px solid #2563eb">
          <div style="font-weight:700;margin-bottom:6px;color:#1e40af">核心结论</div>
          <div style="font-size:13px;color:#475569;line-height:1.8">
            ① 中国政府数据开放平台绩效呈"东高西低"格局，山东、浙江、广东位列前三；<br>
            ② 平台绩效差异主要由制度建设和数据质量双轮驱动；<br>
            ③ "数据二十条"政策对平台绩效产生显著正向效应（ATT=0.187***）。
          </div>
        </div>
      </div>
      <div style="min-width:200px">
        <div class="stats-grid" style="grid-template-columns:1fr 1fr;gap:8px">
          <div class="stat-card" style="padding:12px"><div class="stat-value" style="font-size:24px">8</div><div class="stat-label" style="font-size:11px">章节</div></div>
          <div class="stat-card" style="padding:12px"><div class="stat-value" style="font-size:24px">36</div><div class="stat-label" style="font-size:11px">图表</div></div>
          <div class="stat-card" style="padding:12px"><div class="stat-value" style="font-size:24px">24</div><div class="stat-label" style="font-size:11px">表格</div></div>
          <div class="stat-card" style="padding:12px"><div class="stat-value" style="font-size:24px">286</div><div class="stat-label" style="font-size:11px">参考文献</div></div>
        </div>
      </div>
    </div>
  </div>

  <div class="card">
    <div class="card-header"><div class="card-title"><span class="icon"></span>论文章节结构</div></div>
    <div class="chapter-tree">
      <div class="chapter-node" onclick="location.href='#ch1'">
        <div class="chapter-num">1</div>
        <div class="chapter-info">
          <h4>绪论</h4>
          <p>研究背景、问题提出、研究意义、研究内容与方法、创新点</p>
          <div class="chapter-tags"><span class="chapter-tag">研究背景</span><span class="chapter-tag">问题提出</span><span class="chapter-tag">创新点</span></div>
        </div>
      </div>
      <div class="chapter-node" onclick="location.href='#ch2'">
        <div class="chapter-num">2</div>
        <div class="chapter-info">
          <h4>理论基础与文献综述</h4>
          <p>4E理论框架、制度同形理论、NPG新公共治理、文献计量分析</p>
          <div class="chapter-tags"><span class="chapter-tag">4E理论</span><span class="chapter-tag">制度同形</span><span class="chapter-tag">文献计量</span></div>
        </div>
      </div>
      <div class="chapter-node" onclick="location.href='#ch3'">
        <div class="chapter-num">3</div>
        <div class="chapter-info">
          <h4>研究设计</h4>
          <p>分析框架构建、五方法递进逻辑、指标体系设计、数据来源与采集</p>
          <div class="chapter-tags"><span class="chapter-tag">TOPSIS</span><span class="chapter-tag">DEA</span><span class="chapter-tag">DEMATEL</span><span class="chapter-tag">fsQCA</span><span class="chapter-tag">DID</span></div>
        </div>
      </div>
      <div class="chapter-node" onclick="location.href='#ch4'">
        <div class="chapter-num">4</div>
        <div class="chapter-info">
          <h4>数据采集与平台画像</h4>
          <p>88平台全覆盖采集、平台功能特征分析、数据质量评估</p>
          <div class="chapter-tags"><span class="chapter-tag">88平台</span><span class="chapter-tag">平台画像</span><span class="chapter-tag">数据质量</span></div>
        </div>
      </div>
      <div class="chapter-node" onclick="location.href='#ch5'">
        <div class="chapter-num">5</div>
        <div class="chapter-info">
          <h4>综合评价：TOPSIS与DEA</h4>
          <p>4E指标测度、TOPSIS综合排名、DEA效率分析、效率-排名二维分类</p>
          <div class="chapter-tags"><span class="chapter-tag">TOPSIS排名</span><span class="chapter-tag">DEA效率</span><span class="chapter-tag">二维矩阵</span></div>
        </div>
      </div>
      <div class="chapter-node" onclick="location.href='#ch6'">
        <div class="chapter-num">6</div>
        <div class="chapter-info">
          <h4>因果挖掘：DEMATEL与fsQCA</h4>
          <p>因果关系网络构建、核心驱动因素识别、高绩效路径分析</p>
          <div class="chapter-tags"><span class="chapter-tag">因果网络</span><span class="chapter-tag">组态分析</span><span class="chapter-tag">路径挖掘</span></div>
        </div>
      </div>
      <div class="chapter-node" onclick="location.href='#ch7'">
        <div class="chapter-num">7</div>
        <div class="chapter-info">
          <h4>政策效应：DID评估</h4>
          <p>"数据二十条"政策背景、双重差分设计、平行趋势检验、稳健性检验</p>
          <div class="chapter-tags"><span class="chapter-tag">政策评估</span><span class="chapter-tag">因果推断</span><span class="chapter-tag">稳健性</span></div>
        </div>
      </div>
      <div class="chapter-node" onclick="location.href='#ch8'">
        <div class="chapter-num">8</div>
        <div class="chapter-info">
          <h4>结论与展望</h4>
          <p>主要结论、理论贡献、实践启示、研究局限、未来展望</p>
          <div class="chapter-tags"><span class="chapter-tag">理论贡献</span><span class="chapter-tag">实践启示</span><span class="chapter-tag">未来展望</span></div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- 第二屏：核心发现区（基于真实数据的4张图） -->
<div id="findings" class="scroll-section">
  <div class="card-header"><div class="card-title"><span class="icon"></span>核心发现：用数据说话</div></div>

  <div class="card">
    <div style="display:flex;gap:16px;flex-wrap:wrap">
      <div style="flex:1;min-width:300px">
        <div style="font-weight:700;margin-bottom:8px;color:#2563eb">发现1：绩效格局——东部领先，西部追赶</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:12px">
          基于TOPSIS综合评价，山东省以0.955分位居第一，浙江、广东紧随其后。东部地区平台绩效显著高于中西部，呈现出明显的"梯度分布"特征。
        </div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px;font-size:12px;color:#64748b">
          <strong>数据来源：</strong>88个平台标准化元数据 | <strong>样本量：</strong>n=31省 | <strong>方法：</strong>TOPSIS逼近理想解排序法
        </div>
      </div>
      <div style="flex:1;min-width:300px">
        <img src="/static/charts/fig5_1_topsis_ranking.png" style="max-width:100%;border-radius:8px;border:1px solid #e2e8f0" alt="TOPSIS排名">
      </div>
    </div>
  </div>

  <div class="card">
    <div style="display:flex;gap:16px;flex-wrap:wrap">
      <div style="flex:1;min-width:300px">
        <img src="/static/charts/fig5_2_dea_scatter.png" style="max-width:100%;border-radius:8px;border:1px solid #e2e8f0" alt="DEA效率散点图">
      </div>
      <div style="flex:1;min-width:300px">
        <div style="font-weight:700;margin-bottom:8px;color:#059669">发现2：效率差异——整体效率提升空间巨大</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:12px">
          DEA效率分析显示，仅1个平台达到综合效率有效（效率值=1），多数平台存在投入冗余或产出不足。技术效率普遍高于规模效率，说明平台技术能力较好，但资源配置有待优化。
        </div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px;font-size:12px;color:#64748b">
          <strong>数据来源：</strong>4E指标标准化矩阵 | <strong>样本量：</strong>n=15省 | <strong>方法：</strong>DEA-BCC模型
        </div>
      </div>
    </div>
  </div>

  <div class="card">
    <div style="display:flex;gap:16px;flex-wrap:wrap">
      <div style="flex:1;min-width:300px">
        <div style="font-weight:700;margin-bottom:8px;color:#d97706">发现3：因果网络——制度建设是首要驱动因素</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:12px">
          DEMATEL分析揭示了"制度建设→组织领导→数据质量→服务效益→满意度"的因果传导链。制度建设的原因度最高（0.72），是影响平台绩效的根本性因素。
        </div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px;font-size:12px;color:#64748b">
          <strong>数据来源：</strong>专家问卷+平台指标 | <strong>样本量：</strong>n=6因素 | <strong>方法：</strong>DEMATEL决策试验法
        </div>
      </div>
      <div style="flex:1;min-width:300px">
        <img src="/static/charts/fig6_1_dematel_network.png" style="max-width:100%;border-radius:8px;border:1px solid #e2e8f0" alt="DEMATEL因果网络">
      </div>
    </div>
  </div>

  <div class="card">
    <div style="display:flex;gap:16px;flex-wrap:wrap">
      <div style="flex:1;min-width:300px">
        <img src="/static/charts/fig6_2_fsqca_paths.png" style="max-width:100%;border-radius:8px;border:1px solid #e2e8f0" alt="fsQCA路径">
      </div>
      <div style="flex:1;min-width:300px">
        <div style="font-weight:700;margin-bottom:8px;color:#db2777">发现3续：两条高绩效路径</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:12px">
          fsQCA组态分析发现两条高绩效路径：<strong>"制度驱动型"</strong>（制度建设+数据质量+用户参与，一致性0.91）和<strong>"质量引领型"</strong>（组织领导+数据质量+用户参与+技术支撑，一致性0.88）。
        </div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px;font-size:12px;color:#64748b">
          <strong>数据来源：</strong>标准化指标校准值 | <strong>样本量：</strong>n=31省 | <strong>方法：</strong>fsQCA模糊集定性比较分析
        </div>
      </div>
    </div>
  </div>

  <div class="card">
    <div style="display:flex;gap:16px;flex-wrap:wrap">
      <div style="flex:1;min-width:300px">
        <div style="font-weight:700;margin-bottom:8px;color:#7c3aed">发现4：政策效应——"数据二十条"产生显著正向影响</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:12px">
          DID双重差分分析显示，"数据二十条"政策发布后，处理组（出台配套政策省份）的平台绩效显著高于对照组，平均处理效应ATT=0.187（p<0.01）。平行趋势检验和稳健性检验均通过。
        </div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px;font-size:12px;color:#64748b">
          <strong>数据来源：</strong>2018-2023年面板数据 | <strong>样本量：</strong>n=31省×6年 | <strong>方法：</strong>DID双重差分法
        </div>
      </div>
      <div style="flex:1;min-width:300px">
        <img src="/static/charts/fig7_1_did_trend.png" style="max-width:100%;border-radius:8px;border:1px solid #e2e8f0" alt="DID趋势图">
      </div>
    </div>
  </div>
</div>

<!-- 第三屏：全文章节导航（可展开） -->
<div id="chapters" class="scroll-section">
  <div class="card-header"><div class="card-title"><span class="icon"></span>论文章节详细内容</div><div style="font-size:12px;color:#64748b">点击章节标题展开查看该章所有图表</div></div>

  <div class="card" style="margin-bottom:12px">
    <div style="display:flex;align-items:center;gap:12px;cursor:pointer;padding:12px" onclick="toggleSection('ch1-detail', this)">
      <div style="width:32px;height:32px;background:#2563eb;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px">1</div>
      <div style="flex:1"><div style="font-weight:700">第1章 绪论</div><div style="font-size:12px;color:#64748b">研究背景、问题提出、研究意义、创新点</div></div>
      <div style="font-size:12px;color:#94a3b8">▼</div>
    </div>
    <div id="ch1-detail" style="display:none;padding:0 12px 16px 56px;border-top:1px solid #f1f5f9">
      <div style="font-size:13px;color:#64748b;line-height:1.8">
        <p><strong>1.1 研究背景：</strong>数据已成为继土地、劳动力、资本、技术之后的第五大生产要素。政府数据开放平台作为公共数据资源流通的核心枢纽，其建设质量直接影响数字政府治理效能。</p>
        <p><strong>1.2 核心问题：</strong>（1）如何科学评估政府数据开放平台的综合绩效？（2）哪些因素驱动平台绩效差异？（3）数据开放政策是否产生了实质性效果？</p>
        <p><strong>1.3 创新点：</strong>① 构建"4E+五方法"融合评估框架；② 首次将fsQCA引入政府数据开放研究；③ 首次运用DID方法评估数据开放政策效应。</p>
      </div>
    </div>
  </div>

  <div class="card" style="margin-bottom:12px">
    <div style="display:flex;align-items:center;gap:12px;cursor:pointer;padding:12px" onclick="toggleSection('ch2-detail', this)">
      <div style="width:32px;height:32px;background:#059669;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px">2</div>
      <div style="flex:1"><div style="font-weight:700">第2章 理论基础与文献综述</div><div style="font-size:12px;color:#64748b">4E理论、制度同形理论、文献计量分析</div></div>
      <div style="font-size:12px;color:#94a3b8">▼</div>
    </div>
    <div id="ch2-detail" style="display:none;padding:0 12px 16px 56px;border-top:1px solid #f1f5f9">
      <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:12px">
        <p><strong>4E理论框架：</strong>Economy（经济性）、Efficiency（效率性）、Effectiveness（有效性）、Equity（公平性）——源自新公共管理绩效评估理论，本研究将其适配于政府数据开放语境。</p>
        <p><strong>制度同形理论：</strong>DiMaggio & Powell (1983) 提出的强制性同形、模仿性同形、规范性同形三机制，解释了中国政府数据开放平台建设中的"千台一面"现象。</p>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px">
        <div class="chart-container" style="margin:0"><div class="chart-title">图2-1 4E理论框架适配</div>
          <div style="display:flex;flex-direction:column;gap:10px;align-items:center;padding:16px">
            <div style="width:180px;padding:10px;background:linear-gradient(135deg,#2563eb,#3b82f6);color:#fff;border-radius:10px;text-align:center;font-weight:700;font-size:13px">政府数据开放平台绩效</div>
            <div style="font-size:18px;color:#94a3b8">↓</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;width:100%">
              <div style="padding:8px;background:#dbeafe;border-radius:8px;text-align:center"><div style="font-weight:700;color:#1e40af;font-size:12px">经济性</div><div style="font-size:10px;color:#64748b">投入成本控制</div></div>
              <div style="padding:8px;background:#d1fae5;border-radius:8px;text-align:center"><div style="font-weight:700;color:#065f46;font-size:12px">效率性</div><div style="font-size:10px;color:#64748b">投入产出比</div></div>
              <div style="padding:8px;background:#fef3c7;border-radius:8px;text-align:center"><div style="font-weight:700;color:#92400e;font-size:12px">有效性</div><div style="font-size:10px;color:#64748b">目标达成度</div></div>
              <div style="padding:8px;background:#fce7f3;border-radius:8px;text-align:center"><div style="font-weight:700;color:#9d174d;font-size:12px">公平性</div><div style="font-size:10px;color:#64748b">区域均衡度</div></div>
            </div>
          </div>
        </div>
        <div class="chart-container" style="margin:0"><div class="chart-title">图2-2 制度同形三机制</div>
          <div style="display:flex;flex-direction:column;gap:12px;align-items:center;padding:16px">
            <div style="display:flex;gap:16px">
              <div style="text-align:center"><div style="width:70px;height:70px;border-radius:50%;background:#dbeafe;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#1e40af">强制性<br>同形</div><div style="font-size:10px;color:#64748b;margin-top:4px">法规政策驱动</div></div>
              <div style="text-align:center"><div style="width:70px;height:70px;border-radius:50%;background:#d1fae5;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#065f46">模仿性<br>同形</div><div style="font-size:10px;color:#64748b;margin-top:4px">标杆学习效应</div></div>
              <div style="text-align:center"><div style="width:70px;height:70px;border-radius:50%;background:#fef3c7;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#92400e">规范性<br>同形</div><div style="font-size:10px;color:#64748b;margin-top:4px">专业标准趋同</div></div>
            </div>
            <div style="width:100%;padding:10px;background:#f8fafc;border-radius:8px;text-align:center;font-size:12px;color:#64748b">→ 导致平台功能同质化、差异化不足</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="card" style="margin-bottom:12px">
    <div style="display:flex;align-items:center;gap:12px;cursor:pointer;padding:12px" onclick="toggleSection('ch3-detail', this)">
      <div style="width:32px;height:32px;background:#d97706;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px">3</div>
      <div style="flex:1"><div style="font-weight:700">第3章 研究设计</div><div style="font-size:12px;color:#64748b">五方法递进逻辑、指标体系、数据来源</div></div>
      <div style="font-size:12px;color:#94a3b8">▼</div>
    </div>
    <div id="ch3-detail" style="display:none;padding:0 12px 16px 56px;border-top:1px solid #f1f5f9">
      <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:12px">
        <p><strong>五方法递进逻辑：</strong>本研究设计"排名→效率→因果→路径→政策"的五方法递进分析链，实现对平台绩效从"是什么"到"为什么"再到"怎么办"的完整解释。</p>
      </div>
      <div class="chart-container" style="margin:0">
        <div class="chart-title">图3-1 五方法递进分析框架</div>
        <div style="overflow-x:auto"><svg viewBox="0 0 900 150" style="width:100%;min-width:700px">
          <rect x="20" y="25" width="150" height="70" fill="#dbeafe" stroke="#2563eb" stroke-width="2" rx="8"/><text x="95" y="52" text-anchor="middle" font-size="12" font-weight="700" fill="#1e40af">TOPSIS</text><text x="95" y="68" text-anchor="middle" font-size="9" fill="#3b82f6">综合评价排名</text><text x="95" y="82" text-anchor="middle" font-size="8" fill="#64748b">"是什么"</text>
          <rect x="200" y="25" width="150" height="70" fill="#d1fae5" stroke="#059669" stroke-width="2" rx="8"/><text x="275" y="52" text-anchor="middle" font-size="12" font-weight="700" fill="#065f46">DEA</text><text x="275" y="68" text-anchor="middle" font-size="9" fill="#10b981">效率评估</text><text x="275" y="82" text-anchor="middle" font-size="8" fill="#64748b">"效率如何"</text>
          <rect x="380" y="25" width="150" height="70" fill="#fef3c7" stroke="#d97706" stroke-width="2" rx="8"/><text x="455" y="52" text-anchor="middle" font-size="12" font-weight="700" fill="#92400e">DEMATEL</text><text x="455" y="68" text-anchor="middle" font-size="9" fill="#f59e0b">因果关系</text><text x="455" y="82" text-anchor="middle" font-size="8" fill="#64748b">"为什么"</text>
          <rect x="560" y="25" width="150" height="70" fill="#fce7f3" stroke="#db2777" stroke-width="2" rx="8"/><text x="635" y="52" text-anchor="middle" font-size="12" font-weight="700" fill="#9d174d">fsQCA</text><text x="635" y="68" text-anchor="middle" font-size="9" fill="#ec4899">路径挖掘</text><text x="635" y="82" text-anchor="middle" font-size="8" fill="#64748b">"哪条路径"</text>
          <rect x="740" y="25" width="150" height="70" fill="#f3e8ff" stroke="#9333ea" stroke-width="2" rx="8"/><text x="815" y="52" text-anchor="middle" font-size="12" font-weight="700" fill="#7e22ce">DID</text><text x="815" y="68" text-anchor="middle" font-size="9" fill="#a855f7">政策效应</text><text x="815" y="82" text-anchor="middle" font-size="8" fill="#64748b">"政策有效吗"</text>
          <defs><marker id="ar2" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#94a3b8"/></marker></defs>
          <line x1="170" y1="60" x2="200" y2="60" stroke="#94a3b8" stroke-width="2" marker-end="url(#ar2)"/>
          <line x1="350" y1="60" x2="380" y2="60" stroke="#94a3b8" stroke-width="2" marker-end="url(#ar2)"/>
          <line x1="530" y1="60" x2="560" y2="60" stroke="#94a3b8" stroke-width="2" marker-end="url(#ar2)"/>
          <line x1="710" y1="60" x2="740" y2="60" stroke="#94a3b8" stroke-width="2" marker-end="url(#ar2)"/>
          <text x="450" y="130" text-anchor="middle" font-size="11" fill="#64748b">递进逻辑：描述 → 诊断 → 归因 → 处方 → 验证</text>
        </svg></div>
      </div>
    </div>
  </div>

  <div class="card" style="margin-bottom:12px">
    <div style="display:flex;align-items:center;gap:12px;cursor:pointer;padding:12px" onclick="toggleSection('ch4-detail', this)">
      <div style="width:32px;height:32px;background:#db2777;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px">4</div>
      <div style="flex:1"><div style="font-weight:700">第4章 数据采集与平台画像</div><div style="font-size:12px;color:#64748b">88平台全覆盖采集、功能特征分析</div></div>
      <div style="font-size:12px;color:#94a3b8">▼</div>
    </div>
    <div id="ch4-detail" style="display:none;padding:0 12px 16px 56px;border-top:1px solid #f1f5f9">
      <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:12px">
        <p>本章完成了全国31个省级行政区、88个政府数据开放平台的全覆盖采集，建立了包含平台基本信息、功能特征、数据集元数据的标准化数据库。</p>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px">
        <div class="chart-container" style="margin:0"><div class="chart-title">图4-1 平台覆盖地图</div>
          <img src="/static/charts/fig4_1_province_map.png" style="max-width:100%;border-radius:6px" alt="平台覆盖地图">
        </div>
        <div class="chart-container" style="margin:0"><div class="chart-title">图4-2 功能特征分布</div>
          <div style="padding:10px">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px;font-size:12px"><span>数据目录</span><span>98%</span></div><div class="progress-bar"><div class="progress-fill" style="width:98%"></div></div>
            <div style="display:flex;justify-content:space-between;margin:4px 0;font-size:12px"><span>API接口</span><span>65%</span></div><div class="progress-bar"><div class="progress-fill" style="width:65%"></div></div>
            <div style="display:flex;justify-content:space-between;margin:4px 0;font-size:12px"><span>数据可视化</span><span>52%</span></div><div class="progress-bar"><div class="progress-fill" style="width:52%"></div></div>
            <div style="display:flex;justify-content:space-between;margin:4px 0;font-size:12px"><span>用户反馈</span><span>38%</span></div><div class="progress-bar"><div class="progress-fill" style="width:38%"></div></div>
            <div style="display:flex;justify-content:space-between;margin:4px 0;font-size:12px"><span>开发者中心</span><span>28%</span></div><div class="progress-bar"><div class="progress-fill" style="width:28%"></div></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="card" style="margin-bottom:12px">
    <div style="display:flex;align-items:center;gap:12px;cursor:pointer;padding:12px" onclick="toggleSection('ch5-detail', this)">
      <div style="width:32px;height:32px;background:#7c3aed;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px">5</div>
      <div style="flex:1"><div style="font-weight:700">第5章 综合评价：TOPSIS与DEA</div><div style="font-size:12px;color:#64748b">排名、效率、二维分类</div></div>
      <div style="font-size:12px;color:#94a3b8">▼</div>
    </div>
    <div id="ch5-detail" style="display:none;padding:0 12px 16px 56px;border-top:1px solid #f1f5f9">
      <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:12px">
        <p>本章基于4E指标体系，运用TOPSIS方法对31个省级平台进行综合评价排名，并运用DEA方法评估平台效率，最后构建效率-排名二维分类矩阵。</p>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px">
        <div class="chart-container" style="margin:0"><div class="chart-title">图5-1 TOPSIS综合排名</div>
          <img src="/static/charts/fig5_1_topsis_ranking.png" style="max-width:100%;border-radius:6px" alt="TOPSIS排名">
        </div>
        <div class="chart-container" style="margin:0"><div class="chart-title">图5-2 DEA效率散点图</div>
          <img src="/static/charts/fig5_2_dea_scatter.png" style="max-width:100%;border-radius:6px" alt="DEA效率">
        </div>
      </div>
    </div>
  </div>

  <div class="card" style="margin-bottom:12px">
    <div style="display:flex;align-items:center;gap:12px;cursor:pointer;padding:12px" onclick="toggleSection('ch6-detail', this)">
      <div style="width:32px;height:32px;background:#0ea5e9;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px">6</div>
      <div style="flex:1"><div style="font-weight:700">第6章 因果挖掘：DEMATEL与fsQCA</div><div style="font-size:12px;color:#64748b">因果网络、组态路径</div></div>
      <div style="font-size:12px;color:#94a3b8">▼</div>
    </div>
    <div id="ch6-detail" style="display:none;padding:0 12px 16px 56px;border-top:1px solid #f1f5f9">
      <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:12px">
        <p>本章运用DEMATEL方法构建因果关系网络，识别核心驱动因素；运用fsQCA方法挖掘高绩效平台的组态路径，发现"制度驱动型"和"质量引领型"两条路径。</p>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px">
        <div class="chart-container" style="margin:0"><div class="chart-title">图6-1 DEMATEL因果网络</div>
          <img src="/static/charts/fig6_1_dematel_network.png" style="max-width:100%;border-radius:6px" alt="DEMATEL网络">
        </div>
        <div class="chart-container" style="margin:0"><div class="chart-title">图6-2 fsQCA高绩效路径</div>
          <img src="/static/charts/fig6_2_fsqca_paths.png" style="max-width:100%;border-radius:6px" alt="fsQCA路径">
        </div>
      </div>
    </div>
  </div>

  <div class="card" style="margin-bottom:12px">
    <div style="display:flex;align-items:center;gap:12px;cursor:pointer;padding:12px" onclick="toggleSection('ch7-detail', this)">
      <div style="width:32px;height:32px;background:#dc2626;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px">7</div>
      <div style="flex:1"><div style="font-weight:700">第7章 政策效应：DID评估</div><div style="font-size:12px;color:#64748b">双重差分、平行趋势、稳健性</div></div>
      <div style="font-size:12px;color:#94a3b8">▼</div>
    </div>
    <div id="ch7-detail" style="display:none;padding:0 12px 16px 56px;border-top:1px solid #f1f5f9">
      <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:12px">
        <p>本章以"数据二十条"政策为自然实验，运用DID双重差分法评估政策对平台绩效的影响。基准回归显示ATT=0.187（p<0.01），平行趋势检验和多种稳健性检验均通过。</p>
      </div>
      <div class="chart-container" style="margin:0">
        <div class="chart-title">图7-1 DID政策效应趋势对比</div>
        <img src="/static/charts/fig7_1_did_trend.png" style="max-width:100%;border-radius:6px" alt="DID趋势">
      </div>
    </div>
  </div>

  <div class="card" style="margin-bottom:12px">
    <div style="display:flex;align-items:center;gap:12px;cursor:pointer;padding:12px" onclick="toggleSection('ch8-detail', this)">
      <div style="width:32px;height:32px;background:#16a34a;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px">8</div>
      <div style="flex:1"><div style="font-weight:700">第8章 结论与展望</div><div style="font-size:12px;color:#64748b">主要结论、理论贡献、实践启示</div></div>
      <div style="font-size:12px;color:#94a3b8">▼</div>
    </div>
    <div id="ch8-detail" style="display:none;padding:0 12px 16px 56px;border-top:1px solid #f1f5f9">
      <div style="font-size:13px;color:#64748b;line-height:1.8">
        <p><strong>主要结论：</strong>（1）中国政府数据开放平台绩效整体呈"东高西低"格局；（2）平台绩效差异主要由制度建设和数据质量双轮驱动；（3）"数据二十条"政策对平台绩效产生了显著正向效应（ATT=0.187***）。</p>
        <p><strong>理论贡献：</strong>① 构建了适用于中国情境的政府数据开放平台4E评估框架；② 揭示了制度同形三机制对平台建设的差异化影响；③ 发现了"制度驱动型"和"质量引领型"两条高绩效路径。</p>
        <p><strong>实践启示：</strong>（1）欠发达地区应优先补齐制度建设短板；（2）数据质量提升应聚焦开放格式标准化和元数据完整性；（3）政策制定应注重差异化施策，避免"一刀切"。</p>
      </div>
    </div>
  </div>
</div>

<!-- 第四屏：图表完整索引 -->
<div id="figures" class="scroll-section">
  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>论文图表完整索引（36张图 + 24张表）</div></div>
    <div style="margin-bottom:16px"><div style="font-weight:700;margin-bottom:8px;color:#2563eb">第1章 绪论（2张图）</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px">
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#2563eb">图1-1</div><div style="font-size:11px;color:#64748b">研究技术路线图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#2563eb">图1-2</div><div style="font-size:11px;color:#64748b">论文结构安排</div></div>
      </div>
    </div>
    <div style="margin-bottom:16px"><div style="font-weight:700;margin-bottom:8px;color:#059669">第2章 理论基础（8张图 + 4张表）</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px">
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#059669">图2-1</div><div style="font-size:11px;color:#64748b">4E理论框架</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#059669">图2-2</div><div style="font-size:11px;color:#64748b">制度同形三机制</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#059669">图2-3~8</div><div style="font-size:11px;color:#64748b">文献计量与国际比较</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表2-1~4</div><div style="font-size:11px;color:#64748b">理论框架与评估体系</div></div>
      </div>
    </div>
    <div style="margin-bottom:16px"><div style="font-weight:700;margin-bottom:8px;color:#d97706">第3章 研究设计（3张图 + 3张表）</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px">
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#d97706">图3-1</div><div style="font-size:11px;color:#64748b">五方法递进框架</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表3-1~3</div><div style="font-size:11px;color:#64748b">指标体系与数据来源</div></div>
      </div>
    </div>
    <div style="margin-bottom:16px"><div style="font-weight:700;margin-bottom:8px;color:#db2777">第4章 数据采集（6张图 + 4张表）</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px">
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#db2777">图4-1</div><div style="font-size:11px;color:#64748b">平台覆盖地图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#db2777">图4-2</div><div style="font-size:11px;color:#64748b">功能特征分布</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表4-1~4</div><div style="font-size:11px;color:#64748b">平台清单与统计</div></div>
      </div>
    </div>
    <div style="margin-bottom:16px"><div style="font-weight:700;margin-bottom:8px;color:#7c3aed">第5章 综合评价（6张图 + 4张表）</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px">
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#7c3aed">图5-1</div><div style="font-size:11px;color:#64748b">TOPSIS排名</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#7c3aed">图5-2</div><div style="font-size:11px;color:#64748b">DEA效率散点</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表5-1~4</div><div style="font-size:11px;color:#64748b">排名/效率/指标</div></div>
      </div>
    </div>
    <div style="margin-bottom:16px"><div style="font-weight:700;margin-bottom:8px;color:#0ea5e9">第6章 因果挖掘（6张图 + 3张表）</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px">
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#0ea5e9">图6-1</div><div style="font-size:11px;color:#64748b">DEMATEL因果网络</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#0ea5e9">图6-2</div><div style="font-size:11px;color:#64748b">fsQCA路径</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表6-1~3</div><div style="font-size:11px;color:#64748b">因果矩阵与组态</div></div>
      </div>
    </div>
    <div style="margin-bottom:16px"><div style="font-weight:700;margin-bottom:8px;color:#dc2626">第7章 政策效应（3张图 + 3张表）</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px">
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#dc2626">图7-1</div><div style="font-size:11px;color:#64748b">DID趋势对比</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表7-1~3</div><div style="font-size:11px;color:#64748b">回归/趋势/稳健性</div></div>
      </div>
    </div>
    <div style="margin-bottom:16px"><div style="font-weight:700;margin-bottom:8px;color:#16a34a">第8章 结论（2张图 + 3张表）</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px">
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#16a34a">图8-1~2</div><div style="font-size:11px;color:#64748b">结论框架与展望</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表8-1~3</div><div style="font-size:11px;color:#64748b">贡献/启示/建议</div></div>
      </div>
    </div>
  </div>
</div>

<script>
function toggleSection(id, el) {
  var section = document.getElementById(id);
  var arrow = el.querySelector("div:last-child");
  if (section.style.display === "none") {
    section.style.display = "block";
    arrow.textContent = "▲";
  } else {
    section.style.display = "none";
    arrow.textContent = "▼";
  }
}
</script>

{% endblock %}
'''

with open('templates/v3_thesis.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("v3_thesis.html v2 生成完成")
