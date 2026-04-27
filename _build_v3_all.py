#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3 全站生成脚本 - 5个一级页面"""
import sqlite3, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
TMPL = os.path.join(BASE, 'templates')
os.makedirs(TMPL, exist_ok=True)

def db():
    conn = sqlite3.connect(os.path.join(BASE, 'data', 'ogd_database.db'))
    c = conn.cursor()
    c.execute("SELECT COUNT(DISTINCT province) FROM platforms WHERE province IS NOT NULL")
    provinces = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM platforms")
    platforms = c.fetchone()[0]
    c.execute("SELECT name, url, tier, province, platform_type, launch_year FROM platforms ORDER BY province, tier DESC, name")
    plat_list = c.fetchall()
    conn.close()
    return {'provinces': provinces, 'platforms': platforms, 'plat_list': plat_list}

stats = db()

# ===================== base_v3 =====================
with open(os.path.join(TMPL, 'base_v3.html'), 'w', encoding='utf-8') as f:
    f.write('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{% block title %}OGD-Collector Pro{% endblock %}</title>
<style>
:root{--primary:#2563eb;--primary-dark:#1d4ed8;--bg:#f8fafc;--card:#fff;--text:#1e293b;--text-light:#64748b;--border:#e2e8f0;--shadow:0 4px 6px -1px rgba(0,0,0,.07);--radius:12px;--sidebar-w:220px}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.6}
.layout{display:flex;min-height:100vh}
.sidebar{width:var(--sidebar-w);background:linear-gradient(180deg,#1e293b 0%,#0f172a 100%);color:#fff;position:fixed;height:100vh;overflow-y:auto;z-index:100}
.sidebar-header{padding:24px 20px;border-bottom:1px solid rgba(255,255,255,.1)}
.sidebar-header h1{font-size:18px;font-weight:700;letter-spacing:.5px}
.sidebar-header p{font-size:11px;color:#94a3b8;margin-top:4px}
.sidebar-nav{padding:12px 0}
.nav-item{display:flex;align-items:center;padding:12px 20px;color:#cbd5e1;text-decoration:none;font-size:14px;transition:all .2s;border-left:3px solid transparent}
.nav-item:hover{background:rgba(255,255,255,.06);color:#fff}
.nav-item.active{background:rgba(37,99,235,.15);color:#60a5fa;border-left-color:#60a5fa}
.nav-item svg{width:18px;height:18px;margin-right:12px;opacity:.8;flex-shrink:0}
.sidebar-footer{padding:16px 20px;font-size:11px;color:#64748b;border-top:1px solid rgba(255,255,255,.08)}
.main-content{flex:1;margin-left:var(--sidebar-w);min-height:100vh}
.topbar{position:sticky;top:0;background:rgba(248,250,252,.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);padding:12px 32px;z-index:50;display:flex;align-items:center;justify-content:space-between}
.topbar h2{font-size:18px;font-weight:700}
.page-content{padding:24px 32px 48px}
.anchor-nav{display:flex;gap:8px;padding:12px 32px;background:#fff;border-bottom:1px solid var(--border);position:sticky;top:53px;z-index:40;overflow-x:auto;scrollbar-width:none}
.anchor-nav::-webkit-scrollbar{display:none}
.anchor-nav a{color:var(--text-light);text-decoration:none;font-size:13px;padding:6px 14px;border-radius:20px;white-space:nowrap;transition:all .2s}
.anchor-nav a:hover{color:var(--primary);background:#dbeafe}
.anchor-nav a.active{color:#fff;background:var(--primary);font-weight:500}
.card{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);padding:24px;margin-bottom:20px}
.card-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;flex-wrap:wrap;gap:8px}
.card-title{font-size:16px;font-weight:700;display:flex;align-items:center;gap:8px}
.card-title .icon{width:8px;height:8px;border-radius:50%;background:var(--primary)}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin-bottom:24px}
.stat-card{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);padding:20px;text-align:center;transition:transform .2s}
.stat-card:hover{transform:translateY(-2px)}
.stat-value{font-size:32px;font-weight:800;background:linear-gradient(135deg,var(--primary),#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.stat-label{font-size:13px;color:var(--text-light);margin-top:4px}
.data-table{width:100%;border-collapse:collapse;font-size:13px}
.data-table th{background:#f1f5f9;padding:12px 16px;text-align:left;font-weight:600;color:var(--text-light);white-space:nowrap}
.data-table td{padding:10px 16px;border-bottom:1px solid var(--border)}
.data-table tr:hover td{background:#f8fafc}
.badge{display:inline-block;padding:2px 10px;border-radius:10px;font-size:11px;font-weight:600}
.badge-prov{background:#dbeafe;color:#1d4ed8}
.badge-city{background:#d1fae5;color:#065f46}
.timeline{position:relative;padding-left:28px}
.timeline::before{content:"";position:absolute;left:8px;top:4px;bottom:4px;width:2px;background:linear-gradient(180deg,var(--primary),#0f766e)}
.timeline-item{position:relative;margin-bottom:24px}
.timeline-dot{position:absolute;left:-24px;top:4px;width:14px;height:14px;border-radius:50%;background:var(--card);border:3px solid var(--primary)}
.timeline-title{font-weight:700;font-size:14px;margin-bottom:4px}
.timeline-desc{font-size:13px;color:var(--text-light)}
.progress-bar{height:8px;background:#e2e8f0;border-radius:4px;overflow:hidden}
.progress-fill{height:100%;border-radius:4px;background:linear-gradient(90deg,var(--primary),#3b82f6);transition:width 1s ease}
.code-block{background:#0f172a;color:#e2e8f0;border-radius:var(--radius);padding:20px;font-family:monospace;font-size:12px;line-height:1.7;overflow-x:auto;position:relative}
.code-block .lang{position:absolute;top:8px;right:12px;font-size:10px;color:#64748b;text-transform:uppercase}
.code-block .kw{color:#c084fc}
.code-block .str{color:#4ade80}
.code-block .cm{color:#64748b}
.code-block .fn{color:#60a5fa}
.tabs{display:flex;gap:4px;border-bottom:2px solid var(--border);margin-bottom:20px}
.tab-btn{padding:10px 20px;font-size:13px;font-weight:600;color:var(--text-light);background:none;border:none;cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-2px;transition:all .2s}
.tab-btn.active{color:var(--primary);border-bottom-color:var(--primary)}
.tab-panel{display:none}
.tab-panel.active{display:block}
.chapter-tree{display:flex;flex-direction:column;gap:12px}
.chapter-node{display:flex;align-items:flex-start;gap:16px;padding:16px;background:#fff;border-radius:var(--radius);border:1px solid var(--border);transition:all .2s;cursor:pointer}
.chapter-node:hover{border-color:var(--primary);box-shadow:var(--shadow)}
.chapter-num{width:40px;height:40px;border-radius:10px;background:linear-gradient(135deg,var(--primary),#3b82f6);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;flex-shrink:0}
.chapter-info h4{font-size:15px;font-weight:700;margin-bottom:4px}
.chapter-info p{font-size:13px;color:var(--text-light)}
.chapter-tags{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap}
.chapter-tag{font-size:11px;padding:2px 8px;border-radius:4px;background:#f1f5f9;color:var(--text-light)}
.chart-container{background:#fff;border-radius:var(--radius);padding:20px;box-shadow:var(--shadow);margin-bottom:20px}
.chart-title{font-size:14px;font-weight:700;margin-bottom:16px}
.scroll-section{padding-top:60px;margin-top:-60px}
@media(max-width:768px){.sidebar{transform:translateX(-100%)}.main-content{margin-left:0}.stats-grid{grid-template-columns:repeat(2,1fr)}}
</style>
{% block extra_css %}{% endblock %}
</head>
<body>
<div class="layout">
  <aside class="sidebar">
    <div class="sidebar-header"><h1>OGD-Collector</h1><p>政府数据开放平台采集系统</p></div>
    <nav class="sidebar-nav">
      <a href="/v3/" class="nav-item {% if active=='dashboard' %}active{% endif %}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>系统概览</a>
      <a href="/v3/collection" class="nav-item {% if active=='collection' %}active{% endif %}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>采集中心</a>
      <a href="/v3/analysis" class="nav-item {% if active=='analysis' %}active{% endif %}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>分析看板</a>
      <a href="/v3/thesis" class="nav-item {% if active=='thesis' %}active{% endif %}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>论文成果</a>
      <a href="/v3/research" class="nav-item {% if active=='research' %}active{% endif %}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>研究拓展</a>
    </nav>
    <div class="sidebar-footer"><div>v3.0.0 | OGD-Collector Pro</div><div style="margin-top:4px">博士论文支撑系统</div></div>
  </aside>
  <main class="main-content">
    <div class="topbar"><h2>{% block page_title %}系统概览{% endblock %}</h2><div class="breadcrumb">OGD-Collector Pro / {% block breadcrumb %}系统概览{% endblock %}</div></div>
    {% block anchor_nav %}{% endblock %}
    <div class="page-content">{% block content %}{% endblock %}</div>
  </main>
</div>
<script>
document.addEventListener('scroll',function(){
  const sections=document.querySelectorAll('.scroll-section');
  const navLinks=document.querySelectorAll('.anchor-nav a');
  let current='';
  sections.forEach(function(sec){if(sec.getBoundingClientRect().top<=120) current=sec.id});
  navLinks.forEach(function(link){link.classList.toggle('active', link.getAttribute('href')==='#'+current)});
});
document.querySelectorAll('.tabs').forEach(function(tc){
  const btns=tc.querySelectorAll('.tab-btn');
  const panels=tc.parentElement.querySelectorAll('.tab-panel');
  btns.forEach(function(btn,idx){btn.addEventListener('click',function(){btns.forEach(function(b){b.classList.remove('active')});panels.forEach(function(p){p.classList.remove('active')});btn.classList.add('active');panels[idx].classList.add('active')})});
});
</script>
{% block extra_js %}{% endblock %}
</body>
</html>
''')

print("base_v3.html 生成完成")

# ===================== v3_dashboard =====================
with open(os.path.join(TMPL, 'v3_dashboard.html'), 'w', encoding='utf-8') as f:
    f.write('''{% extends "base_v3.html" %}{% set active = "dashboard" %}{% block title %}系统概览 - OGD-Collector Pro{% endblock %}{% block page_title %}系统概览{% endblock %}{% block breadcrumb %}系统概览{% endblock %}
{% block anchor_nav %}<div class="anchor-nav"><a href="#overview" class="active">数据规模</a><a href="#roadmap">技术路线</a><a href="#architecture">系统架构</a><a href="#highlights">核心亮点</a></div>{% endblock %}
{% block content %}
<div id="overview" class="scroll-section">
  <div class="card-header"><div class="card-title"><span class="icon"></span>数据规模总览</div></div>
  <div class="stats-grid">
    <div class="stat-card"><div class="stat-value">88</div><div class="stat-label">政府数据开放平台</div><div style="font-size:12px;color:#16a34a;margin-top:4px">覆盖31个省级行政区</div></div>
    <div class="stat-card"><div class="stat-value">31</div><div class="stat-label">省级行政区</div><div style="font-size:12px;color:#16a34a;margin-top:4px">含22省+5自治区+4直辖市</div></div>
    <div class="stat-card"><div class="stat-value">''' + str(stats['platforms']) + '''</div><div class="stat-label">平台总数</div><div style="font-size:12px;color:#16a34a;margin-top:4px">省/副省/地市三级</div></div>
    <div class="stat-card"><div class="stat-value">6</div><div class="stat-label">评估方法论</div><div style="font-size:12px;color:#16a34a;margin-top:4px">4E/TOPSIS/DEA/DEMATEL/fsQCA/DID</div></div>
  </div>
  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>平台层级分布</div></div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px">
      <div><div style="display:flex;justify-content:space-between;margin-bottom:6px;font-size:13px"><span>省级平台</span><span style="font-weight:700">31个</span></div><div class="progress-bar"><div class="progress-fill" style="width:35%"></div></div></div>
      <div><div style="display:flex;justify-content:space-between;margin-bottom:6px;font-size:13px"><span>副省级/省会城市</span><span style="font-weight:700">25个</span></div><div class="progress-bar"><div class="progress-fill" style="width:28%"></div></div></div>
      <div><div style="display:flex;justify-content:space-between;margin-bottom:6px;font-size:13px"><span>地级市平台</span><span style="font-weight:700">32个</span></div><div class="progress-bar"><div class="progress-fill" style="width:36%"></div></div></div>
    </div>
  </div>
  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>数据采集时间轴</div></div>
    <div class="timeline">
      <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2023.03 项目启动</div><div class="timeline-desc">确定研究目标，搭建基础采集框架</div></div>
      <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2023.06 首轮采集</div><div class="timeline-desc">完成31个省级平台全覆盖采集</div></div>
      <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2023.09 市级拓展</div><div class="timeline-desc">补充57个副省级/地级市平台，总数达88个</div></div>
      <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2024.01 数据清洗</div><div class="timeline-desc">完成去重、格式统一、缺失值处理</div></div>
      <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2024.06 多方法分析</div><div class="timeline-desc">完成TOPSIS/DEA/DEMATEL/fsQCA/DID全方法链分析</div></div>
      <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2025.04 系统上线</div><div class="timeline-desc">OGD-Collector Pro v3 可视化平台部署</div></div>
    </div>
  </div>
</div>

<div id="roadmap" class="scroll-section">
  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>研究技术路线图</div></div>
    <div style="overflow-x:auto">
      <svg viewBox="0 0 1000 420" style="width:100%;min-width:900px">
        <rect x="0" y="0" width="1000" height="420" fill="#f8fafc" rx="12"/>
        <rect x="40" y="30" width="200" height="70" fill="#dbeafe" stroke="#2563eb" stroke-width="2" rx="8"/><text x="140" y="58" text-anchor="middle" font-size="14" font-weight="700" fill="#1e40af">数据采集层</text><text x="140" y="78" text-anchor="middle" font-size="10" fill="#3b82f6">Requests + BeautifulSoup</text><text x="140" y="92" text-anchor="middle" font-size="9" fill="#64748b">动态/静态页面自适应</text>
        <rect x="280" y="30" width="200" height="70" fill="#d1fae5" stroke="#059669" stroke-width="2" rx="8"/><text x="380" y="58" text-anchor="middle" font-size="14" font-weight="700" fill="#065f46">数据存储层</text><text x="380" y="78" text-anchor="middle" font-size="10" fill="#10b981">SQLite + JSON + CSV</text><text x="380" y="92" text-anchor="middle" font-size="9" fill="#64748b">多格式持久化存储</text>
        <rect x="520" y="30" width="200" height="70" fill="#fef3c7" stroke="#d97706" stroke-width="2" rx="8"/><text x="620" y="58" text-anchor="middle" font-size="14" font-weight="700" fill="#92400e">评估体系层</text><text x="620" y="78" text-anchor="middle" font-size="10" fill="#f59e0b">4E框架 + 5种方法</text><text x="620" y="92" text-anchor="middle" font-size="9" fill="#64748b">TOPSIS/DEA/DEMATEL/fsQCA/DID</text>
        <rect x="760" y="30" width="200" height="70" fill="#fce7f3" stroke="#db2777" stroke-width="2" rx="8"/><text x="860" y="58" text-anchor="middle" font-size="14" font-weight="700" fill="#9d174d">可视化层</text><text x="860" y="78" text-anchor="middle" font-size="10" fill="#ec4899">Flask + ECharts + D3.js</text><text x="860" y="92" text-anchor="middle" font-size="9" fill="#64748b">交互式图表展示</text>
        <defs><marker id="ar" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#94a3b8"/></marker></defs>
        <path d="M 240 65 L 280 65" stroke="#94a3b8" stroke-width="2" marker-end="url(#ar)"/>
        <path d="M 480 65 L 520 65" stroke="#94a3b8" stroke-width="2" marker-end="url(#ar)"/>
        <path d="M 720 65 L 760 65" stroke="#94a3b8" stroke-width="2" marker-end="url(#ar)"/>
        <rect x="40" y="130" width="120" height="45" fill="#eff6ff" stroke="#93c5fd" stroke-width="1" rx="6"/><text x="100" y="157" text-anchor="middle" font-size="11" fill="#1d4ed8">URL发现与解析</text>
        <rect x="40" y="185" width="120" height="45" fill="#eff6ff" stroke="#93c5fd" stroke-width="1" rx="6"/><text x="100" y="212" text-anchor="middle" font-size="11" fill="#1d4ed8">页面结构识别</text>
        <rect x="40" y="240" width="120" height="45" fill="#eff6ff" stroke="#93c5fd" stroke-width="1" rx="6"/><text x="100" y="267" text-anchor="middle" font-size="11" fill="#1d4ed8">数据提取与清洗</text>
        <rect x="280" y="130" width="120" height="45" fill="#ecfdf5" stroke="#6ee7b7" stroke-width="1" rx="6"/><text x="340" y="157" text-anchor="middle" font-size="11" fill="#065f46">元数据标准化</text>
        <rect x="280" y="185" width="120" height="45" fill="#ecfdf5" stroke="#6ee7b7" stroke-width="1" rx="6"/><text x="340" y="212" text-anchor="middle" font-size="11" fill="#065f46">多表关联设计</text>
        <rect x="280" y="240" width="120" height="45" fill="#ecfdf5" stroke="#6ee7b7" stroke-width="1" rx="6"/><text x="340" y="267" text-anchor="middle" font-size="11" fill="#065f46">增量更新机制</text>
        <rect x="520" y="130" width="120" height="45" fill="#fffbeb" stroke="#fcd34d" stroke-width="1" rx="6"/><text x="580" y="157" text-anchor="middle" font-size="11" fill="#92400e">4E指标体系构建</text>
        <rect x="520" y="185" width="120" height="45" fill="#fffbeb" stroke="#fcd34d" stroke-width="1" rx="6"/><text x="580" y="212" text-anchor="middle" font-size="11" fill="#92400e">多方法融合分析</text>
        <rect x="520" y="240" width="120" height="45" fill="#fffbeb" stroke="#fcd34d" stroke-width="1" rx="6"/><text x="580" y="267" text-anchor="middle" font-size="11" fill="#92400e">因果路径挖掘</text>
        <rect x="760" y="130" width="120" height="45" fill="#fdf2f8" stroke="#f9a8d4" stroke-width="1" rx="6"/><text x="820" y="157" text-anchor="middle" font-size="11" fill="#9d174d">排名可视化</text>
        <rect x="760" y="185" width="120" height="45" fill="#fdf2f8" stroke="#f9a8d4" stroke-width="1" rx="6"/><text x="820" y="212" text-anchor="middle" font-size="11" fill="#9d174d">网络关系图</text>
        <rect x="760" y="240" width="120" height="45" fill="#fdf2f8" stroke="#f9a8d4" stroke-width="1" rx="6"/><text x="820" y="267" text-anchor="middle" font-size="11" fill="#9d174d">政策效应展示</text>
        <line x1="100" y1="100" x2="100" y2="130" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="4"/>
        <line x1="340" y1="100" x2="340" y2="130" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="4"/>
        <line x1="580" y1="100" x2="580" y2="130" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="4"/>
        <line x1="820" y1="100" x2="820" y2="130" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="4"/>
        <rect x="40" y="320" width="920" height="70" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1" rx="8"/>
        <text x="500" y="348" text-anchor="middle" font-size="13" font-weight="700" fill="#334155">底层技术支撑</text>
        <text x="180" y="372" text-anchor="middle" font-size="11" fill="#64748b">Python 3.11 + Flask</text>
        <text x="380" y="372" text-anchor="middle" font-size="11" fill="#64748b">SQLite + APScheduler</text>
        <text x="580" y="372" text-anchor="middle" font-size="11" fill="#64748b">ECharts + D3.js</text>
        <text x="780" y="372" text-anchor="middle" font-size="11" fill="#64748b">腾讯云服务器部署</text>
      </svg>
    </div>
  </div>
</div>

<div id="architecture" class="scroll-section">
  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>系统技术架构</div></div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px">
      <div style="padding:16px;background:#f8fafc;border-radius:8px"><div style="font-weight:700;margin-bottom:8px;color:#2563eb">采集引擎</div><div style="font-size:13px;color:#64748b;line-height:1.8">• 动态请求：Selenium + ChromeDriver<br>• 静态解析：Requests + BeautifulSoup4<br>• 反爬策略：随机UA + 代理池 + 频率控制<br>• 容错机制：自动重试 + 异常捕获 + 断点续采</div></div>
      <div style="padding:16px;background:#f8fafc;border-radius:8px"><div style="font-weight:700;margin-bottom:8px;color:#059669">数据治理</div><div style="font-size:13px;color:#64748b;line-height:1.8">• 存储层：SQLite + JSON + CSV<br>• 清洗流程：去重 → 标准化 → 校验 → 关联<br>• 版本管理：Git + 数据库快照<br>• 增量更新：哈希比对 + 时间戳追踪</div></div>
      <div style="padding:16px;background:#f8fafc;border-radius:8px"><div style="font-weight:700;margin-bottom:8px;color:#d97706">分析引擎</div><div style="font-size:13px;color:#64748b;line-height:1.8">• 排名分析：TOPSIS（逼近理想解）<br>• 效率评估：DEA（数据包络分析）<br>• 因果挖掘：DEMATEL（决策试验法）<br>• 路径分析：fsQCA（模糊集定性比较）<br>• 政策评估：DID（双重差分法）</div></div>
      <div style="padding:16px;background:#f8fafc;border-radius:8px"><div style="font-weight:700;margin-bottom:8px;color:#db2777">展示层</div><div style="font-size:13px;color:#64748b;line-height:1.8">• 后端框架：Flask + Jinja2 模板<br>• 前端图表：ECharts 5.x + D3.js 7.x<br>• 响应式布局：CSS Grid + Flexbox<br>• 部署环境：腾讯云 + Nginx + Gunicorn</div></div>
    </div>
  </div>
</div>

<div id="highlights" class="scroll-section">
  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>核心亮点与创新</div></div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px">
      <div class="card" style="margin:0;border-left:4px solid #2563eb"><div style="font-weight:700;margin-bottom:8px">多层级全覆盖</div><div style="font-size:13px;color:#64748b">全国31个省级行政区、88个政府数据开放平台全覆盖采集，包括省级、副省级、地级市三级平台。</div></div>
      <div class="card" style="margin:0;border-left:4px solid #059669"><div style="font-weight:700;margin-bottom:8px">方法链创新</div><div style="font-size:13px;color:#64748b">首创"TOPSIS→DEA→DEMATEL→fsQCA→DID"五方法递进分析链，实现从排名到因果的全链条解释。</div></div>
      <div class="card" style="margin:0;border-left:4px solid #d97706"><div style="font-weight:700;margin-bottom:8px">自适应采集</div><div style="font-size:13px;color:#64748b">针对不同平台技术架构差异（静态/动态/接口），实现自适应采集策略，覆盖率达100%。</div></div>
      <div class="card" style="margin:0;border-left:4px solid #db2777"><div style="font-weight:700;margin-bottom:8px">政策因果推断</div><div style="font-size:13px;color:#64748b">首次将DID方法应用于数据开放平台政策效应评估，量化"数据二十条"等政策的实际影响。</div></div>
    </div>
  </div>
</div>
{% endblock %}''')

print("v3_dashboard.html 生成完成")
