import sqlite3, json, html

conn = sqlite3.connect('data/ogd_database.db')
c = conn.cursor()

# ============================================================
# 1. 采集中心页面 - 新增内容
# ============================================================

# 1.1 获取采集任务记录
c.execute("""
    SELECT id, task_name, task_type, status, total_count, completed_count, success_count, fail_count, started_at, completed_at
    FROM collection_tasks ORDER BY id DESC LIMIT 10
""")
tasks = c.fetchall()

# 1.2 获取采集日志
c.execute("""
    SELECT id, task_id, platform_code, log_level, message, created_at
    FROM collection_logs ORDER BY id DESC LIMIT 20
""")
logs = c.fetchall()

# 1.3 获取数据来源记录
c.execute("""
    SELECT id, source_name, source_type, access_method, data_start_date, data_end_date, data_format, record_count, cited_in_chapter, created_at
    FROM data_provenance WHERE is_active=1 ORDER BY id
""")
provenance = c.fetchall()

# 1.4 获取采集记录（带平台名和方法）
c.execute("""
    SELECT platform_name, tier, region, status, dataset_count, format_types, has_api, has_bulk_download, response_time, score_c1, score_c2, score_c3, score_c4, overall_score, collected_at
    FROM collection_records ORDER BY collected_at DESC LIMIT 15
""")
records = c.fetchall()

conn.close()

# ---- 构建采集日志HTML ----
log_rows = ""
for log in logs:
    lid, tid, pcode, level, msg, created = log
    level_class = "badge-prov" if level == "INFO" else ("badge-city" if level == "WARN" else "badge-api")
    safe_msg = html.escape(str(msg)[:80]) if msg else ""
    safe_time = str(created)[:19] if created else ""
    log_rows += f'<tr><td>{lid}</td><td><span class="badge {level_class}">{level}</span></td><td>{pcode or "-"}</td><td style="font-size:12px">{safe_msg}</td><td style="font-size:12px;color:#64748b">{safe_time}</td></tr>'

# ---- 构建数据来源记录HTML ----
prov_rows = ""
for p in provenance:
    pid, name, stype, method, start, end, fmt, count, chapter, created = p
    safe_name = html.escape(str(name)) if name else ""
    safe_method = html.escape(str(method)) if method else ""
    safe_chapter = html.escape(str(chapter)) if chapter else "未引用"
    count_str = f"{count}条" if count else "-"
    date_range = f"{start}~{end}" if start and end else (start or end or "-")
    prov_rows += f'<tr><td>{safe_name}</td><td>{stype or "-"}</td><td>{safe_method}</td><td>{date_range}</td><td>{fmt or "-"}</td><td>{count_str}</td><td><span class="badge" style="background:#dbeafe;color:#1d4ed8">{safe_chapter}</span></td></tr>'

# ---- 构建采集记录HTML ----
rec_rows = ""
for r in records:
    name, tier, region, status, ds_count, fmt, has_api, has_bulk, resp, s1, s2, s3, s4, overall, collected = r
    safe_name = html.escape(str(name)) if name else ""
    status_badge = '<span class="badge badge-prov">成功</span>' if status == 'success' else '<span class="badge badge-api">失败</span>'
    ds_str = f"{int(ds_count)}" if ds_count else "-"
    score_str = f"{overall:.3f}" if overall else "-"
    time_str = str(collected)[:19] if collected else "-"
    rec_rows += f'<tr><td>{safe_name}</td><td>{tier or "-"}</td><td>{region or "-"}</td><td>{status_badge}</td><td>{ds_str}</td><td>{fmt or "-"}</td><td>{score_str}</td><td style="font-size:12px;color:#64748b">{time_str}</td></tr>'

# ---- 采集任务记录HTML ----
task_rows = ""
for t in tasks:
    tid, name, ttype, status, total, comp, success, fail, started, ended = t
    ttype_label = "全量" if ttype == "full" else "增量"
    status_badge = '<span class="badge badge-prov">完成</span>' if status == 'completed' else ('<span class="badge badge-city">进行中</span>' if status == 'running' else '<span class="badge badge-api">失败</span>')
    rate = f"{success}/{total}" if total else "-"
    time_str = f"{str(started)[:16]}" if started else "-"
    task_rows += f'<tr><td>{tid}</td><td>{name}</td><td><span class="badge" style="background:#e0e7ff;color:#4338ca">{ttype_label}</span></td><td>{status_badge}</td><td>{rate}</td><td>{time_str}</td></tr>'

new_collection_sections = f'''
<div id="logs" class="scroll-section">
  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>采集日志（真实记录）</div></div>
    <div style="overflow-x:auto"><table class="data-table"><tr><th>ID</th><th>级别</th><th>平台</th><th>消息</th><th>时间</th></tr>{log_rows}</table></div>
  </div>
</div>

<div id="tasks" class="scroll-section">
  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>采集任务历史</div></div>
    <div style="overflow-x:auto"><table class="data-table"><tr><th>任务ID</th><th>任务名称</th><th>类型</th><th>状态</th><th>成功/总数</th><th>启动时间</th></tr>{task_rows}</table></div>
  </div>
</div>

<div id="provenance" class="scroll-section">
  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>博士论文数据来源完整记录</div><div style="font-size:12px;color:#64748b">展示本研究使用的所有数据来源、采集方法与引用章节</div></div>
    <div style="overflow-x:auto"><table class="data-table"><tr><th>来源名称</th><th>来源类型</th><th>采集方法</th><th>数据时间范围</th><th>数据格式</th><th>记录数</th><th>引用章节</th></tr>{prov_rows}</table></div>
    <div style="margin-top:20px;padding:16px;background:#f8fafc;border-radius:8px">
      <div style="font-weight:700;margin-bottom:12px;color:#1e293b">数据采集时间线</div>
      <div class="timeline">
        <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2023年3月 - 项目启动与框架设计</div><div class="timeline-desc">确定研究问题，构建4E理论框架，设计五方法递进分析链。确定采集目标：全国31个省级政府数据开放平台。</div></div>
        <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2023年6月 - 首轮省级平台采集</div><div class="timeline-desc">使用Requests+BeautifulSoup对31个省级平台进行静态页面采集。山东、浙江、广东等采用直接HTML解析；北京、上海等采用Selenium动态渲染。</div></div>
        <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2023年9月 - 市级平台拓展采集</div><div class="timeline-desc">补充57个副省级/地级市平台。深圳、杭州等采用API接口直接调用；部分中西部市级平台因技术架构差异采用混合策略。</div></div>
        <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2023年12月 - 数据清洗与标准化（第一阶段）</div><div class="timeline-desc">去重：基于URL哈希去重，消除跨平台重复数据集。格式统一：将CSV/XLS/JSON/XML等格式映射为标准枚举值。日期标准化：统一为ISO 8601格式。</div></div>
        <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2024年3月 - 数据清洗与标准化（第二阶段）</div><div class="timeline-desc">部门名称标准化：参照GB/T 2260行政区划代码和国务院机构简称规范。缺失值处理：对缺失率>50%的字段标记，<50%采用众数填补。异常值检测：箱线图法识别离群值。</div></div>
        <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2024年6月 - 统一指标体系构建</div><div class="timeline-desc">将原始元数据（数据集数量、格式类型、更新频率、下载量等）映射为4E框架的二级指标，形成标准化评估矩阵。</div></div>
        <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2024年9月-2025年4月 - 多方法分析与验证</div><div class="timeline-desc">依次完成TOPSIS排名、DEA效率、DEMATEL因果、fsQCA路径、DID政策效应五方法分析。每种方法的结果均经过交叉验证。</div></div>
        <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-title">2025年5月-2026年4月 - 系统开发与论文写作</div><div class="timeline-desc">开发OGD-Collector Pro可视化平台，将采集、分析、展示全流程系统化。完成博士论文v25版本撰写。</div></div>
      </div>
    </div>
  </div>
</div>

<div id="cleaning" class="scroll-section">
  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>数据归纳、分类与清洗流程</div></div>
    <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:16px">
      <p>原始采集数据来自88个政府数据开放平台，各平台的元数据字段命名、格式、分类体系存在显著差异。本研究通过<strong>四步清洗流程</strong>将其转化为统一的标准化数据集。</p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-bottom:16px">
      <div style="padding:16px;background:#f8fafc;border-radius:8px;border-left:4px solid #2563eb">
        <div style="font-weight:700;margin-bottom:8px">Step 1: 字段映射</div>
        <div style="font-size:12px;color:#64748b;line-height:1.8">
          将各平台不同的字段名映射到统一标准。例如：<br>
          • "数据集名称" / "资源标题" / "name" → <strong>dataset_title</strong><br>
          • "更新日期" / "发布时间" / "update_time" → <strong>update_date</strong><br>
          • "提供部门" / "责任部门" / "dept" → <strong>department</strong>
        </div>
      </div>
      <div style="padding:16px;background:#f8fafc;border-radius:8px;border-left:4px solid #059669">
        <div style="font-weight:700;margin-bottom:8px">Step 2: 分类体系统一</div>
        <div style="font-size:12px;color:#64748b;line-height:1.8">
          各平台数据集分类标签不一致（如"交通"vs"交通运输"），采用<strong>关键词匹配+人工校验</strong>统一为12个一级主题：交通、环境、教育、医疗、经济、社会、文化、科技、农业、公共安全、城市规划、其他。
        </div>
      </div>
      <div style="padding:16px;background:#f8fafc;border-radius:8px;border-left:4px solid #d97706">
        <div style="font-weight:700;margin-bottom:8px">Step 3: 格式标准化</div>
        <div style="font-size:12px;color:#64748b;line-height:1.8">
          数据格式字段统一映射：<br>
          • CSV/Excel/XLS/XLSX → <strong>表格</strong><br>
          • JSON/XML/API → <strong>接口</strong><br>
          • PDF/DOC → <strong>文档</strong><br>
          • SHP/GeoJSON → <strong>地理</strong>
        </div>
      </div>
      <div style="padding:16px;background:#f8fafc;border-radius:8px;border-left:4px solid #db2777">
        <div style="font-weight:700;margin-bottom:8px">Step 4: 质量校验</div>
        <div style="font-size:12px;color:#64748b;line-height:1.8">
          完整性：必填字段缺失率<20%<br>
          一致性：省份-平台关联正确性100%<br>
          时效性：数据集更新时间在近2年内<br>
          可用性：下载链接可访问性检验
        </div>
      </div>
    </div>
    <div class="chart-container" style="margin:0">
      <div class="chart-title">图：数据清洗全流程示意图</div>
      <div style="overflow-x:auto"><svg viewBox="0 0 900 160" style="width:100%;min-width:700px">
        <rect x="0" y="0" width="900" height="160" fill="#f8fafc" rx="8"/>
        <rect x="20" y="30" width="140" height="80" fill="#fee2e2" stroke="#dc2626" stroke-width="2" rx="8"/><text x="90" y="60" text-anchor="middle" font-size="12" font-weight="700" fill="#991b1b">原始数据</text><text x="90" y="78" text-anchor="middle" font-size="9" fill="#64748b">88平台元数据</text><text x="90" y="92" text-anchor="middle" font-size="9" fill="#64748b">字段各异、格式混乱</text>
        <rect x="190" y="30" width="140" height="80" fill="#fef3c7" stroke="#d97706" stroke-width="2" rx="8"/><text x="260" y="60" text-anchor="middle" font-size="12" font-weight="700" fill="#92400e">字段映射</text><text x="260" y="78" text-anchor="middle" font-size="9" fill="#64748b">统一字段命名</text><text x="260" y="92" text-anchor="middle" font-size="9" fill="#64748b">建立对照表</text>
        <rect x="360" y="30" width="140" height="80" fill="#dbeafe" stroke="#2563eb" stroke-width="2" rx="8"/><text x="430" y="60" text-anchor="middle" font-size="12" font-weight="700" fill="#1e40af">分类统一</text><text x="430" y="78" text-anchor="middle" font-size="9" fill="#64748b">12个一级主题</text><text x="430" y="92" text-anchor="middle" font-size="9" fill="#64748b">关键词匹配+人工</text>
        <rect x="530" y="30" width="140" height="80" fill="#d1fae5" stroke="#059669" stroke-width="2" rx="8"/><text x="600" y="60" text-anchor="middle" font-size="12" font-weight="700" fill="#065f46">格式标准化</text><text x="600" y="78" text-anchor="middle" font-size="9" fill="#64748b">4类标准格式</text><text x="600" y="92" text-anchor="middle" font-size="9" fill="#64748b">枚举值映射</text>
        <rect x="700" y="30" width="170" height="80" fill="#ecfdf5" stroke="#10b981" stroke-width="2" rx="8"/><text x="785" y="60" text-anchor="middle" font-size="12" font-weight="700" fill="#065f46">标准化数据集</text><text x="785" y="78" text-anchor="middle" font-size="9" fill="#64748b">字段统一、分类一致</text><text x="785" y="92" text-anchor="middle" font-size="9" fill="#64748b">可直接用于分析</text>
        <defs><marker id="cl" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#94a3b8"/></marker></defs>
        <line x1="160" y1="70" x2="190" y2="70" stroke="#94a3b8" stroke-width="2" marker-end="url(#cl)"/>
        <line x1="330" y1="70" x2="360" y2="70" stroke="#94a3b8" stroke-width="2" marker-end="url(#cl)"/>
        <line x1="500" y1="70" x2="530" y2="70" stroke="#94a3b8" stroke-width="2" marker-end="url(#cl)"/>
        <line x1="670" y1="70" x2="700" y2="70" stroke="#94a3b8" stroke-width="2" marker-end="url(#cl)"/>
      </svg></div>
    </div>
  </div>
</div>

<div id="unified" class="scroll-section">
  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>统一指标体系构建过程</div></div>
    <div style="font-size:13px;color:#64748b;line-height:1.8;margin-bottom:16px">
      <p>清洗后的标准化元数据需要进一步转化为可量化评估的指标。本研究基于<strong>4E理论框架</strong>，将原始字段映射为16个二级指标，再聚合为4个一级维度。</p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px">
      <div class="chart-container" style="margin:0"><div class="chart-title">经济性(Economy)指标构建</div>
        <div style="padding:12px;font-size:12px;color:#64748b;line-height:2">
          <strong>原始数据字段：</strong>平台维护状态、域名注册年限、服务器响应时间<br>
          <strong>→ 映射指标：</strong><br>
          • C1-投入强度 = 数据集总量 / 平台运营年限<br>
          • C2-成本控制 = 开放格式占比（CSV/JSON/API视为低成本）<br>
          <strong>→ 数据来源：</strong>collection_records.dataset_count, format_types
        </div>
      </div>
      <div class="chart-container" style="margin:0"><div class="chart-title">效率性(Efficiency)指标构建</div>
        <div style="padding:12px;font-size:12px;color:#64748b;line-height:2">
          <strong>原始数据字段：</strong>数据集更新频率、下载量、API调用次数<br>
          <strong>→ 映射指标：</strong><br>
          • C3-更新效率 = 近一年更新数据集占比<br>
          • C4-访问效率 = 平均响应时间倒数（标准化）<br>
          <strong>→ 数据来源：</strong>collection_records.response_time, 数据集update_date
        </div>
      </div>
      <div class="chart-container" style="margin:0"><div class="chart-title">有效性(Effectiveness)指标构建</div>
        <div style="padding:12px;font-size:12px;color:#64748b;line-height:2">
          <strong>原始数据字段：</strong>功能完整性（API/下载/搜索/可视化/反馈）<br>
          <strong>→ 映射指标：</strong><br>
          • C5-功能完整度 = has_api + has_download + has_search + has_visualization + has_feedback（5项求和标准化）<br>
          • C6-数据覆盖度 = 主题分类覆盖数 / 12<br>
          <strong>→ 数据来源：</strong>collection_records各功能布尔字段
        </div>
      </div>
      <div class="chart-container" style="margin:0"><div class="chart-title">公平性(Equity)指标构建</div>
        <div style="padding:12px;font-size:12px;color:#64748b;line-height:2">
          <strong>原始数据字段：</strong>地区经济发展水平、平台层级、数据集可获取性<br>
          <strong>→ 映射指标：</strong><br>
          • C7-区域均衡 = 该平台绩效与全国均值的偏差（越小越公平）<br>
          • C8-层级覆盖 = 省/市两级平台覆盖率<br>
          <strong>→ 数据来源：</strong>platforms.tier, collection_records.overall_score
        </div>
      </div>
    </div>
    <div style="margin-top:20px;padding:16px;background:#f0f9ff;border-radius:8px">
      <div style="font-weight:700;margin-bottom:8px;color:#0369a1">指标计算示例：功能完整度(C5)</div>
      <div style="font-size:12px;color:#64748b;line-height:1.8">
        以山东省数据开放平台为例：<br>
        has_api=1, has_download=1, has_search=1, has_visualization=1, has_feedback=0<br>
        C5 = (1+1+1+1+0) / 5 = 0.80<br>
        经过Min-Max标准化后：C5_std = (0.80 - 0.20) / (1.00 - 0.20) = 0.75<br>
        该指标最终进入TOPSIS和DEA的输入/输出矩阵。
      </div>
    </div>
    <div style="margin-top:16px">
      <div style="font-weight:700;margin-bottom:12px">最新采集记录（真实数据）</div>
      <div style="overflow-x:auto"><table class="data-table"><tr><th>平台名称</th><th>层级</th><th>地区</th><th>状态</th><th>数据集数</th><th>格式</th><th>综合得分</th><th>采集时间</th></tr>{rec_rows}</table></div>
    </div>
  </div>
</div>
'''

# 读取现有 collection 页面
with open('templates/v3_collection.html', 'r', encoding='utf-8') as f:
    collection_content = f.read()

# 修改锚点导航
old_anchor = '<a href="#recollect" class="">重新采集</a>'
new_anchor = '<a href="#recollect" class="">重新采集</a><a href="#logs" class="">采集日志</a><a href="#tasks" class="">任务记录</a><a href="#provenance" class="">数据来源</a><a href="#cleaning" class="">数据清洗</a><a href="#unified" class="">统一指标</a>'
collection_content = collection_content.replace(old_anchor, new_anchor)

# 在 {% endblock %} 前插入新内容
collection_content = collection_content.replace('{% endblock %}', new_collection_sections + '\n{% endblock %}')

with open('templates/v3_collection.html', 'w', encoding='utf-8') as f:
    f.write(collection_content)

print("v3_collection.html 更新完成")

# ============================================================
# 2. 系统概览页面 - 技术路线图升级
# ============================================================

with open('templates/v3_dashboard.html', 'r', encoding='utf-8') as f:
    dash_content = f.read()

# 替换技术路线图部分
old_roadmap = '''<div id="roadmap" class="scroll-section">
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
</div>'''

new_roadmap = '''<div id="roadmap" class="scroll-section">
  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>博士论文研究技术路线图（全文）</div></div>
    <div style="overflow-x:auto">
      <svg viewBox="0 0 1100 500" style="width:100%;min-width:1000px">
        <rect x="0" y="0" width="1100" height="500" fill="#f8fafc" rx="12"/>
        <!-- 第一层：研究问题 -->
        <rect x="350" y="15" width="400" height="45" fill="#1e293b" stroke="#334155" stroke-width="2" rx="8"/><text x="550" y="43" text-anchor="middle" font-size="14" font-weight="700" fill="#ffffff">中国政府数据开放平台绩效评估研究</text>

        <!-- 第二层：理论框架 -->
        <rect x="50" y="80" width="200" height="55" fill="#dbeafe" stroke="#2563eb" stroke-width="2" rx="8"/><text x="150" y="102" text-anchor="middle" font-size="12" font-weight="700" fill="#1e40af">4E理论框架</text><text x="150" y="118" text-anchor="middle" font-size="9" fill="#3b82f6">经济性/效率性/有效性/公平性</text>
        <rect x="280" y="80" width="200" height="55" fill="#d1fae5" stroke="#059669" stroke-width="2" rx="8"/><text x="380" y="102" text-anchor="middle" font-size="12" font-weight="700" fill="#065f46">制度同形理论</text><text x="380" y="118" text-anchor="middle" font-size="9" fill="#10b981">强制性/模仿性/规范性同形</text>
        <rect x="510" y="80" width="200" height="55" fill="#fef3c7" stroke="#d97706" stroke-width="2" rx="8"/><text x="610" y="102" text-anchor="middle" font-size="12" font-weight="700" fill="#92400e">NPG新公共治理</text><text x="610" y="118" text-anchor="middle" font-size="9" fill="#f59e0b">多元主体协同治理</text>
        <rect x="740" y="80" width="200" height="55" fill="#fce7f3" stroke="#db2777" stroke-width="2" rx="8"/><text x="840" y="102" text-anchor="middle" font-size="12" font-weight="700" fill="#9d174d">数据要素理论</text><text x="840" y="118" text-anchor="middle" font-size="9" fill="#ec4899">数据作为第五大生产要素</text>

        <!-- 第三层：数据采集 -->
        <rect x="50" y="160" width="160" height="55" fill="#eff6ff" stroke="#93c5fd" stroke-width="2" rx="8"/><text x="130" y="182" text-anchor="middle" font-size="11" font-weight="700" fill="#1d4ed8">种子URL发现</text><text x="130" y="198" text-anchor="middle" font-size="9" fill="#64748b">88个平台入口</text>
        <rect x="230" y="160" width="160" height="55" fill="#eff6ff" stroke="#93c5fd" stroke-width="2" rx="8"/><text x="310" y="182" text-anchor="middle" font-size="11" font-weight="700" fill="#1d4ed8">页面类型识别</text><text x="310" y="198" text-anchor="middle" font-size="9" fill="#64748b">静态/动态/API</text>
        <rect x="410" y="160" width="160" height="55" fill="#eff6ff" stroke="#93c5fd" stroke-width="2" rx="8"/><text x="490" y="182" text-anchor="middle" font-size="11" font-weight="700" fill="#1d4ed8">元数据提取</text><text x="490" y="198" text-anchor="middle" font-size="9" fill="#64748b">8个核心字段</text>
        <rect x="590" y="160" width="160" height="55" fill="#eff6ff" stroke="#93c5fd" stroke-width="2" rx="8"/><text x="670" y="182" text-anchor="middle" font-size="11" font-weight="700" fill="#1d4ed8">数据清洗</text><text x="670" y="198" text-anchor="middle" font-size="9" fill="#64748b">去重/标准化/校验</text>
        <rect x="770" y="160" width="160" height="55" fill="#eff6ff" stroke="#93c5fd" stroke-width="2" rx="8"/><text x="850" y="182" text-anchor="middle" font-size="11" font-weight="700" fill="#1d4ed8">统一指标构建</text><text x="850" y="198" text-anchor="middle" font-size="9" fill="#64748b">4E→16个二级指标</text>

        <!-- 第四层：五方法分析链 -->
        <rect x="30" y="250" width="180" height="65" fill="#fef3c7" stroke="#d97706" stroke-width="2" rx="8"/><text x="120" y="275" text-anchor="middle" font-size="12" font-weight="700" fill="#92400e">TOPSIS</text><text x="120" y="292" text-anchor="middle" font-size="9" fill="#f59e0b">综合评价排名</text><text x="120" y="306" text-anchor="middle" font-size="8" fill="#64748b">第5章 | "是什么"</text>
        <rect x="230" y="250" width="180" height="65" fill="#d1fae5" stroke="#059669" stroke-width="2" rx="8"/><text x="320" y="275" text-anchor="middle" font-size="12" font-weight="700" fill="#065f46">DEA</text><text x="320" y="292" text-anchor="middle" font-size="9" fill="#10b981">效率评估分析</text><text x="320" y="306" text-anchor="middle" font-size="8" fill="#64748b">第5章 | "效率如何"</text>
        <rect x="430" y="250" width="180" height="65" fill="#dbeafe" stroke="#2563eb" stroke-width="2" rx="8"/><text x="520" y="275" text-anchor="middle" font-size="12" font-weight="700" fill="#1e40af">DEMATEL</text><text x="520" y="292" text-anchor="middle" font-size="9" fill="#3b82f6">因果关系挖掘</text><text x="520" y="306" text-anchor="middle" font-size="8" fill="#64748b">第6章 | "为什么"</text>
        <rect x="630" y="250" width="180" height="65" fill="#fce7f3" stroke="#db2777" stroke-width="2" rx="8"/><text x="720" y="275" text-anchor="middle" font-size="12" font-weight="700" fill="#9d174d">fsQCA</text><text x="720" y="292" text-anchor="middle" font-size="9" fill="#ec4899">高绩效路径分析</text><text x="720" y="306" text-anchor="middle" font-size="8" fill="#64748b">第6章 | "哪条路径"</text>
        <rect x="830" y="250" width="180" height="65" fill="#f3e8ff" stroke="#9333ea" stroke-width="2" rx="8"/><text x="920" y="275" text-anchor="middle" font-size="12" font-weight="700" fill="#7e22ce">DID</text><text x="920" y="292" text-anchor="middle" font-size="9" fill="#a855f7">政策效应评估</text><text x="920" y="306" text-anchor="middle" font-size="8" fill="#64748b">第7章 | "政策有效吗"</text>

        <!-- 第五层：结论与应用 -->
        <rect x="200" y="350" width="240" height="55" fill="#ecfdf5" stroke="#10b981" stroke-width="2" rx="8"/><text x="320" y="372" text-anchor="middle" font-size="12" font-weight="700" fill="#065f46">理论贡献</text><text x="320" y="388" text-anchor="middle" font-size="9" fill="#64748b">4E框架+制度同形+两条高绩效路径</text>
        <rect x="470" y="350" width="240" height="55" fill="#ecfdf5" stroke="#10b981" stroke-width="2" rx="8"/><text x="590" y="372" text-anchor="middle" font-size="12" font-weight="700" fill="#065f46">实践启示</text><text x="590" y="388" text-anchor="middle" font-size="9" fill="#64748b">差异化施策+数据质量提升+制度建设</text>
        <rect x="740" y="350" width="240" height="55" fill="#ecfdf5" stroke="#10b981" stroke-width="2" rx="8"/><text x="860" y="372" text-anchor="middle" font-size="12" font-weight="700" fill="#065f46">政策建议</text><text x="860" y="388" text-anchor="middle" font-size="9" fill="#64748b">面向国家数据局的三条行动建议</text>

        <!-- 底部支撑 -->
        <rect x="30" y="430" width="1040" height="55" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1" rx="8"/>
        <text x="150" y="455" text-anchor="middle" font-size="11" font-weight="700" fill="#334155">技术支撑</text>
        <text x="150" y="472" text-anchor="middle" font-size="10" fill="#64748b">Python 3.11 + Flask</text>
        <text x="380" y="455" text-anchor="middle" font-size="11" font-weight="700" fill="#334155">数据存储</text>
        <text x="380" y="472" text-anchor="middle" font-size="10" fill="#64748b">SQLite + JSON + CSV</text>
        <text x="610" y="455" text-anchor="middle" font-size="11" font-weight="700" fill="#334155">分析工具</text>
        <text x="610" y="472" text-anchor="middle" font-size="10" fill="#64748b">R + Python + fsQCA + Stata</text>
        <text x="840" y="455" text-anchor="middle" font-size="11" font-weight="700" fill="#334155">部署环境</text>
        <text x="840" y="472" text-anchor="middle" font-size="10" fill="#64748b">腾讯云 + Nginx + Gunicorn</text>

        <!-- 箭头连接 -->
        <defs><marker id="ar" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#94a3b8"/></marker></defs>
        <!-- 问题→理论 -->
        <line x1="450" y1="60" x2="150" y2="80" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#ar)"/>
        <line x1="500" y1="60" x2="380" y2="80" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#ar)"/>
        <line x1="550" y1="60" x2="610" y2="80" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#ar)"/>
        <line x1="600" y1="60" x2="840" y2="80" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#ar)"/>
        <!-- 理论→采集 -->
        <line x1="150" y1="135" x2="130" y2="160" stroke="#94a3b8" stroke-width="1" stroke-dasharray="3"/>
        <line x1="380" y1="135" x2="310" y2="160" stroke="#94a3b8" stroke-width="1" stroke-dasharray="3"/>
        <line x1="610" y1="135" x2="490" y2="160" stroke="#94a3b8" stroke-width="1" stroke-dasharray="3"/>
        <line x1="840" y1="135" x2="850" y2="160" stroke="#94a3b8" stroke-width="1" stroke-dasharray="3"/>
        <!-- 采集横向 -->
        <line x1="210" y1="187" x2="230" y2="187" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#ar)"/>
        <line x1="390" y1="187" x2="410" y2="187" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#ar)"/>
        <line x1="570" y1="187" x2="590" y2="187" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#ar)"/>
        <line x1="750" y1="187" x2="770" y2="187" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#ar)"/>
        <!-- 采集→分析 -->
        <line x1="500" y1="215" x2="500" y2="250" stroke="#94a3b8" stroke-width="2" marker-end="url(#ar)"/>
        <!-- 分析横向 -->
        <line x1="210" y1="282" x2="230" y2="282" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#ar)"/>
        <line x1="410" y1="282" x2="430" y2="282" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#ar)"/>
        <line x1="610" y1="282" x2="630" y2="282" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#ar)"/>
        <line x1="810" y1="282" x2="830" y2="282" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#ar)"/>
        <!-- 分析→结论 -->
        <line x1="320" y1="315" x2="320" y2="350" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#ar)"/>
        <line x1="520" y1="315" x2="520" y2="350" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#ar)"/>
        <line x1="720" y1="315" x2="720" y2="350" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#ar)"/>
        <!-- 结论横向 -->
        <line x1="440" y1="377" x2="470" y2="377" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#ar)"/>
        <line x1="710" y1="377" x2="740" y2="377" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#ar)"/>

        <!-- 核心标签 -->
        <text x="550" y="240" text-anchor="middle" font-size="11" fill="#64748b" font-weight="700">递进逻辑：描述 → 诊断 → 归因 → 处方 → 验证</text>
      </svg>
    </div>
    <div style="margin-top:16px;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px">
      <div style="padding:12px;background:#f8fafc;border-radius:8px;text-align:center"><div style="font-size:20px;font-weight:800;color:#2563eb">8</div><div style="font-size:12px;color:#64748b">论文章节</div></div>
      <div style="padding:12px;background:#f8fafc;border-radius:8px;text-align:center"><div style="font-size:20px;font-weight:800;color:#059669">5</div><div style="font-size:12px;color:#64748b">分析方法</div></div>
      <div style="padding:12px;background:#f8fafc;border-radius:8px;text-align:center"><div style="font-size:20px;font-weight:800;color:#d97706">88</div><div style="font-size:12px;color:#64748b">采集平台</div></div>
      <div style="padding:12px;background:#f8fafc;border-radius:8px;text-align:center"><div style="font-size:20px;font-weight:800;color:#db2777">4</div><div style="font-size:12px;color:#64748b">理论维度</div></div>
    </div>
  </div>
</div>'''

dash_content = dash_content.replace(old_roadmap, new_roadmap)

with open('templates/v3_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dash_content)

print("v3_dashboard.html 更新完成")

# ============================================================
# 3. 论文成果页面 - 每章详细图表+可展开内容
# ============================================================

with open('templates/v3_thesis.html', 'r', encoding='utf-8') as f:
    thesis_content = f.read()

# 在每章内容后面添加"查看全部图表"按钮和隐藏的详细内容区域
# 以及修改图表总览部分

# 找到图表总览部分并替换为更详细的版本
old_figures = '''<div id="figures" class="scroll-section">
  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>图表总览</div></div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px">
      <div style="padding:12px;background:#f8fafc;border-radius:8px"><div style="font-weight:700;font-size:13px;color:#2563eb">图1-1</div><div style="font-size:12px;color:#64748b">研究技术路线图</div></div>
      <div style="padding:12px;background:#f8fafc;border-radius:8px"><div style="font-weight:700;font-size:13px;color:#2563eb">图2-1</div><div style="font-size:12px;color:#64748b">4E理论框架适配图</div></div>
      <div style="padding:12px;background:#f8fafc;border-radius:8px"><div style="font-weight:700;font-size:13px;color:#2563eb">图2-2</div><div style="font-size:12px;color:#64748b">制度同形三机制图</div></div>
      <div style="padding:12px;background:#f8fafc;border-radius:8px"><div style="font-weight:700;font-size:13px;color:#2563eb">图3-1</div><div style="font-size:12px;color:#64748b">五方法递进分析框架</div></div>
      <div style="padding:12px;background:#f8fafc;border-radius:8px"><div style="font-weight:700;font-size:13px;color:#2563eb">图4-1</div><div style="font-size:12px;color:#64748b">平台地域分布图</div></div>
      <div style="padding:12px;background:#f8fafc;border-radius:8px"><div style="font-weight:700;font-size:13px;color:#2563eb">图4-2</div><div style="font-size:12px;color:#64748b">功能特征分布图</div></div>
      <div style="padding:12px;background:#f8fafc;border-radius:8px"><div style="font-weight:700;font-size:13px;color:#2563eb">图5-1</div><div style="font-size:12px;color:#64748b">TOPSIS-DEA二维矩阵</div></div>
      <div style="padding:12px;background:#f8fafc;border-radius:8px"><div style="font-weight:700;font-size:13px;color:#2563eb">图6-1</div><div style="font-size:12px;color:#64748b">DEMATEL因果网络</div></div>
      <div style="padding:12px;background:#f8fafc;border-radius:8px"><div style="font-weight:700;font-size:13px;color:#2563eb">图7-1</div><div style="font-size:12px;color:#64748b">政策实施趋势对比</div></div>
    </div>
  </div>
</div>'''

new_figures = '''<div id="figures" class="scroll-section">
  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>论文图表完整索引（36张图 + 24张表）</div></div>
    <div style="margin-bottom:16px"><div style="font-weight:700;margin-bottom:8px;color:#2563eb">第1章 绪论（2张图）</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px">
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#2563eb">图1-1</div><div style="font-size:11px;color:#64748b">研究技术路线图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#2563eb">图1-2</div><div style="font-size:11px;color:#64748b">论文结构安排</div></div>
      </div>
    </div>
    <div style="margin-bottom:16px"><div style="font-weight:700;margin-bottom:8px;color:#059669">第2章 理论基础与文献综述（8张图 + 4张表）</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px">
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#059669">图2-1</div><div style="font-size:11px;color:#64748b">4E理论框架适配图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#059669">图2-2</div><div style="font-size:11px;color:#64748b">制度同形三机制图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#059669">图2-3</div><div style="font-size:11px;color:#64748b">关键词共现网络图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#059669">图2-4</div><div style="font-size:11px;color:#64748b">文献时间分布图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#059669">图2-5</div><div style="font-size:11px;color:#64748b">研究主题演化图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#059669">图2-6</div><div style="font-size:11px;color:#64748b">国际比较框架图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#059669">图2-7</div><div style="font-size:11px;color:#64748b">WOS文献计量图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#059669">图2-8</div><div style="font-size:11px;color:#64748b">CNKI文献计量图</div></div>
      </div>
      <div style="margin-top:8px;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px">
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表2-1</div><div style="font-size:11px;color:#64748b">4E理论核心维度</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表2-2</div><div style="font-size:11px;color:#64748b">制度同形三机制对比</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表2-3</div><div style="font-size:11px;color:#64748b">国内外评估框架比较</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表2-4</div><div style="font-size:11px;color:#64748b">国际案例汇总表</div></div>
      </div>
    </div>
    <div style="margin-bottom:16px"><div style="font-weight:700;margin-bottom:8px;color:#d97706">第3章 研究设计（3张图 + 3张表）</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px">
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#d97706">图3-1</div><div style="font-size:11px;color:#64748b">五方法递进分析框架</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#d97706">图3-2</div><div style="font-size:11px;color:#64748b">指标体系层次结构图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#d97706">图3-3</div><div style="font-size:11px;color:#64748b">数据采集流程图</div></div>
      </div>
      <div style="margin-top:8px;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px">
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表3-1</div><div style="font-size:11px;color:#64748b">4E指标体系总表</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表3-2</div><div style="font-size:11px;color:#64748b">五方法特征对比</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表3-3</div><div style="font-size:11px;color:#64748b">数据来源说明表</div></div>
      </div>
    </div>
    <div style="margin-bottom:16px"><div style="font-weight:700;margin-bottom:8px;color:#db2777">第4章 数据采集与平台画像（6张图 + 4张表）</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px">
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#db2777">图4-1</div><div style="font-size:11px;color:#64748b">平台地域分布图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#db2777">图4-2</div><div style="font-size:11px;color:#64748b">功能特征分布图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#db2777">图4-3</div><div style="font-size:11px;color:#64748b">数据集格式饼图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#db2777">图4-4</div><div style="font-size:11px;color:#64748b">平台层级柱状图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#db2777">图4-5</div><div style="font-size:11px;color:#64748b">DID设计示意图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#db2777">图4-6</div><div style="font-size:11px;color:#64748b">数据预处理流程图</div></div>
      </div>
      <div style="margin-top:8px;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px">
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表4-1</div><div style="font-size:11px;color:#64748b">88平台清单总表</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表4-2</div><div style="font-size:11px;color:#64748b">平台功能对比表</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表4-3</div><div style="font-size:11px;color:#64748b">数据集统计表</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表4-4</div><div style="font-size:11px;color:#64748b">描述性统计表</div></div>
      </div>
    </div>
    <div style="margin-bottom:16px"><div style="font-weight:700;margin-bottom:8px;color:#7c3aed">第5章 综合评价（6张图 + 4张表）</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px">
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#7c3aed">图5-1</div><div style="font-size:11px;color:#64748b">TOPSIS-DEA二维矩阵</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#7c3aed">图5-2</div><div style="font-size:11px;color:#64748b">TOPSIS排名条形图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#7c3aed">图5-3</div><div style="font-size:11px;color:#64748b">DEA效率散点图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#7c3aed">图5-4</div><div style="font-size:11px;color:#64748b">四维度雷达图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#7c3aed">图5-5</div><div style="font-size:11px;color:#64748b">区域对比热力图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#7c3aed">图5-6</div><div style="font-size:11px;color:#64748b">效率-排名象限图</div></div>
      </div>
      <div style="margin-top:8px;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px">
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表5-1</div><div style="font-size:11px;color:#64748b">TOPSIS排名结果表</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表5-2</div><div style="font-size:11px;color:#64748b">DEA效率结果表</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表5-3</div><div style="font-size:11px;color:#64748b">4E指标得分表</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表5-4</div><div style="font-size:11px;color:#64748b">效率-排名分类表</div></div>
      </div>
    </div>
    <div style="margin-bottom:16px"><div style="font-weight:700;margin-bottom:8px;color:#0ea5e9">第6章 因果挖掘（6张图 + 3张表）</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px">
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#0ea5e9">图6-1</div><div style="font-size:11px;color:#64748b">DEMATEL因果网络</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#0ea5e9">图6-2</div><div style="font-size:11px;color:#64748b">原因度-结果度散点图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#0ea5e9">图6-3</div><div style="font-size:11px;color:#64748b">中心度柱状图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#0ea5e9">图6-4</div><div style="font-size:11px;color:#64748b">fsQCA真值表</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#0ea5e9">图6-5</div><div style="font-size:11px;color:#64748b">高绩效路径图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#0ea5e9">图6-6</div><div style="font-size:11px;color:#64748b">组态覆盖度图</div></div>
      </div>
      <div style="margin-top:8px;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px">
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表6-1</div><div style="font-size:11px;color:#64748b">DEMATEL直接影响矩阵</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表6-2</div><div style="font-size:11px;color:#64748b">因果关系综合表</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表6-3</div><div style="font-size:11px;color:#64748b">fsQCA组态结果表</div></div>
      </div>
    </div>
    <div style="margin-bottom:16px"><div style="font-weight:700;margin-bottom:8px;color:#dc2626">第7章 政策效应（3张图 + 3张表）</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px">
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#dc2626">图7-1</div><div style="font-size:11px;color:#64748b">政策实施趋势对比</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#dc2626">图7-2</div><div style="font-size:11px;color:#64748b">平行趋势检验图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#dc2626">图7-3</div><div style="font-size:11px;color:#64748b">稳健性检验结果</div></div>
      </div>
      <div style="margin-top:8px;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px">
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表7-1</div><div style="font-size:11px;color:#64748b">DID基准回归结果</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表7-2</div><div style="font-size:11px;color:#64748b">平行趋势检验表</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表7-3</div><div style="font-size:11px;color:#64748b">稳健性检验汇总</div></div>
      </div>
    </div>
    <div style="margin-bottom:16px"><div style="font-weight:700;margin-bottom:8px;color:#16a34a">第8章 结论与展望（2张图 + 3张表）</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px">
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#16a34a">图8-1</div><div style="font-size:11px;color:#64748b">主要结论框架图</div></div>
        <div style="padding:10px;background:#f8fafc;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#16a34a">图8-2</div><div style="font-size:11px;color:#64748b">研究局限与未来方向</div></div>
      </div>
      <div style="margin-top:8px;display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px">
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表8-1</div><div style="font-size:11px;color:#64748b">理论贡献汇总表</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表8-2</div><div style="font-size:11px;color:#64748b">实践启示对照表</div></div>
        <div style="padding:10px;background:#fffbeb;border-radius:6px"><div style="font-weight:700;font-size:12px;color:#92400e">表8-3</div><div style="font-size:11px;color:#64748b">政策建议行动表</div></div>
      </div>
    </div>
  </div>
</div>'''

thesis_content = thesis_content.replace(old_figures, new_figures)

# 在每章添加"展开查看详细内容"的折叠区域
# 第1章
ch1_expand = '''</div>
</div>

<div id="ch1-detail" class="scroll-section" style="display:none">
  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>第1章 完整内容</div></div>
    <div style="font-size:13px;color:#64748b;line-height:1.8">
      <p style="margin-bottom:12px"><strong>1.1 研究背景</strong><br>数据作为新型生产要素，已成为推动经济社会数字化转型的核心驱动力。2022年12月，中共中央、国务院印发《关于构建数据基础制度更好发挥数据要素作用的意见》（"数据二十条"），标志着中国数据要素市场化配置改革进入新阶段。政府数据开放平台作为公共数据资源流通的核心枢纽，其建设质量直接影响数字政府治理效能和数据要素市场化配置效率。</p>
      <p style="margin-bottom:12px"><strong>1.2 问题提出</strong><br>（1）如何科学评估政府数据开放平台的综合绩效？（2）哪些因素驱动平台绩效差异？（3）数据开放政策是否产生了实质性效果？（4）高绩效平台的成功经验能否被复制推广？</p>
      <p style="margin-bottom:12px"><strong>1.3 研究意义</strong><br>理论意义：构建适用于中国情境的政府数据开放平台绩效评估框架，丰富信息资源管理学科的理论体系。实践意义：为政府数据开放平台建设提供科学的评估工具和优化路径。</p>
      <p style="margin-bottom:12px"><strong>1.4 研究内容与方法</strong><br>以全国31个省级政府数据开放平台为研究对象，采用"4E理论+五方法递进分析链"的研究设计，依次完成综合评价、因果挖掘和政策效应评估。</p>
      <p><strong>1.5 创新点</strong><br>① 构建"4E+五方法"融合评估框架；② 首次将fsQCA引入政府数据开放研究；③ 首次运用DID方法评估数据开放政策效应；④ 提出"制度驱动型"和"质量引领型"两条高绩效路径。</p>
    </div>
  </div>
</div>'''

# 使用更简单的方法：在第1章结束标记处添加展开按钮
thesis_content = thesis_content.replace(
    '<div id="ch1" class="scroll-section">\n  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>第1章 绪论</div></div>',
    '<div id="ch1" class="scroll-section">\n  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>第1章 绪论</div><button onclick="document.getElementById(\'ch1-detail\').style.display=\'block\';this.style.display=\'none\'" style="background:#2563eb;color:#fff;border:none;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:12px">展开完整内容</button></div>'
)

# 在ch1和ch2之间插入详细内容
insert_marker_ch1 = '</div>\n</div>\n\n<div id="ch2" class="scroll-section">'
thesis_content = thesis_content.replace(
    insert_marker_ch1,
    '''</div>
</div>

<div id="ch1-detail" class="scroll-section" style="display:none">
  <div class="card"><div class="card-header"><div class="card-title"><span class="icon"></span>第1章 完整内容</div></div>
    <div style="font-size:13px;color:#64748b;line-height:1.8">
      <p style="margin-bottom:12px"><strong>1.1 研究背景</strong><br>数据作为新型生产要素，已成为推动经济社会数字化转型的核心驱动力。2022年12月，中共中央、国务院印发《关于构建数据基础制度更好发挥数据要素作用的意见》（"数据二十条"），标志着中国数据要素市场化配置改革进入新阶段。</p>
      <p style="margin-bottom:12px"><strong>1.2 问题提出</strong><br>（1）如何科学评估政府数据开放平台的综合绩效？（2）哪些因素驱动平台绩效差异？（3）数据开放政策是否产生了实质性效果？</p>
      <p style="margin-bottom:12px"><strong>1.3 研究意义</strong><br>理论意义：构建适用于中国情境的政府数据开放平台绩效评估框架。实践意义：为平台建设提供科学的评估工具和优化路径。</p>
      <p style="margin-bottom:12px"><strong>1.4 创新点</strong><br>① 构建"4E+五方法"融合评估框架；② 首次将fsQCA引入政府数据开放研究；③ 首次运用DID方法评估数据开放政策效应。</p>
    </div>
  </div>
</div>

<div id="ch2" class="scroll-section">'''
)

with open('templates/v3_thesis.html', 'w', encoding='utf-8') as f:
    f.write(thesis_content)

print("v3_thesis.html 更新完成")
print("所有页面更新完成！")
