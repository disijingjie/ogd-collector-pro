import re

def extract_block(text, start_marker, end_marker):
    start = text.find(start_marker)
    if start == -1: return ''
    start += len(start_marker)
    end = text.find(end_marker, start)
    if end == -1: return text[start:]
    return text[start:end]

def extract_content(html):
    return extract_block(html, '{% block content %}', '{% endblock %}')

def extract_extra_js(html):
    return extract_block(html, '{% block extra_js %}', '{% endblock %}')

def extract_extra_css(html):
    return extract_block(html, '{% block extra_css %}', '{% endblock %}')

# 读取各文件
files = {
    'collector': open('collector.html', 'r', encoding='utf-8').read(),
    'monitoring': open('monitoring.html', 'r', encoding='utf-8').read(),
    'source_code': open('source_code.html', 'r', encoding='utf-8').read(),
    'provenance': open('provenance.html', 'r', encoding='utf-8').read(),
    'data_archive': open('data_archive.html', 'r', encoding='utf-8').read(),
}

# 提取各部分内容
parts = {}
for name, html in files.items():
    parts[name] = {
        'content': extract_content(html),
        'js': extract_extra_js(html),
        'css': extract_extra_css(html),
    }
    print(f'{name}: content={len(parts[name]["content"])} chars, js={len(parts[name]["js"])} chars, css={len(parts[name]["css"])} chars')

# 构建新的 dashboard.html
# 去掉每个子页面的 h2/h3 标题（因为用分割线代替）
def clean_title(content):
    # 去掉开头的 d-flex justify-content-between 标题行
    lines = content.split('\n')
    result = []
    skip = False
    for line in lines:
        if '<div class="d-flex justify-content-between align-items-center mb-4">' in line or \
           '<div class="d-flex justify-content-between align-items-center mb-3">' in line:
            skip = True
            continue
        if skip and '</div>' in line and line.strip() == '</div>':
            skip = False
            continue
        if skip:
            continue
        result.append(line)
    return '\n'.join(result)

# 收集所有 CSS
all_css = []
for name in ['monitoring', 'provenance', 'data_archive']:
    if parts[name]['css']:
        all_css.append(f'/* ===== {name} CSS ===== */')
        all_css.append(parts[name]['css'])

# 收集所有 content
sections = []

# 1. 采集管理
sections.append('<!-- ========== 一、采集管理 ========== -->')
sections.append('<div class="d-flex align-items-center mb-3">')
sections.append('    <div class="flex-grow-1"><hr class="my-0"></div>')
sections.append('    <h4 class="mx-3 mb-0 text-muted"><i class="bi bi-collection-play text-primary me-2"></i>采集管理</h4>')
sections.append('    <div class="flex-grow-1"><hr class="my-0"></div>')
sections.append('</div>')
sections.append(parts['collector']['content'])

# 2. 实时监控
sections.append('<!-- ========== 二、实时监控 ========== -->')
sections.append('<div class="d-flex align-items-center mb-3 mt-5">')
sections.append('    <div class="flex-grow-1"><hr class="my-0"></div>')
sections.append('    <h4 class="mx-3 mb-0 text-muted"><i class="bi bi-activity text-primary me-2"></i>实时监控</h4>')
sections.append('    <div class="flex-grow-1"><hr class="my-0"></div>')
sections.append('</div>')
sections.append(parts['monitoring']['content'])

# 3. 采集源码
sections.append('<!-- ========== 三、采集源码 ========== -->')
sections.append('<div class="d-flex align-items-center mb-3 mt-5">')
sections.append('    <div class="flex-grow-1"><hr class="my-0"></div>')
sections.append('    <h4 class="mx-3 mb-0 text-muted"><i class="bi bi-code-square text-primary me-2"></i>采集源码</h4>')
sections.append('    <div class="flex-grow-1"><hr class="my-0"></div>')
sections.append('</div>')
sections.append(parts['source_code']['content'])

# 4. 数据来源
sections.append('<!-- ========== 四、数据来源 ========== -->')
sections.append('<div class="d-flex align-items-center mb-3 mt-5">')
sections.append('    <div class="flex-grow-1"><hr class="my-0"></div>')
sections.append('    <h4 class="mx-3 mb-0 text-muted"><i class="bi bi-database-check text-primary me-2"></i>数据来源</h4>')
sections.append('    <div class="flex-grow-1"><hr class="my-0"></div>')
sections.append('</div>')
sections.append(parts['provenance']['content'])

# 5. 数据归集
sections.append('<!-- ========== 五、数据归集 ========== -->')
sections.append('<div class="d-flex align-items-center mb-3 mt-5">')
sections.append('    <div class="flex-grow-1"><hr class="my-0"></div>')
sections.append('    <h4 class="mx-3 mb-0 text-muted"><i class="bi bi-archive text-primary me-2"></i>数据归集</h4>')
sections.append('    <div class="flex-grow-1"><hr class="my-0"></div>')
sections.append('</div>')
sections.append(parts['data_archive']['content'])

# 收集所有 JS
all_js = []
for name in ['collector', 'monitoring', 'source_code', 'provenance', 'data_archive']:
    if parts[name]['js']:
        all_js.append(f'// ===== {name} JS =====')
        all_js.append(parts[name]['js'])

# 组装最终文件
css_block = '\n'.join(all_css) if all_css else ''
js_block = '\n'.join(all_js) if all_js else ''
content_block = '\n'.join(sections)

output = f'''{{% extends "base.html" %}}

{{% block extra_css %}}
<style>
/* 分割线标题样式 */
.section-divider {{
    color: rgba(0,0,0,0.4);
    font-weight: 600;
}}
.section-divider i {{
    font-size: 1.2rem;
}}
</style>
{css_block}
{{% endblock %}}

{{% block content %}}
<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h2 class="mb-1">采集管理</h2>
        <p class="text-muted mb-0">采集任务、实时监控、源码公开、数据溯源与归集一体化管理</p>
    </div>
    <div>
        <a href="/api/export/csv" class="btn btn-outline-primary">
            <i class="bi bi-download"></i> 导出CSV
        </a>
    </div>
</div>

{content_block}
{{% endblock %}}

{{% block extra_js %}}
<script>
{js_block}
</script>
{{% endblock %}}
'''

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(output)

print(f'\\ndashboard.html generated: {len(output)} chars, {len(output.splitlines())} lines')
