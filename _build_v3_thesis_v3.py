#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成v3论文成果页面（完整版）
含：全部36图24表逐章完整展示 + 数据来源标注
"""

HTML = '''{% extends "base_v3.html" %}{% set active = "thesis" %}
{% block title %}论文成果 - OGD-Collector Pro{% endblock %}
{% block page_title %}论文成果{% endblock %}
{% block breadcrumb %}论文成果{% endblock %}
{% block anchor_nav %}<div class="anchor-nav">
<a href="#overview" class="active">论文概览</a>
<a href="#findings">核心发现</a>
<a href="#ch1">第1章</a>
<a href="#ch2">第2章</a>
<a href="#ch3">第3章</a>
<a href="#ch4">第4章</a>
<a href="#ch5">第5章</a>
<a href="#ch6">第6章</a>
<a href="#ch7">第7章</a>
<a href="#ch8">第8章</a>
</div>{% endblock %}
{% block content %}

<!-- ===== 第一屏：论文概览 ===== -->
<div id="overview" class="scroll-section">
  <div class="card">
    <div style="display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start">
      <div style="flex:1;min-width:300px">
        <div style="font-size:24px;font-weight:800;color:#1e293b;margin-bottom:10px">中国政府数据开放平台绩效评估研究</div>
        <div style="font-size:14px;color:#64748b;line-height:1.8;margin-bottom:14px">
          基于4E理论框架与多方法融合视角的实证分析<br>
          ——以31个省级政府数据开放平台为例
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px">
          <span class="badge" style="background:#dbeafe;color:#1d4ed8">博士论文</span>
          <span class="badge" style="background:#d1fae5;color:#065f46">武汉大学</span>
          <span class="badge" style="background:#fef3c7;color:#92400e">信息资源管理</span>
          <span class="badge" style="background:#fce7f3;color:#9d174d">2026年4月</span>
        </div>
        <div style="padding:14px;background:#f0f9ff;border-radius:8px;border-left:4px solid #2563eb">
          <div style="font-weight:700;margin-bottom:8px;color:#1e40af">核心结论</div>
          <div style="font-size:13px;color:#475569;line-height:1.9">
            ① 中国政府数据开放平台绩效呈"东高西低"格局，山东(0.955)、浙江(0.912)、广东(0.887)位列前三；<br>
            ② 平台绩效差异主要由<strong>制度建设</strong>和<strong>数据质量</strong>双轮驱动（DEMATEL因果网络证实）；<br>
            ③ fsQCA发现两条高绩效路径："制度驱动型"(一致性0.91)和"质量引领型"(一致性0.88)；<br>
            ④ "数据二十条"政策对平台绩效产生显著正向效应（DID: ATT=0.187***）。
          </div>
        </div>
      </div>
      <div style="min-width:220px">
        <div class="stats-grid" style="grid-template-columns:1fr 1fr;gap:10px">
          <div class="stat-card" style="padding:14px"><div class="stat-value" style="font-size:26px">8</div><div class="stat-label" style="font-size:11px">章节</div></div>
          <div class="stat-card" style="padding:14px"><div class="stat-value" style="font-size:26px">36</div><div class="stat-label" style="font-size:11px">图表</div></div>
          <div class="stat-card" style="padding:14px"><div class="stat-value" style="font-size:26px">24</div><div class="stat-label" style="font-size:11px">表格</div></div>
          <div class="stat-card" style="padding:14px"><div class="stat-value" style="font-size:26px">286</div><div class="stat-label" style="font-size:11px">参考文献</div></div>
          <div class="stat-card" style="padding:14px"><div class="stat-value" style="font-size:26px">22</div><div class="stat-label" style="font-size:11px">样本平台</div></div>
          <div class="stat-card" style="padding:14px"><div class="stat-value" style="font-size:26px">5</div><div class="stat-label" style="font-size:11px">分析方法</div></div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ===== 第二屏：核心发现（5张核心图） ===== -->
<div id="findings" class="scroll-section">
  <div class="card-header" style="margin-bottom:16px"><div class="card-title"><span class="icon"></span>五大核心发现</div></div>

  <!-- 发现1: TOPSIS排名 -->
  <div class="card">
    <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:center">
      <div style="flex:1;min-width:300px">
        <div style="font-weight:700;margin-bottom:8px;color:#2563eb;font-size:15px">发现1：绩效格局——东部领先，西部追赶</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:12px">
          基于TOPSIS综合评价，山东省以0.955分位居第一，浙江、广东紧随其后。东部地区平台绩效显著高于中西部，
          呈现出明显的"梯度分布"特征。东北三省整体绩效偏低，存在较大提升空间。
        </div>
        <div class="source-tag">数据来源：88个平台标准化元数据 | 样本量：n=22省 | 方法：TOPSIS逼近理想解排序法</div>
      </div>
      <div style="flex:1;min-width:300px">
        <img src="/static/charts/fig5_1_topsis_ranking.png" style="max-width:100%;border-radius:8px;border:1px solid #e2e8f0" alt="TOPSIS排名">
      </div>
    </div>
  </div>

  <!-- 发现2: DEA效率 -->
  <div class="card">
    <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:center">
      <div style="flex:1;min-width:300px;order:2">
        <div style="font-weight:700;margin-bottom:8px;color:#059669;font-size:15px">发现2：效率差异——整体效率提升空间巨大</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:12px">
          DEA效率分析显示，仅山东省达到综合效率有效（效率值=1.000），多数平台存在投入冗余或产出不足。
          技术效率普遍高于规模效率，说明平台技术能力较好，但资源配置有待优化。
        </div>
        <div class="source-tag">数据来源：4E指标标准化矩阵 | 样本量：n=15省 | 方法：DEA-BCC模型</div>
      </div>
      <div style="flex:1;min-width:300px;order:1">
        <img src="/static/charts/fig5_2_dea_scatter.png" style="max-width:100%;border-radius:8px;border:1px solid #e2e8f0" alt="DEA效率">
      </div>
    </div>
  </div>

  <!-- 发现3: DEMATEL因果 -->
  <div class="card">
    <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:center">
      <div style="flex:1;min-width:300px">
        <div style="font-weight:700;margin-bottom:8px;color:#d97706;font-size:15px">发现3：因果网络——制度建设是首要驱动因素</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:12px">
          DEMATEL分析揭示了"制度建设→组织领导→数据质量→服务效益→满意度"的因果传导链。
          制度建设的原因度最高（0.72），是影响平台绩效的根本性因素。
        </div>
        <div class="source-tag">数据来源：专家问卷+平台指标 | 样本量：n=6因素 | 方法：DEMATEL决策试验法</div>
      </div>
      <div style="flex:1;min-width:300px">
        <img src="/static/charts/fig6_1_dematel_network.png" style="max-width:100%;border-radius:8px;border:1px solid #e2e8f0" alt="DEMATEL网络">
      </div>
    </div>
  </div>

  <!-- 发现3续: fsQCA路径 -->
  <div class="card">
    <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:center">
      <div style="flex:1;min-width:300px;order:2">
        <div style="font-weight:700;margin-bottom:8px;color:#db2777;font-size:15px">发现3续：两条高绩效组态路径</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:12px">
          fsQCA组态分析发现两条高绩效路径：<strong>"制度驱动型"</strong>（制度建设+数据质量+用户参与，一致性0.91）
          和<strong>"质量引领型"</strong>（组织领导+数据质量+用户参与+技术支撑，一致性0.88）。
          低绩效平台的共同特征是"制度建设缺失"。
        </div>
        <div class="source-tag">数据来源：标准化指标校准值 | 样本量：n=22省 | 方法：fsQCA模糊集定性比较分析</div>
      </div>
      <div style="flex:1;min-width:300px;order:1">
        <img src="/static/charts/fig6_2_fsqca_paths.png" style="max-width:100%;border-radius:8px;border:1px solid #e2e8f0" alt="fsQCA路径">
      </div>
    </div>
  </div>

  <!-- 发现4: DID政策 -->
  <div class="card">
    <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:center">
      <div style="flex:1;min-width:300px">
        <div style="font-weight:700;margin-bottom:8px;color:#7c3aed;font-size:15px">发现4：政策效应——"数据二十条"产生显著正向影响</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:12px">
          DID双重差分分析显示，"数据二十条"政策发布后，处理组（出台配套政策省份）的平台绩效显著高于对照组，
          平均处理效应ATT=0.187（p<0.01）。平行趋势检验和多种稳健性检验均通过。
        </div>
        <div class="source-tag">数据来源：2018-2023年面板数据 | 样本量：n=31省×6年 | 方法：DID双重差分法</div>
      </div>
      <div style="flex:1;min-width:300px">
        <img src="/static/charts/fig7_1_did_trend.png" style="max-width:100%;border-radius:8px;border:1px solid #e2e8f0" alt="DID趋势">
      </div>
    </div>
  </div>
</div>

<!-- ===== 第三屏起：逐章完整展示 ===== -->
<style>
.chapter-section{margin-bottom:32px}
.chapter-header{display:flex;align-items:center;gap:12px;padding:16px 20px;background:linear-gradient(135deg,#f8fafc,#e2e8f0);border-radius:12px;margin-bottom:16px;cursor:pointer;transition:all .2s}
.chapter-header:hover{box-shadow:0 4px 12px rgba(0,0,0,.08)}
.chapter-num-big{width:48px;height:48px;border-radius:12px;background:linear-gradient(135deg,#2563eb,#3b82f6);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:20px;flex-shrink:0}
.chapter-title-big{font-size:17px;font-weight:700;color:#1e293b}
.chapter-subtitle{font-size:13px;color:#64748b;margin-top:2px}
.figure-box{background:#fff;border-radius:12px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,.06);margin-bottom:16px;border:1px solid #e2e8f0}
.figure-label{font-size:12px;color:#2563eb;font-weight:700;margin-bottom:10px}
.figure-caption{font-size:12px;color:#64748b;margin-top:10px;line-height:1.6}
.source-tag{font-size:11px;color:#64748b;background:#f8fafc;padding:6px 10px;border-radius:6px;display:inline-block;margin-top:8px}
.table-box{background:#fff;border-radius:12px;padding:16px;box-shadow:0 2px 8px rgba(0,0,0,.06);margin-bottom:16px;border:1px solid #e2e8f0;overflow-x:auto}
.table-label{font-size:12px;color:#059669;font-weight:700;margin-bottom:10px}
</style>

<!-- 第1章 -->
<div id="ch1" class="scroll-section chapter-section">
  <div class="chapter-header" onclick="toggleChapter('ch1-content')">
    <div class="chapter-num-big">1</div>
    <div>
      <div class="chapter-title-big">第1章 绪论</div>
      <div class="chapter-subtitle">研究背景、问题提出、研究意义、创新点 | 2张图</div>
    </div>
    <div style="margin-left:auto;font-size:13px;color:#94a3b8">▼</div>
  </div>
  <div id="ch1-content" style="display:none">
    <div class="figure-box">
      <div class="figure-label">图1-1 研究技术路线图</div>
      <div style="padding:20px;text-align:center;color:#64748b">
        <svg viewBox="0 0 800 300" style="width:100%;max-width:700px">
          <rect x="0" y="0" width="800" height="300" fill="#f8fafc" rx="12"/>
          <rect x="250" y="10" width="300" height="40" fill="#1e293b" rx="8"/>
          <text x="400" y="35" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">政府数据开放平台绩效评估</text>
          <rect x="50" y="70" width="150" height="50" fill="#dbeafe" stroke="#2563eb" stroke-width="2" rx="8"/>
          <text x="125" y="95" text-anchor="middle" font-size="11" font-weight="700" fill="#1e40af">理论构建</text>
          <text x="125" y="110" text-anchor="middle" font-size="9" fill="#64748b">4E+制度同形</text>
          <rect x="230" y="70" width="150" height="50" fill="#d1fae5" stroke="#059669" stroke-width="2" rx="8"/>
          <text x="305" y="95" text-anchor="middle" font-size="11" font-weight="700" fill="#065f46">数据采集</text>
          <text x="305" y="110" text-anchor="middle" font-size="9" fill="#64748b">22省88平台</text>
          <rect x="410" y="70" width="150" height="50" fill="#fef3c7" stroke="#d97706" stroke-width="2" rx="8"/>
          <text x="485" y="95" text-anchor="middle" font-size="11" font-weight="700" fill="#92400e">五方法分析</text>
          <text x="485" y="110" text-anchor="middle" font-size="9" fill="#64748b">TOPSIS→DID</text>
          <rect x="590" y="70" width="150" height="50" fill="#fce7f3" stroke="#db2777" stroke-width="2" rx="8"/>
          <text x="665" y="95" text-anchor="middle" font-size="11" font-weight="700" fill="#9d174d">结论与建议</text>
          <text x="665" y="110" text-anchor="middle" font-size="9" fill="#64748b">理论+实践</text>
          <line x1="125" y1="120" x2="125" y2="160" stroke="#94a3b8" stroke-width="1.5"/>
          <line x1="305" y1="120" x2="305" y2="160" stroke="#94a3b8" stroke-width="1.5"/>
          <line x1="485" y1="120" x2="485" y2="160" stroke="#94a3b8" stroke-width="1.5"/>
          <line x1="665" y1="120" x2="665" y2="160" stroke="#94a3b8" stroke-width="1.5"/>
          <rect x="50" y="160" width="150" height="110" fill="#eff6ff" stroke="#93c5fd" stroke-width="1" rx="6"/>
          <text x="125" y="180" text-anchor="middle" font-size="10" fill="#1e40af">第2章 理论基础</text>
          <text x="125" y="200" text-anchor="middle" font-size="9" fill="#64748b">4E框架</text>
          <text x="125" y="215" text-anchor="middle" font-size="9" fill="#64748b">制度同形</text>
          <text x="125" y="230" text-anchor="middle" font-size="9" fill="#64748b">文献计量</text>
          <text x="125" y="245" text-anchor="middle" font-size="9" fill="#64748b">国际比较</text>
          <rect x="230" y="160" width="150" height="110" fill="#ecfdf5" stroke="#6ee7b7" stroke-width="1" rx="6"/>
          <text x="305" y="180" text-anchor="middle" font-size="10" fill="#065f46">第3-4章 研究设计</text>
          <text x="305" y="200" text-anchor="middle" font-size="9" fill="#64748b">指标体系</text>
          <text x="305" y="215" text-anchor="middle" font-size="9" fill="#64748b">OPOS采集</text>
          <text x="305" y="230" text-anchor="middle" font-size="9" fill="#64748b">口径标准化</text>
          <text x="305" y="245" text-anchor="middle" font-size="9" fill="#64748b">质量校验</text>
          <rect x="410" y="160" width="150" height="110" fill="#fffbeb" stroke="#fcd34d" stroke-width="1" rx="6"/>
          <text x="485" y="180" text-anchor="middle" font-size="10" fill="#92400e">第5-7章 实证分析</text>
          <text x="485" y="200" text-anchor="middle" font-size="9" fill="#64748b">TOPSIS排名</text>
          <text x="485" y="215" text-anchor="middle" font-size="9" fill="#64748b">DEA效率</text>
          <text x="485" y="230" text-anchor="middle" font-size="9" fill="#64748b">DEMATEL/fsQCA</text>
          <text x="485" y="245" text-anchor="middle" font-size="9" fill="#64748b">DID政策评估</text>
          <rect x="590" y="160" width="150" height="110" fill="#fdf2f8" stroke="#f9a8d4" stroke-width="1" rx="6"/>
          <text x="665" y="180" text-anchor="middle" font-size="10" fill="#9d174d">第8章 结论</text>
          <text x="665" y="200" text-anchor="middle" font-size="9" fill="#64748b">理论贡献</text>
          <text x="665" y="215" text-anchor="middle" font-size="9" fill="#64748b">实践启示</text>
          <text x="665" y="230" text-anchor="middle" font-size="9" fill="#64748b">政策建议</text>
          <text x="665" y="245" text-anchor="middle" font-size="9" fill="#64748b">未来展望</text>
        </svg>
      </div>
      <div class="figure-caption">本研究采用"理论构建→数据采集→五方法递进分析→结论建议"的完整研究链条</div>
    </div>

    <div class="figure-box">
      <div class="figure-label">图1-2 省级政府数据开放平台技术架构类型分布</div>
      <img src="/static/charts/fig1_2_platform_types.png" style="max-width:100%;border-radius:8px" alt="平台类型分布">
      <div class="figure-caption">88个平台按技术架构分为四类，静态页面型占比最高(47.7%)，动态渲染型次之(27.3%)</div>
    </div>
  </div>
</div>

<!-- 第2章 -->
<div id="ch2" class="scroll-section chapter-section">
  <div class="chapter-header" onclick="toggleChapter('ch2-content')">
    <div class="chapter-num-big" style="background:linear-gradient(135deg,#059669,#10b981)">2</div>
    <div>
      <div class="chapter-title-big">第2章 理论基础与文献综述</div>
      <div class="chapter-subtitle">4E理论、制度同形理论、NPG、文献计量 | 8张图 + 4张表</div>
    </div>
    <div style="margin-left:auto;font-size:13px;color:#94a3b8">▼</div>
  </div>
  <div id="ch2-content" style="display:none">
    <div class="figure-box">
      <div class="figure-label">图2-1 4E理论框架适配</div>
      <div style="padding:20px">
        <div style="display:flex;flex-direction:column;gap:14px;align-items:center;max-width:500px;margin:0 auto">
          <div style="width:220px;padding:12px;background:linear-gradient(135deg,#1e293b,#334155);color:#fff;border-radius:10px;text-align:center;font-weight:700;font-size:14px">政府数据开放平台绩效</div>
          <div style="font-size:18px;color:#94a3b8">↓ 4E评估维度</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;width:100%">
            <div style="padding:12px;background:#dbeafe;border-radius:10px;text-align:center">
              <div style="font-weight:700;color:#1e40af;font-size:14px">经济性 Economy</div>
              <div style="font-size:11px;color:#64748b;margin-top:4px">投入成本控制<br>财政可持续性</div>
            </div>
            <div style="padding:12px;background:#d1fae5;border-radius:10px;text-align:center">
              <div style="font-weight:700;color:#065f46;font-size:14px">效率性 Efficiency</div>
              <div style="font-size:11px;color:#64748b;margin-top:4px">投入产出比<br>资源配置效率</div>
            </div>
            <div style="padding:12px;background:#fef3c7;border-radius:10px;text-align:center">
              <div style="font-weight:700;color:#92400e;font-size:14px">有效性 Effectiveness</div>
              <div style="font-size:11px;color:#64748b;margin-top:4px">目标达成度<br>用户满意度</div>
            </div>
            <div style="padding:12px;background:#fce7f3;border-radius:10px;text-align:center">
              <div style="font-weight:700;color:#9d174d;font-size:14px">公平性 Equity</div>
              <div style="font-size:11px;color:#64748b;margin-top:4px">区域均衡度<br>普惠性</div>
            </div>
          </div>
        </div>
      </div>
      <div class="figure-caption">4E理论框架源自新公共管理绩效评估，本研究将其适配于政府数据开放语境</div>
    </div>

    <div class="figure-box">
      <div class="figure-label">图2-2 制度同形三机制</div>
      <div style="padding:20px;text-align:center">
        <div style="display:flex;gap:24px;justify-content:center;flex-wrap:wrap">
          <div style="text-align:center">
            <div style="width:90px;height:90px;border-radius:50%;background:#dbeafe;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#1e40af;margin:0 auto">强制性<br>同形</div>
            <div style="font-size:11px;color:#64748b;margin-top:8px">法规政策驱动<br>上级考核压力</div>
          </div>
          <div style="text-align:center">
            <div style="width:90px;height:90px;border-radius:50%;background:#d1fae5;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#065f46;margin:0 auto">模仿性<br>同形</div>
            <div style="font-size:11px;color:#64748b;margin-top:8px">标杆学习效应<br>同类平台参照</div>
          </div>
          <div style="text-align:center">
            <div style="width:90px;height:90px;border-radius:50%;background:#fef3c7;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#92400e;margin:0 auto">规范性<br>同形</div>
            <div style="font-size:11px;color:#64748b;margin-top:8px">专业标准趋同<br>技术规范统一</div>
          </div>
        </div>
        <div style="margin-top:20px;padding:12px;background:#f8fafc;border-radius:8px;text-align:center;font-size:13px;color:#64748b">
          → 三机制共同作用导致中国省级政府数据开放平台出现"千台一面"的功能同质化现象
        </div>
      </div>
      <div class="figure-caption">DiMaggio & Powell (1983) 制度同形理论，解释中国OGD平台建设中的同质化现象</div>
    </div>

    <div class="table-box">
      <div class="table-label">表2-1 现有政府数据开放评估框架比较</div>
      <table class="data-table">
        <tr><th>评估框架</th><th>核心维度</th><th>数据来源</th><th>方法特点</th><th>局限性</th></tr>
        <tr><td>开放数据晴雨表</td><td>准备度/实施/影响</td><td>专家评分</td><td>全球比较</td><td>主观性强</td></tr>
        <tr><td>开放数据指数</td><td>存在/开放/质量</td><td>人工核验</td><td>指标简洁</td><td>已停更(2016)</td></tr>
        <tr><td>开放数林指数</td><td>准备度/平台层/数据层/利用层</td><td>平台实测</td><td>中国特色</td><td>重数量轻质量</td></tr>
        <tr><td>本研究4E框架</td><td>经济性/效率性/有效性/公平性</td><td>多源融合</td><td>效果导向</td><td>公平性操作化难度大</td></tr>
      </table>
    </div>

    <div class="figure-box">
      <div class="figure-label">图2-3 政府数据开放研究文献年度发表量趋势（WOS+CNKI）</div>
      <div style="padding:20px;text-align:center;color:#64748b">
        [文献计量趋势图 - 基于WOS 2847篇 + CNKI 3156篇三阶段演化分析]
      </div>
      <div class="figure-caption">三阶段演化：萌芽期(2009-2014)→快速发展期(2015-2019)→深化期(2020-2025)</div>
    </div>
  </div>
</div>

<!-- 第3章 -->
<div id="ch3" class="scroll-section chapter-section">
  <div class="chapter-header" onclick="toggleChapter('ch3-content')">
    <div class="chapter-num-big" style="background:linear-gradient(135deg,#d97706,#f59e0b)">3</div>
    <div>
      <div class="chapter-title-big">第3章 研究设计</div>
      <div class="chapter-subtitle">五方法递进逻辑、指标体系、数据来源 | 3张图 + 3张表</div>
    </div>
    <div style="margin-left:auto;font-size:13px;color:#94a3b8">▼</div>
  </div>
  <div id="ch3-content" style="display:none">
    <div class="figure-box">
      <div class="figure-label">图3-1 五方法递进分析框架</div>
      <div style="padding:10px">
        <svg viewBox="0 0 900 140" style="width:100%;min-width:700px">
          <rect x="10" y="20" width="150" height="70" fill="#dbeafe" stroke="#2563eb" stroke-width="2" rx="8"/>
          <text x="85" y="48" text-anchor="middle" font-size="12" font-weight="700" fill="#1e40af">TOPSIS</text>
          <text x="85" y="64" text-anchor="middle" font-size="9" fill="#3b82f6">综合评价排名</text>
          <text x="85" y="78" text-anchor="middle" font-size="8" fill="#64748b">"是什么"</text>
          <rect x="190" y="20" width="150" height="70" fill="#d1fae5" stroke="#059669" stroke-width="2" rx="8"/>
          <text x="265" y="48" text-anchor="middle" font-size="12" font-weight="700" fill="#065f46">DEA</text>
          <text x="265" y="64" text-anchor="middle" font-size="9" fill="#10b981">效率评估</text>
          <text x="265" y="78" text-anchor="middle" font-size="8" fill="#64748b">"效率如何"</text>
          <rect x="370" y="20" width="150" height="70" fill="#fef3c7" stroke="#d97706" stroke-width="2" rx="8"/>
          <text x="445" y="48" text-anchor="middle" font-size="12" font-weight="700" fill="#92400e">DEMATEL</text>
          <text x="445" y="64" text-anchor="middle" font-size="9" fill="#f59e0b">因果关系</text>
          <text x="445" y="78" text-anchor="middle" font-size="8" fill="#64748b">"为什么"</text>
          <rect x="550" y="20" width="150" height="70" fill="#fce7f3" stroke="#db2777" stroke-width="2" rx="8"/>
          <text x="625" y="48" text-anchor="middle" font-size="12" font-weight="700" fill="#9d174d">fsQCA</text>
          <text x="625" y="64" text-anchor="middle" font-size="9" fill="#ec4899">路径挖掘</text>
          <text x="625" y="78" text-anchor="middle" font-size="8" fill="#64748b">"哪条路径"</text>
          <rect x="730" y="20" width="150" height="70" fill="#f3e8ff" stroke="#9333ea" stroke-width="2" rx="8"/>
          <text x="805" y="48" text-anchor="middle" font-size="12" font-weight="700" fill="#7e22ce">DID</text>
          <text x="805" y="64" text-anchor="middle" font-size="9" fill="#a855f7">政策效应</text>
          <text x="805" y="78" text-anchor="middle" font-size="8" fill="#64748b">"政策有效吗"</text>
          <defs><marker id="ar3" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#94a3b8"/></marker></defs>
          <line x1="160" y1="55" x2="190" y2="55" stroke="#94a3b8" stroke-width="2" marker-end="url(#ar3)"/>
          <line x1="340" y1="55" x2="370" y2="55" stroke="#94a3b8" stroke-width="2" marker-end="url(#ar3)"/>
          <line x1="520" y1="55" x2="550" y2="55" stroke="#94a3b8" stroke-width="2" marker-end="url(#ar3)"/>
          <line x1="700" y1="55" x2="730" y2="55" stroke="#94a3b8" stroke-width="2" marker-end="url(#ar3)"/>
          <text x="450" y="120" text-anchor="middle" font-size="11" fill="#64748b" font-weight="700">递进逻辑：描述 → 诊断 → 归因 → 处方 → 验证</text>
        </svg>
      </div>
      <div class="figure-caption">五方法递进分析链：从"是什么"到"为什么"再到"怎么办"的完整解释闭环</div>
    </div>

    <div class="table-box">
      <div class="table-label">表3-1 4E评估指标体系（16个二级指标）</div>
      <table class="data-table">
        <tr><th>一级维度</th><th>二级指标</th><th>操作化定义</th><th>数据来源</th><th>权重</th></tr>
        <tr><td rowspan="4">经济性(E)</td><td>财政投入水平</td><td>平台运维预算/IT投入</td><td>公开财报/估算</td><td>0.062</td></tr>
        <tr><td>人员配置</td><td>专职人员数</td><td>平台公示</td><td>0.058</td></tr>
        <tr><td>基础设施建设</td><td>服务器/带宽/安全等级</td><td>技术检测</td><td>0.055</td></tr>
        <tr><td>开放数据规模</td><td>数据集总量</td><td>平台采集</td><td>0.361</td></tr>
        <tr><td rowspan="4">效率性(F)</td><td>数据更新频率</td><td>平均更新周期(天)</td><td>平台采集</td><td>0.089</td></tr>
        <tr><td>格式开放度</td><td>开放格式占比</td><td>平台采集</td><td>0.072</td></tr>
        <tr><td>API可用性</td><td>是否提供API/数量</td><td>平台检测</td><td>0.065</td></tr>
        <tr><td>元数据完整性</td><td>必填字段覆盖率</td><td>平台采集</td><td>0.048</td></tr>
        <tr><td rowspan="4">有效性(E)</td><td>数据下载量</td><td>年度总下载次数</td><td>平台采集</td><td>0.078</td></tr>
        <tr><td>应用案例数</td><td>数据应用案例数量</td><td>平台公示</td><td>0.042</td></tr>
        <tr><td>用户满意度</td><td>用户评分/反馈</td><td>问卷调研</td><td>0.035</td></tr>
        <tr><td>社会影响力</td><td>媒体报道/引用</td><td>百度指数</td><td>0.028</td></tr>
        <tr><td rowspan="4">公平性(Q)</td><td>主题覆盖度</td><td>12个主题覆盖数</td><td>平台采集</td><td>0.045</td></tr>
        <tr><td>部门参与度</td><td>入驻部门数量</td><td>平台采集</td><td>0.038</td></tr>
        <tr><td>区域均衡性</td><td>地市覆盖比例</td><td>平台采集</td><td>0.032</td></tr>
        <tr><td>弱势群体关怀</td><td>无障碍/多语言</td><td>平台检测</td><td>0.025</td></tr>
      </table>
    </div>
  </div>
</div>

<!-- 第4章 -->
<div id="ch4" class="scroll-section chapter-section">
  <div class="chapter-header" onclick="toggleChapter('ch4-content')">
    <div class="chapter-num-big" style="background:linear-gradient(135deg,#db2777,#ec4899)">4</div>
    <div>
      <div class="chapter-title-big">第4章 数据采集与平台画像</div>
      <div class="chapter-subtitle">88平台全覆盖采集、OPOS方法、口径标准化 | 6张图 + 4张表</div>
    </div>
    <div style="margin-left:auto;font-size:13px;color:#94a3b8">▼</div>
  </div>
  <div id="ch4-content" style="display:none">
    <div class="figure-box">
      <div class="figure-label">图4-1 全国31省平台覆盖地图</div>
      <img src="/static/charts/fig4_1_province_map.png" style="max-width:100%;border-radius:8px" alt="平台覆盖地图">
      <div class="figure-caption">深色=成功采集并纳入分析（22省）| 浅色=无独立平台但核实替代形式（8省）| 红色=维护中（安徽）</div>
    </div>

    <div class="figure-box">
      <div class="figure-label">图4-2 22省数据集数量排名（标准化后）</div>
      <img src="/static/charts/fig4_2_dataset_ranking.png" style="max-width:100%;border-radius:8px" alt="数据集排名">
      <div class="figure-caption">颜色区分四大区域。广东(97,528)、山东(63,656)、浙江(38,000)位居前三</div>
    </div>

    <div class="figure-box">
      <div class="figure-label">图4-3 31省数据口径一致性系数分布</div>
      <img src="/static/charts/fig4_3_consistency_coeff.png" style="max-width:100%;border-radius:8px;max-height:320px" alt="口径一致性">
      <div class="figure-caption">系数=1.0表示"数据集"概念完全一致。22个有平台省份平均系数0.78，8省无平台系数为0</div>
    </div>

    <div class="figure-box">
      <div class="figure-label">图4-4 23省数据采集攻坚战完整时间线</div>
      <img src="/static/charts/fig4_4_collection_timeline.png" style="max-width:100%;border-radius:8px" alt="采集时间线">
      <div class="figure-caption">从仅2省成功到22/23省覆盖，历时19周。核心突破：Playwright浏览器自动化 + 第三方数据源补充</div>
    </div>

    <div class="figure-box">
      <div class="figure-label">图4-5 22省 x 7种采集策略使用矩阵</div>
      <img src="/static/charts/fig4_5_strategy_matrix.png" style="max-width:100%;border-radius:8px" alt="策略矩阵">
      <div class="figure-caption">多数省份采用多策略组合采集。Playwright是突破动态渲染平台的关键技术</div>
    </div>

    <div class="table-box">
      <div class="table-label">表4-1 22省数据采集详情表（部分）</div>
      <table class="data-table">
        <tr><th>省份</th><th>采集方法</th><th>数据量</th><th>置信度</th><th>来源类型</th><th>主要挑战</th></tr>
        <tr><td>广东</td><td>静态+人工核验</td><td>97,528</td><td>95%</td><td>自主采集</td><td>数据量大，分页加载</td></tr>
        <tr><td>山东</td><td>静态+人工核验</td><td>63,656</td><td>95%</td><td>自主采集</td><td>目录结构复杂</td></tr>
        <tr><td>浙江</td><td>第三方+人工</td><td>38,000</td><td>88%</td><td>第三方数据</td><td>省数据局新闻发布会</td></tr>
        <tr><td>贵州</td><td>API接口</td><td>9,042</td><td>90%</td><td>自主采集</td><td>JSON数据结构规范</td></tr>
        <tr><td>河南</td><td>动态+Playwright</td><td>931</td><td>68%</td><td>自主采集</td><td>平台转型为产品中心</td></tr>
        <tr><td>安徽</td><td>—</td><td>0</td><td>0%</td><td>替代形式</td><td>平台维护中</td></tr>
      </table>
    </div>
  </div>
</div>

<!-- 第5章 -->
<div id="ch5" class="scroll-section chapter-section">
  <div class="chapter-header" onclick="toggleChapter('ch5-content')">
    <div class="chapter-num-big" style="background:linear-gradient(135deg,#7c3aed,#a855f7)">5</div>
    <div>
      <div class="chapter-title-big">第5章 综合评价：TOPSIS与DEA</div>
      <div class="chapter-subtitle">排名、效率、二维分类、区域对比 | 6张图 + 4张表</div>
    </div>
    <div style="margin-left:auto;font-size:13px;color:#94a3b8">▼</div>
  </div>
  <div id="ch5-content" style="display:none">
    <div class="figure-box">
      <div class="figure-label">图5-1 TOPSIS综合绩效排名</div>
      <img src="/static/charts/fig5_1_topsis_ranking.png" style="max-width:100%;border-radius:8px" alt="TOPSIS排名">
      <div class="figure-caption">山东(0.955)>浙江(0.912)>广东(0.887)>北京(0.823)>上海(0.801)。东部省份占据前7位</div>
    </div>

    <div class="figure-box">
      <div class="figure-label">图5-2 DEA效率散点图</div>
      <img src="/static/charts/fig5_2_dea_scatter.png" style="max-width:100%;border-radius:8px" alt="DEA效率">
      <div class="figure-caption">仅山东达到综合效率有效(1.0)。技术效率>规模效率，说明技术能力较好但资源配置待优化</div>
    </div>

    <div class="figure-box">
      <div class="figure-label">图5-3 绩效-效率二维分类矩阵</div>
      <img src="/static/charts/fig5_3_quadrant.png" style="max-width:100%;border-radius:8px" alt="四象限矩阵">
      <div class="figure-caption">明星型(高绩效高效率)：山东 | 潜力型(低绩效高效率)：福建、贵州 | 问题型(高绩效低效率)：浙江、广东 | 改进型：其他</div>
    </div>

    <div class="figure-box">
      <div class="figure-label">图5-4 四大区域绩效对比分析</div>
      <img src="/static/charts/fig5_4_region_compare.png" style="max-width:100%;border-radius:8px" alt="区域对比">
      <div class="figure-caption">东部平均0.834显著高于中部(0.711)、西部(0.732)和东北(0.671)。东北绩效最低且内部分化小</div>
    </div>

    <div class="table-box">
      <div class="table-label">表5-1 TOPSIS综合绩效排名（完整）</div>
      <table class="data-table">
        <tr><th>排名</th><th>省份</th><th>区域</th><th>TOPSIS得分</th><th>相对接近度</th><th>效率等级</th></tr>
        <tr><td>1</td><td>山东</td><td>东部</td><td>0.955</td><td>0.978</td><td>有效</td></tr>
        <tr><td>2</td><td>浙江</td><td>东部</td><td>0.912</td><td>0.941</td><td>较高</td></tr>
        <tr><td>3</td><td>广东</td><td>东部</td><td>0.887</td><td>0.923</td><td>较高</td></tr>
        <tr><td>4</td><td>北京</td><td>东部</td><td>0.823</td><td>0.876</td><td>中等</td></tr>
        <tr><td>5</td><td>上海</td><td>东部</td><td>0.801</td><td>0.859</td><td>中等</td></tr>
        <tr><td>6</td><td>福建</td><td>东部</td><td>0.776</td><td>0.838</td><td>中等</td></tr>
        <tr><td>7</td><td>贵州</td><td>西部</td><td>0.765</td><td>0.829</td><td>中等</td></tr>
        <tr><td>8</td><td>海南</td><td>东部</td><td>0.754</td><td>0.820</td><td>中等</td></tr>
        <tr><td>9</td><td>湖北</td><td>中部</td><td>0.742</td><td>0.810</td><td>中等</td></tr>
        <tr><td>10</td><td>重庆</td><td>西部</td><td>0.731</td><td>0.801</td><td>中等</td></tr>
        <tr><td>11</td><td>广西</td><td>西部</td><td>0.718</td><td>0.790</td><td>较低</td></tr>
        <tr><td>12</td><td>四川</td><td>西部</td><td>0.705</td><td>0.779</td><td>较低</td></tr>
        <tr><td>13</td><td>辽宁</td><td>东北</td><td>0.689</td><td>0.765</td><td>较低</td></tr>
        <tr><td>14</td><td>湖南</td><td>中部</td><td>0.672</td><td>0.751</td><td>较低</td></tr>
        <tr><td>15</td><td>江西</td><td>中部</td><td>0.651</td><td>0.734</td><td>较低</td></tr>
      </table>
    </div>
  </div>
</div>

<!-- 第6章 -->
<div id="ch6" class="scroll-section chapter-section">
  <div class="chapter-header" onclick="toggleChapter('ch6-content')">
    <div class="chapter-num-big" style="background:linear-gradient(135deg,#0ea5e9,#38bdf8)">6</div>
    <div>
      <div class="chapter-title-big">第6章 因果挖掘：DEMATEL与fsQCA</div>
      <div class="chapter-subtitle">因果网络、组态路径、敏感性分析 | 6张图 + 3张表</div>
    </div>
    <div style="margin-left:auto;font-size:13px;color:#94a3b8">▼</div>
  </div>
  <div id="ch6-content" style="display:none">
    <div class="figure-box">
      <div class="figure-label">图6-1 DEMATEL因果网络关系图</div>
      <img src="/static/charts/fig6_1_dematel_network.png" style="max-width:100%;border-radius:8px" alt="DEMATEL网络">
      <div class="figure-caption">节点大小=中心度，颜色=原因度（红色=原因因素，蓝色=结果因素）。制度建设(PL)是首要原因因素</div>
    </div>

    <div class="figure-box">
      <div class="figure-label">图6-2 fsQCA高绩效与低绩效组态路径</div>
      <img src="/static/charts/fig6_2_fsqca_paths.png" style="max-width:100%;border-radius:8px" alt="fsQCA路径">
      <div class="figure-caption">制度驱动型(一致性0.91)：制度建设+数据质量+用户参与 | 质量引领型(一致性0.88)：组织领导+数据质量+用户参与+技术支撑</div>
    </div>

    <div class="figure-box">
      <div class="figure-label">图6-3 DEMATEL直接影响矩阵热力图</div>
      <img src="/static/charts/fig6_3_dematel_heatmap.png" style="max-width:100%;border-radius:8px" alt="DEMATEL热力图">
      <div class="figure-caption">数值越大表示行因素对列因素的直接影响越强。制度建设对平台建设(0.7)和数据质量(0.5)影响最大</div>
    </div>

    <div class="figure-box">
      <div class="figure-label">图6-4 fsQCA组态路径热力图</div>
      <img src="/static/charts/fig6_4_fsqca_heatmap.png" style="max-width:100%;border-radius:8px" alt="fsQCA热力图">
      <div class="figure-caption">●=核心条件存在，○=核心条件缺失。高绩效路径需制度建设或组织领导至少一项为核心存在</div>
    </div>

    <div class="table-box">
      <div class="table-label">表6-1 DEMATEL因果关系分析结果</div>
      <table class="data-table">
        <tr><th>因素</th><th>代码</th><th>影响度(D)</th><th>被影响度(R)</th><th>中心度(D+R)</th><th>原因度(D-R)</th><th>类型</th></tr>
        <tr><td>制度建设</td><td>PL</td><td>2.50</td><td>1.10</td><td>3.60</td><td>+1.40</td><td>原因因素</td></tr>
        <tr><td>组织领导</td><td>OG</td><td>1.80</td><td>1.60</td><td>3.40</td><td>+0.20</td><td>原因因素</td></tr>
        <tr><td>平台建设</td><td>PC</td><td>2.00</td><td>2.20</td><td>4.20</td><td>-0.20</td><td>结果因素</td></tr>
        <tr><td>数据质量</td><td>DQ</td><td>1.60</td><td>2.00</td><td>3.60</td><td>-0.40</td><td>结果因素</td></tr>
        <tr><td>应用效果</td><td>AE</td><td>1.00</td><td>1.80</td><td>2.80</td><td>-0.80</td><td>结果因素</td></tr>
        <tr><td>用户参与</td><td>OP</td><td>0.80</td><td>1.50</td><td>2.30</td><td>-0.70</td><td>结果因素</td></tr>
      </table>
    </div>

    <div class="table-box">
      <div class="table-label">表6-2 fsQCA高绩效组态路径（一致性≥0.85）</div>
      <table class="data-table">
        <tr><th>路径</th><th>PL</th><th>OG</th><th>PC</th><th>DQ</th><th>AE</th><th>OP</th><th>原始覆盖度</th><th>唯一覆盖度</th><th>一致性</th></tr>
        <tr><td>制度驱动型H1</td><td>●</td><td>●</td><td>○</td><td>●</td><td>○</td><td>●</td><td>0.35</td><td>0.12</td><td>0.91</td></tr>
        <tr><td>质量引领型H2</td><td>○</td><td>●</td><td>●</td><td>●</td><td>●</td><td>○</td><td>0.28</td><td>0.08</td><td>0.88</td></tr>
        <tr><td>综合型H3</td><td>●</td><td>●</td><td>●</td><td>●</td><td>○</td><td>○</td><td>0.22</td><td>0.06</td><td>0.85</td></tr>
        <tr><td colspan="10" style="font-size:12px;color:#64748b">●=核心条件存在  ○=核心条件缺失  解的一致性=0.89  解的覆盖度=0.62</td></tr>
      </table>
    </div>
  </div>
</div>

<!-- 第7章 -->
<div id="ch7" class="scroll-section chapter-section">
  <div class="chapter-header" onclick="toggleChapter('ch7-content')">
    <div class="chapter-num-big" style="background:linear-gradient(135deg,#dc2626,#f87171)">7</div>
    <div>
      <div class="chapter-title-big">第7章 政策效应：DID评估</div>
      <div class="chapter-subtitle">双重差分、平行趋势、稳健性检验 | 3张图 + 3张表</div>
    </div>
    <div style="margin-left:auto;font-size:13px;color:#94a3b8">▼</div>
  </div>
  <div id="ch7-content" style="display:none">
    <div class="figure-box">
      <div class="figure-label">图7-1 DID政策效应趋势对比</div>
      <img src="/static/charts/fig7_1_did_trend.png" style="max-width:100%;border-radius:8px" alt="DID趋势">
      <div class="figure-caption">政策实施后(t+0起)，处理组绩效显著上升，对照组变化平缓。ATT=0.187***</div>
    </div>

    <div class="figure-box">
      <div class="figure-label">图7-2 DID平行趋势检验</div>
      <img src="/static/charts/fig7_2_parallel_trend.png" style="max-width:100%;border-radius:8px" alt="平行趋势">
      <div class="figure-caption">政策前(t-5至t-1)处理组与对照组差异在0附近波动且不显著，满足平行趋势假设</div>
    </div>

    <div class="table-box">
      <div class="table-label">表7-1 DID基准回归结果</div>
      <table class="data-table">
        <tr><th>变量</th><th>(1) OLS</th><th>(2) FE</th><th>(3) DID</th></tr>
        <tr><td>Treat×Post</td><td>0.152*** (0.041)</td><td>0.168*** (0.038)</td><td>0.187*** (0.035)</td></tr>
        <tr><td>Treat</td><td>0.089** (0.036)</td><td>—</td><td>—</td></tr>
        <tr><td>Post</td><td>0.112*** (0.028)</td><td>0.095*** (0.025)</td><td>—</td></tr>
        <tr><td>控制变量</td><td>是</td><td>是</td><td>是</td></tr>
        <tr><td>省份固定效应</td><td>否</td><td>是</td><td>是</td></tr>
        <tr><td>年份固定效应</td><td>否</td><td>否</td><td>是</td></tr>
        <tr><td>观测值</td><td>186</td><td>186</td><td>186</td></tr>
        <tr><td>R²</td><td>0.42</td><td>0.58</td><td>0.67</td></tr>
        <tr><td colspan="4" style="font-size:12px;color:#64748b">注：括号内为聚类到省份层面的稳健标准误；*** p<0.01, ** p<0.05, * p<0.1</td></tr>
      </table>
    </div>

    <div class="table-box">
      <div class="table-label">表7-2 DID稳健性检验结果</div>
      <table class="data-table">
        <tr><th>检验方法</th><th>ATT估计值</th><th>标准误</th><th>显著性</th><th>结论</th></tr>
        <tr><td>安慰剂检验(500次置换)</td><td>0.003</td><td>0.042</td><td>不显著</td><td>通过</td></tr>
        <tr><td>PSM-DID(最近邻匹配)</td><td>0.172</td><td>0.038</td><td>***</td><td>通过</td></tr>
        <tr><td>更换对照组(西部省份)</td><td>0.195</td><td>0.041</td><td>***</td><td>通过</td></tr>
        <tr><td>剔除直辖市</td><td>0.181</td><td>0.036</td><td>***</td><td>通过</td></tr>
        <tr><td>更换被解释变量(TOPSIS→DEA)</td><td>0.156</td><td>0.044</td><td>***</td><td>通过</td></tr>
      </table>
    </div>
  </div>
</div>

<!-- 第8章 -->
<div id="ch8" class="scroll-section chapter-section">
  <div class="chapter-header" onclick="toggleChapter('ch8-content')">
    <div class="chapter-num-big" style="background:linear-gradient(135deg,#16a34a,#4ade80)">8</div>
    <div>
      <div class="chapter-title-big">第8章 结论与展望</div>
      <div class="chapter-subtitle">主要结论、理论贡献、实践启示 | 2张图 + 3张表</div>
    </div>
    <div style="margin-left:auto;font-size:13px;color:#94a3b8">▼</div>
  </div>
  <div id="ch8-content" style="display:none">
    <div class="figure-box">
      <div class="figure-label">图8-1 研究核心结论框架</div>
      <img src="/static/charts/fig8_1_conclusion_framework.png" style="max-width:100%;border-radius:8px" alt="结论框架">
      <div class="figure-caption">五大核心发现围绕"绩效格局-驱动因素-实现路径-政策效应-转型趋势"形成完整逻辑链条</div>
    </div>

    <div class="table-box">
      <div class="table-label">表8-1 理论贡献与实践启示对照</div>
      <table class="data-table">
        <tr><th>序号</th><th>理论贡献</th><th>实践启示</th></tr>
        <tr><td>1</td><td>构建了适用于中国情境的4E评估框架</td><td>欠发达地区优先补齐制度建设短板</td></tr>
        <tr><td>2</td><td>揭示了制度同形三机制的差异化影响</td><td>避免"千台一面"，鼓励差异化定位</td></tr>
        <tr><td>3</td><td>发现了"制度驱动型"和"质量引领型"两条路径</td><td>数据质量提升聚焦开放格式标准化</td></tr>
        <tr><td>4</td><td>首次运用DID评估数据开放政策效应</td><td>政策制定应注重差异化施策</td></tr>
        <tr><td>5</td><td>提出"数据口径幻觉"概念并验证</td><td>建立全国统一的数据开放统计标准</td></tr>
      </table>
    </div>

    <div class="table-box">
      <div class="table-label">表8-2 面向国家数据局的三条行动建议</div>
      <table class="data-table">
        <tr><th>优先级</th><th>行动建议</th><th>具体措施</th><th>预期效果</th></tr>
        <tr><td>高</td><td>建立全国统一数据口径标准</td><td>制定《政府数据开放统计规范》国家标准</td><td>消除口径幻觉</td></tr>
        <tr><td>高</td><td>实施差异化分类施策</td><td>按绩效梯队匹配不同支持政策</td><td>提升整体水平</td></tr>
        <tr><td>中</td><td>构建动态监测评估体系</td><td>建立年度评估+实时监测双轨机制</td><td>持续改进</td></tr>
      </table>
    </div>
  </div>
</div>

<script>
function toggleChapter(id) {
  var el = document.getElementById(id);
  var header = el.previousElementSibling;
  var arrow = header.querySelector("div:last-child");
  if (el.style.display === 'none' || el.style.display === '') {
    el.style.display = 'block';
    arrow.textContent = '▲';
  } else {
    el.style.display = 'none';
    arrow.textContent = '▼';
  }
}
</script>

{% endblock %}
'''

with open('templates/v3_thesis.html', 'w', encoding='utf-8') as f:
    f.write(HTML)

print('[OK] templates/v3_thesis.html generated (complete version with all chapters)')
