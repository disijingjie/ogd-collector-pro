"""
扫描论文中所有图和表的引用，生成完整清单
"""
import re
import os

with open('docs/博士论文_最终定稿版_v10.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 扫描图引用
fig_refs = []
for line_num, line in enumerate(content.split('\n'), 1):
    # 匹配 ![图X-Y ...](path)
    m = re.search(r'!\[([^\]]+)\]\(([^)]+)\)', line)
    if m:
        caption, path = m.groups()
        fig_id = re.search(r'图\d+-\d+', caption)
        fig_refs.append({
            'line': line_num,
            'caption': caption.strip(),
            'path': path,
            'fig_id': fig_id.group() if fig_id else 'UNKNOWN'
        })

# 扫描表引用
table_refs = []
for line_num, line in enumerate(content.split('\n'), 1):
    # 匹配 **表X-Y 标题**
    m = re.search(r'\*\*(表\d+-\d+\s+[^*]+)\*\*', line)
    if m:
        table_refs.append({
            'line': line_num,
            'caption': m.group(1).strip()
        })

# 检查文件是否存在
for fig in fig_refs:
    full_path = os.path.join('c:/Users/MI/WorkBuddy/newbbbb/ogd_collector_system', fig['path'])
    fig['exists'] = os.path.exists(full_path)
    if fig['exists']:
        fig['size'] = os.path.getsize(full_path)

print(f"=== 论文中的图表清单 ===")
print(f"共发现 {len(fig_refs)} 张图")
print()
for fig in fig_refs:
    status = "存在" if fig['exists'] else "缺失"
    size = f"({fig['size']/1024:.1f}KB)" if fig['exists'] else ""
    print(f"  {fig['fig_id']:8} | {status:4} | {fig['path']:60} {size}")

print()
print(f"=== 论文中的表格清单 ===")
print(f"共发现 {len(table_refs)} 个表")
print()
for tbl in table_refs:
    print(f"  {tbl['line']:5} | {tbl['caption']}")

# 保存到文件
with open('_all_figures_tables_report.txt', 'w', encoding='utf-8') as f:
    f.write("=== 论文中的图表清单 ===\n")
    f.write(f"共发现 {len(fig_refs)} 张图\n\n")
    for fig in fig_refs:
        status = "存在" if fig['exists'] else "缺失"
        size = f"({fig['size']/1024:.1f}KB)" if fig['exists'] else ""
        f.write(f"  {fig['fig_id']:8} | {status:4} | {fig['path']:60} {size}\n")
    f.write("\n")
    f.write(f"=== 论文中的表格清单 ===\n")
    f.write(f"共发现 {len(table_refs)} 个表\n\n")
    for tbl in table_refs:
        f.write(f"  {tbl['line']:5} | {tbl['caption']}\n")

print("\n报告已保存到 _all_figures_tables_report.txt")
