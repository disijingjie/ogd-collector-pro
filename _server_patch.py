import sys

with open('/opt/ogd-collector-pro/templates/v3_dashboard.html','r',encoding='utf-8') as f:
    c = f.read()

# 重写数据规模总览模块
old = '''<div id="overview" class="scroll-section">
  <div class="card-header"><div class="card-title"><span class="icon"></span>数据规模总览</div></div>
  <div class="stats-grid">
    <a href="/v3/collection#provenance" class="stat-card"><div class="stat-value">88</div><div class="stat-label">政府数据开放平台</div><div style="font-size:12px;color:#16a34a;margin-top:4px">覆盖31个省级行政区 →</div></a>
    <a href="/v3/collection#strategy" class="stat-card"><div class="stat-value">23/23</div><div class="stat-label">省级数据采集覆盖</div><div style="font-size:12px;color:#16a34a;margin-top:4px">23省+8种采集策略 →</div></a>
    <a href="/v3/thesis" class="stat-card"><div class="stat-value">36</div><div class="stat-label">论文图表</div><div style="font-size:12px;color:#16a34a;margin-top:4px">24张表+12张图 →</div></a>
    <a href="/v3/analysis" class="stat-card"><div class="stat-value">5</div><div class="stat-label">分析方法</div><div style="font-size:12px;color:#16a34a;margin-top:4px">TOPSIS→DEA→DEMATEL→fsQCA→DID →</div></a>
  </div>
</div>'''

new = '''<div id="overview" class="scroll-section" data-v="2">
  <div class="card-header"><div class="card-title"><span class="icon"></span>数据规模总览</div></div>
  <div class="stats-grid">
    <a href="/v3/collection#provenance" class="stat-card"><div class="stat-value">88</div><div class="stat-label">政府数据开放平台</div><div class="stat-note">覆盖31个省级行政区 →</div></a>
    <a href="/v3/collection#strategy" class="stat-card"><div class="stat-value">23/23</div><div class="stat-label">省级数据采集覆盖</div><div class="stat-note">23省+8种采集策略 →</div></a>
    <a href="/v3/thesis" class="stat-card"><div class="stat-value">36</div><div class="stat-label">论文图表</div><div class="stat-note">24张表+12张图 →</div></a>
    <a href="/v3/analysis" class="stat-card"><div class="stat-value">5</div><div class="stat-label">分析方法</div><div class="stat-note">TOPSIS→DEA→DEMATEL→fsQCA→DID →</div></a>
  </div>
</div>'''

if old in c:
    c = c.replace(old, new)
    with open('/opt/ogd-collector-pro/templates/v3_dashboard.html','w',encoding='utf-8') as f:
        f.write(c)
    print('OK')
else:
    print('NOT_FOUND')
    sys.exit(1)
