#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
TMPL = os.path.join(os.path.dirname(__file__), 'templates')

html = '''{% extends "base_v3.html" %}{% set active = "research" %}{% block title %}研究拓展 - OGD-Collector Pro{% endblock %}{% block page_title %}研究拓展{% endblock %}{% block breadcrumb %}研究拓展{% endblock %}
{% block anchor_nav %}<div class="anchor-nav"><a href="#central" class="active">中央级网站</a><a href="#plans">拓展计划</a><a href="#other">其他成果</a><a href="#cooperation">合作交流</a></div>{% endblock %}
{% block content %}

<div id="central" class="scroll-section">
  <div class="card">
    <div class="card-header"><div class="card-title"><span class="icon"></span>中央级政府网站数据分析</div></div>
    <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:16px">
      <p>在省级平台研究基础上，本研究方向正逐步向中央级政府网站拓展。中央级平台（如国家数据局官网、国务院数据开放平台等）具有更高的政策权威性和数据汇聚能力，是理解国家数据治理战略的重要窗口。</p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px">
      <div class="card" style="margin:0;border-left:4px solid #2563eb">
        <div style="font-weight:700;margin-bottom:8px">国家数据局</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8">
          <strong>网址：</strong>https://www.nda.gov.cn<br>
          <strong>定位：</strong>全国数据要素市场化配置的核心统筹机构<br>
          <strong>研究价值：</strong>政策发布源头、标准制定主体、跨区域协调中枢<br>
          <strong>分析维度：</strong>政策文本演化、标准规范体系、地方落实情况
        </div>
      </div>
      <div class="card" style="margin:0;border-left:4px solid #059669">
        <div style="font-weight:700;margin-bottom:8px">国家政务服务平台</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8">
          <strong>网址：</strong>https://www.gov.cn<br>
          <strong>定位：</strong>国务院统一政务服务平台<br>
          <strong>研究价值：</strong>跨部门数据共享进展、政务服务一体化程度<br>
          <strong>分析维度：</strong>部门接入数、数据共享清单、服务事项覆盖
        </div>
      </div>
      <div class="card" style="margin:0;border-left:4px solid #d97706">
        <div style="font-weight:700;margin-bottom:8px">全国一体化政务大数据体系</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8">
          <strong>定位：</strong>《全国一体化政务大数据体系建设指南》落地载体<br>
          <strong>研究价值：</strong>国家-省-市三级数据共享交换机制<br>
          <strong>分析维度：</strong>共享目录规模、交换频率、数据质量报告
        </div>
      </div>
    </div>
  </div>
</div>

<div id="plans" class="scroll-section">
  <div class="card">
    <div class="card-header"><div class="card-title"><span class="icon"></span>未来拓展计划</div></div>
    <div class="timeline">
      <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">Phase 1: 中央级平台纳入（2025 Q3）</div><div class="timeline-desc">将国家数据局、国家政务服务平台等中央级网站纳入采集范围，建立国家-省两级分析框架</div></div>
      <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">Phase 2: 国际比较研究（2025 Q4）</div><div class="timeline-desc">采集美国 data.gov、英国 data.gov.uk、欧盟 data.europa.eu 等国际平台数据，开展跨国比较分析</div></div>
      <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">Phase 3: 实时监测体系（2026 Q1）</div><div class="timeline-desc">建立平台健康度实时监测系统，自动追踪平台更新频率、数据集增长、接口可用性等指标</div></div>
      <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">Phase 4: 大模型应用（2026 Q2）</div><div class="timeline-desc">探索将LLM技术应用于政策文本分析、用户评论情感分析、数据需求智能识别等场景</div></div>
    </div>
  </div>
</div>

<div id="other" class="scroll-section">
  <div class="card">
    <div class="card-header"><div class="card-title"><span class="icon"></span>其他研究成果</div></div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px">
      <div class="card" style="margin:0">
        <div style="font-weight:700;margin-bottom:8px;color:#2563eb">数据集质量评估模型</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8">构建了包含完整性、准确性、时效性、可用性、规范性五个维度的数据集质量评估指标体系，可用于自动化评估任意政府数据集的质量等级。</div>
      </div>
      <div class="card" style="margin:0">
        <div style="font-weight:700;margin-bottom:8px;color:#059669">平台成熟度评估工具</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8">开发了基于五阶段成熟度模型（初始级→可重复级→定义级→管理级→优化级）的在线评估工具，可为各平台提供诊断报告和改进建议。</div>
      </div>
      <div class="card" style="margin:0">
        <div style="font-weight:700;margin-bottom:8px;color:#d97706">开放数据利用案例库</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8">收集整理了国内外100+个政府开放数据创新应用案例，涵盖交通、环境、医疗、金融等多个领域，为数据利用方提供参考。</div>
      </div>
      <div class="card" style="margin:0">
        <div style="font-weight:700;margin-bottom:8px;color:#db2777">数据采集规范指南</div>
        <div style="font-size:13px;color:#64748b;line-height:1.8">编写了《政府数据开放平台数据采集技术规范》，涵盖采集伦理、技术方案、质量控制、数据安全等方面，已通过GitHub开源。</div>
      </div>
    </div>
  </div>
</div>

<div id="cooperation" class="scroll-section">
  <div class="card">
    <div class="card-header"><div class="card-title"><span class="icon"></span>合作交流与开源</div></div>
    <div style="padding:24px;background:linear-gradient(135deg,#eff6ff,#dbeafe);border-radius:8px;text-align:center">
      <div style="font-size:18px;font-weight:700;color:#1e40af;margin-bottom:12px">开放合作，共建共享</div>
      <div style="font-size:13px;color:#3b82f6;max-width:600px;margin:0 auto;line-height:1.8">
        本研究所有数据、代码、文档均已开源。欢迎学术界、业界同仁参与合作，共同推进中国政府数据开放研究。
      </div>
      <div style="margin-top:20px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
        <a href="https://github.com/disijingjie/ogd-collector-pro" target="_blank" style="display:inline-flex;background:#2563eb;color:#fff;padding:10px 24px;border-radius:8px;text-decoration:none;font-weight:600">GitHub 仓库</a>
        <a href="/v3/" style="display:inline-flex;background:#fff;color:#2563eb;border:1px solid #2563eb;padding:10px 24px;border-radius:8px;text-decoration:none;font-weight:600">返回系统概览</a>
      </div>
    </div>
    <div style="margin-top:20px">
      <div style="font-weight:700;margin-bottom:12px">联系方式</div>
      <div style="font-size:13px;color:#64748b;line-height:1.8">
        <p>• 项目地址：https://github.com/disijingjie/ogd-collector-pro</p>
        <p>• 数据集下载：可通过GitHub Releases获取完整数据集</p>
        <p>• 问题反馈：请在GitHub Issues中提交</p>
        <p>• 学术引用：请引用博士论文正式发表版本</p>
      </div>
    </div>
  </div>
</div>
{% endblock %}'''

with open(os.path.join(TMPL, 'v3_research.html'), 'w', encoding='utf-8') as f:
    f.write(html)
print('v3_research.html OK')
