import sqlite3, html

conn = sqlite3.connect('data/ogd_database.db')
c = conn.cursor()

# 1. 获取数据来源记录
c.execute("""
    SELECT source_name, source_type, access_method, data_start_date, data_end_date, data_format, record_count, cited_in_chapter
    FROM data_provenance WHERE is_active=1 ORDER BY id
""")
provenance = c.fetchall()

# 2. 获取最新采集任务
c.execute("""
    SELECT task_name, task_type, status, total_count, success_count, started_at
    FROM collection_tasks ORDER BY id DESC LIMIT 1
""")
latest_task = c.fetchone()

# 3. 获取最近5条日志
c.execute("""
    SELECT log_level, message, created_at FROM collection_logs ORDER BY id DESC LIMIT 5
""")
logs = c.fetchall()

# 4. 获取平台统计
c.execute("SELECT COUNT(*) FROM platforms")
plat_count = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM collection_records WHERE status='success'")
success_count = c.fetchone()[0]

conn.close()

# 构建数据来源表格
prov_rows = ""
for p in provenance:
    name, stype, method, start, end, fmt, count, chapter = p
    safe_name = html.escape(str(name)) if name else ""
    safe_method = html.escape(str(method)) if method else ""
    safe_chapter = html.escape(str(chapter)) if chapter else "未引用"
    count_str = f"{count}条" if count else "-"
    date_range = f"{start}~{end}" if start and end else (start or end or "-")
    prov_rows += f'<tr><td>{safe_name}</td><td>{stype or "-"}</td><td>{safe_method}</td><td>{date_range}</td><td>{fmt or "-"}</td><td>{count_str}</td><td><span class="badge" style="background:#dbeafe;color:#1d4ed8">{safe_chapter}</span></td></tr>'

# 构建日志行
log_html = ""
for log in logs:
    level, msg, created = log
    level_class = "badge-prov" if level == "INFO" else "badge-city"
    safe_msg = html.escape(str(msg)[:60]) if msg else ""
    safe_time = str(created)[:19] if created else ""
    log_html += f'<tr><td><span class="badge {level_class}">{level}</span></td><td style="font-size:12px">{safe_msg}</td><td style="font-size:12px;color:#64748b">{safe_time}</td></tr>'

# 最新任务信息
task_info = ""
if latest_task:
    tname, ttype, status, total, success, started = latest_task
    ttype_label = "全量" if ttype == "full" else "增量"
    status_label = "完成" if status == "completed" else "进行中"
    status_color = "#16a34a" if status == "completed" else "#d97706"
    task_info = f'<div style="display:flex;gap:16px;flex-wrap:wrap"><div style="padding:12px 20px;background:#f8fafc;border-radius:8px"><div style="font-size:12px;color:#64748b">最近任务</div><div style="font-weight:700">{tname}</div></div><div style="padding:12px 20px;background:#f8fafc;border-radius:8px"><div style="font-size:12px;color:#64748b">类型</div><div style="font-weight:700">{ttype_label}</div></div><div style="padding:12px 20px;background:#f8fafc;border-radius:8px"><div style="font-size:12px;color:#64748b">状态</div><div style="font-weight:700;color:{status_color}">{status_label}</div></div><div style="padding:12px 20px;background:#f8fafc;border-radius:8px"><div style="font-size:12px;color:#64748b">成功/总数</div><div style="font-weight:700">{success}/{total}</div></div><div style="padding:12px 20px;background:#f8fafc;border-radius:8px"><div style="font-size:12px;color:#64748b">启动时间</div><div style="font-weight:700">{str(started)[:16]}</div></div></div>'

content = f'''{{% extends "base_v3.html" %}}{{% set active = "collection" %}}{{% block title %}}采集中心 - OGD-Collector Pro{{% endblock %}}{{% block page_title %}}采集中心{{% endblock %}}{{% block breadcrumb %}}采集中心{{% endblock %}}
{{% block anchor_nav %}}<div class="anchor-nav"><a href="#purpose" class="active">采集目的</a><a href="#strategy">采集策略</a><a href="#provenance">数据来源</a><a href="#standard">标准化</a><a href="#recollect">复现</a></div>{{% endblock %}}
{{% block content %}}

<!-- 板块1: 采集目的与范围 -->
<div id="purpose" class="scroll-section">
  <div style="padding:24px;background:linear-gradient(135deg,#1e293b,#334155);border-radius:12px;color:#fff;margin-bottom:20px">
    <div style="font-size:14px;opacity:0.8;margin-bottom:8px">OGD-Collector Pro / 数据采集</div>
    <div style="font-size:22px;font-weight:800;margin-bottom:12px">为政府数据开放绩效评估研究提供标准化数据基础</div>
    <div style="font-size:13px;opacity:0.9;line-height:1.8;max-width:700px">
      本系统为全国31个省级政府数据开放平台（88个平台）提供自动化数据采集、标准化处理与质量校验，
      获取数据集元数据（名称、格式、部门、更新日期、下载量等）作为博士论文实证分析的输入数据。
    </div>
  </div>

  <div class="stats-grid" style="margin-bottom:20px">
    <div class="stat-card"><div class="stat-value">{plat_count}</div><div class="stat-label">采集平台</div><div style="font-size:12px;color:#16a34a">省/副省/地市三级</div></div>
    <div class="stat-card"><div class="stat-value">31</div><div class="stat-label">覆盖省份</div><div style="font-size:12px;color:#16a34a">全国全覆盖</div></div>
    <div class="stat-card"><div class="stat-value">{success_count}</div><div class="stat-label">成功采集</div><div style="font-size:12px;color:#16a34a">平台记录入库</div></div>
    <div class="stat-card"><div class="stat-value">2023-2026</div><div class="stat-label">采集周期</div><div style="font-size:12px;color:#16a34a">持续更新维护</div></div>
  </div>

  <div class="card">
    <div class="card-header"><div class="card-title"><span class="icon"></span>全国31省覆盖图</div></div>
    <div style="text-align:center;padding:10px"><img src="/static/charts/fig4_1_province_map.png" style="max-width:100%;border-radius:8px" alt="全国31省覆盖图"></div>
    <div style="font-size:12px;color:#64748b;text-align:center;margin-top:8px">颜色深浅表示平台绩效水平（基于TOPSIS综合得分）</div>
  </div>

  <div class="card" style="margin-top:16px">
    <div class="card-header"><div class="card-title"><span class="icon"></span>最新采集状态</div></div>
    {task_info}
  </div>
</div>

<!-- 板块2: 采集策略与方法 -->
<div id="strategy" class="scroll-section">
  <div class="card">
    <div class="card-header"><div class="card-title"><span class="icon"></span>采集策略：按平台技术架构自适应选择方法</div></div>
    <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:16px">
      不同省份的政府数据开放平台采用不同的技术架构，本系统通过发送HEAD请求识别页面类型，自动选择最优采集策略，确保88个平台100%覆盖。
    </div>
    <div style="overflow-x:auto">
      <table class="data-table">
        <tr><th>平台类型</th><th>代表省份</th><th>技术特征</th><th>采集方法</th><th>选择理由</th></tr>
        <tr><td><span class="badge badge-prov">静态页面型</span></td><td>山东、浙江、广东</td><td>HTML服务器端渲染</td><td>Requests + BeautifulSoup</td><td>响应快、结构稳定、易于解析</td></tr>
        <tr><td><span class="badge badge-city">动态渲染型</span></td><td>北京、上海、四川</td><td>Vue/React异步加载</td><td>Selenium + ChromeDriver</td><td>需等待JS渲染完成</td></tr>
        <tr><td><span class="badge badge-api">接口API型</span></td><td>贵州、福建、深圳</td><td>RESTful JSON返回</td><td>直接调用API端点</td><td>数据结构规范、易于批量获取</td></tr>
        <tr><td><span class="badge" style="background:#fce7f3;color:#9d174d">混合型</span></td><td>部分中西部市级</td><td>静态+动态+下载</td><td>组合策略</td><td>需定制化解析规则</td></tr>
      </table>
    </div>
    <div style="margin-top:20px">
      <div style="font-weight:700;margin-bottom:12px">四步采集流程</div>
      <div style="overflow-x:auto">
        <svg viewBox="0 0 800 100" style="width:100%;min-width:600px">
          <rect x="0" y="15" width="160" height="70" fill="#dbeafe" stroke="#2563eb" stroke-width="2" rx="8"/>
          <text x="80" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="#1e40af">1. 平台识别</text>
          <text x="80" y="60" text-anchor="middle" font-size="9" fill="#64748b">HEAD请求探测</text>
          <text x="80" y="74" text-anchor="middle" font-size="9" fill="#64748b">识别技术架构</text>

          <rect x="210" y="15" width="160" height="70" fill="#d1fae5" stroke="#059669" stroke-width="2" rx="8"/>
          <text x="290" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="#065f46">2. 方法选择</text>
          <text x="290" y="60" text-anchor="middle" font-size="9" fill="#64748b">静态/动态/API</text>
          <text x="290" y="74" text-anchor="middle" font-size="9" fill="#64748b">自适应匹配</text>

          <rect x="420" y="15" width="160" height="70" fill="#fef3c7" stroke="#d97706" stroke-width="2" rx="8"/>
          <text x="500" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="#92400e">3. 元数据提取</text>
          <text x="500" y="60" text-anchor="middle" font-size="9" fill="#64748b">8个核心字段</text>
          <text x="500" y="74" text-anchor="middle" font-size="9" fill="#64748b">名称/格式/部门/日期</text>

          <rect x="630" y="15" width="160" height="70" fill="#f3e8ff" stroke="#9333ea" stroke-width="2" rx="8"/>
          <text x="710" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="#7e22ce">4. 质量校验</text>
          <text x="710" y="60" text-anchor="middle" font-size="9" fill="#64748b">完整性/一致性</text>
          <text x="710" y="74" text-anchor="middle" font-size="9" fill="#64748b">时效性/可用性</text>

          <defs><marker id="ar" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#94a3b8"/></marker></defs>
          <line x1="160" y1="50" x2="210" y2="50" stroke="#94a3b8" stroke-width="2" marker-end="url(#ar)"/>
          <line x1="370" y1="50" x2="420" y2="50" stroke="#94a3b8" stroke-width="2" marker-end="url(#ar)"/>
          <line x1="580" y1="50" x2="630" y2="50" stroke="#94a3b8" stroke-width="2" marker-end="url(#ar)"/>
        </svg>
      </div>
    </div>
    <div style="margin-top:16px;padding:16px;background:#f0f9ff;border-radius:8px">
      <div style="font-weight:700;margin-bottom:8px;color:#0369a1">核心采集逻辑</div>
      <div style="font-size:12px;color:#64748b;line-height:1.8;font-family:monospace;background:#f8fafc;padding:12px;border-radius:6px">
def collect(platform):
    page_type = detect_page_type(platform.url)  # HEAD请求识别
    if page_type == 'static':
        return static_collect(platform)         # BeautifulSoup解析
    elif page_type == 'dynamic':
        return dynamic_collect(platform)        # Selenium渲染
    elif page_type == 'api':
        return api_collect(platform)            # RESTful调用
    else:
        return hybrid_collect(platform)         # 组合策略
      </div>
    </div>
  </div>
</div>

<!-- 板块3: 数据来源总览 -->
<div id="provenance" class="scroll-section">
  <div class="card">
    <div class="card-header"><div class="card-title"><span class="icon"></span>博士论文数据来源总览</div><div style="font-size:12px;color:#64748b">所有数据来源均可追溯、可验证、可复现</div></div>
    <div style="overflow-x:auto">
      <table class="data-table">
        <tr><th>来源名称</th><th>来源类型</th><th>采集方法</th><th>数据时间范围</th><th>数据格式</th><th>记录数</th><th>引用章节</th></tr>
        {prov_rows}
      </table>
    </div>
    <div style="margin-top:20px;padding:16px;background:#f8fafc;border-radius:8px">
      <div style="font-weight:700;margin-bottom:12px">数据采集时间线</div>
      <div class="timeline">
        <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2023.03 项目启动</div><div class="timeline-desc">确定研究问题，构建4E理论框架，设计五方法递进分析链</div></div>
        <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2023.06 首轮省级采集</div><div class="timeline-desc">完成31个省级平台全覆盖采集，采用Requests+BeautifulSoup静态解析为主</div></div>
        <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2023.09 市级拓展</div><div class="timeline-desc">补充57个副省级/地级市平台，北京/上海等采用Selenium动态渲染</div></div>
        <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2023.12 数据清洗（一）</div><div class="timeline-desc">URL哈希去重、格式统一映射、日期标准化为ISO 8601</div></div>
        <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2024.03 数据清洗（二）</div><div class="timeline-desc">部门名称标准化（GB/T 2260）、缺失值处理、异常值检测</div></div>
        <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2024.06 统一指标构建</div><div class="timeline-desc">原始元数据映射为4E框架16个二级指标，形成标准化评估矩阵</div></div>
        <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2024.09-2025.04 多方法分析</div><div class="timeline-desc">依次完成TOPSIS、DEA、DEMATEL、fsQCA、DID五方法分析</div></div>
      </div>
    </div>
  </div>
</div>

<!-- 板块4: 数据标准化过程 -->
<div id="standard" class="scroll-section">
  <div class="card">
    <div class="card-header"><div class="card-title"><span class="icon"></span>数据标准化过程：从原始数据到统一指标</div></div>
    <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:16px">
      原始采集数据来自88个政府数据开放平台，各平台的元数据字段命名、格式、分类体系存在显著差异。本研究通过<strong>四步标准化流程</strong>将其转化为可直接用于实证分析的标准化数据集。
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-bottom:20px">
      <div style="padding:16px;background:#f8fafc;border-radius:8px;border-left:4px solid #2563eb">
        <div style="font-weight:700;margin-bottom:6px">Step 1: 字段映射</div>
        <div style="font-size:12px;color:#64748b;line-height:1.8">
          将各平台不同的字段名映射到统一标准。<br>
          "数据集名称"/"资源标题"/"name" → <strong>dataset_title</strong><br>
          "更新日期"/"发布时间"/"update_time" → <strong>update_date</strong>
        </div>
      </div>
      <div style="padding:16px;background:#f8fafc;border-radius:8px;border-left:4px solid #059669">
        <div style="font-weight:700;margin-bottom:6px">Step 2: 分类统一</div>
        <div style="font-size:12px;color:#64748b;line-height:1.8">
          各平台分类标签不一致（"交通"vs"交通运输"），采用<strong>关键词匹配+人工校验</strong>统一为12个一级主题。
        </div>
      </div>
      <div style="padding:16px;background:#f8fafc;border-radius:8px;border-left:4px solid #d97706">
        <div style="font-weight:700;margin-bottom:6px">Step 3: 格式规范</div>
        <div style="font-size:12px;color:#64748b;line-height:1.8">
          CSV/Excel/XLS/XLSX → <strong>表格</strong><br>
          JSON/XML/API → <strong>接口</strong><br>
          PDF/DOC → <strong>文档</strong><br>
          SHP/GeoJSON → <strong>地理</strong>
        </div>
      </div>
      <div style="padding:16px;background:#f8fafc;border-radius:8px;border-left:4px solid #db2777">
        <div style="font-weight:700;margin-bottom:6px">Step 4: 质量校验</div>
        <div style="font-size:12px;color:#64748b;line-height:1.8">
          完整性：必填字段缺失率&lt;20%<br>
          一致性：省份-平台关联正确性100%<br>
          时效性：近2年内更新<br>
          可用性：下载链接可访问
        </div>
      </div>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px">
      <div style="padding:16px;background:#eff6ff;border-radius:8px;text-align:center">
        <div style="font-size:28px;font-weight:800;color:#2563eb">88</div>
        <div style="font-size:12px;color:#64748b">原始采集平台数</div>
      </div>
      <div style="padding:16px;background:#ecfdf5;border-radius:8px;text-align:center">
        <div style="font-size:28px;font-weight:800;color:#059669">100%</div>
        <div style="font-size:12px;color:#64748b">字段映射覆盖率</div>
      </div>
      <div style="padding:16px;background:#fffbeb;border-radius:8px;text-align:center">
        <div style="font-size:28px;font-weight:800;color:#d97706">12</div>
        <div style="font-size:12px;color:#64748b">统一主题分类数</div>
      </div>
      <div style="padding:16px;background:#fdf2f8;border-radius:8px;text-align:center">
        <div style="font-size:28px;font-weight:800;color:#db2777">4E</div>
        <div style="font-size:12px;color:#64748b">评估维度框架</div>
      </div>
    </div>
  </div>
</div>

<!-- 板块5: 数据集与复现 -->
<div id="recollect" class="scroll-section">
  <div class="card">
    <div class="card-header"><div class="card-title"><span class="icon"></span>数据复现与重新采集</div></div>
    <div style="padding:24px;background:linear-gradient(135deg,#eff6ff,#dbeafe);border-radius:8px;text-align:center;margin-bottom:16px">
      <div style="font-size:18px;font-weight:700;color:#1e40af;margin-bottom:12px">数据可追溯、可复现、可验证</div>
      <div style="font-size:13px;color:#3b82f6;max-width:600px;margin:0 auto;line-height:1.8">
        所有采集参数、源代码、时间戳均已版本化管理（GitHub）。任何人都可以基于相同配置复现整个数据采集过程，确保研究的科学严谨性。
      </div>
      <div style="margin-top:20px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
        <a href="/collector" style="display:inline-flex;background:#2563eb;color:#fff;padding:10px 24px;border-radius:8px;text-decoration:none;font-weight:600">启动全量采集</a>
        <a href="/logs" style="display:inline-flex;background:#fff;color:#2563eb;border:1px solid #2563eb;padding:10px 24px;border-radius:8px;text-decoration:none;font-weight:600">查看采集日志</a>
      </div>
    </div>
    <div style="margin-top:16px">
      <div style="font-weight:700;margin-bottom:12px">最近采集日志（最近5条）</div>
      <div style="overflow-x:auto">
        <table class="data-table">
          <tr><th>级别</th><th>消息</th><th>时间</th></tr>
          {log_html}
        </table>
      </div>
    </div>
  </div>
</div>

{{% endblock %}}
'''

with open('templates/v3_collection.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("v3_collection.html v2 生成完成")
