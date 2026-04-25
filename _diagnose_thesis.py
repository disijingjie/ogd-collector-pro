import re
import os

with open('docs/博士论文_完整版_v4.md', 'r', encoding='utf-8') as f:
    content = f.read()

print('=== 论文全面诊断报告 ===')
print()

# 1. 字数
print('【字数统计】')
clean = re.sub(r'```[\s\S]*?```', '', content)
clean = re.sub(r'!\[.*?\]\(.*?\)', '', clean)
clean = re.sub(r'\[.*?\]\(.*?\)', '', clean)
clean = re.sub(r'#+\s*', '', clean)
clean = re.sub(r'[*\-_`>]', '', clean)
clean = re.sub(r'\s+', '', clean)
print(f'  Markdown总字符: {len(content)}')
print(f'  纯文本字数: {len(clean)}')
print()

# 2. 图片
print('【图片引用】')
img_refs = re.findall(r'!\[(.*?)\]\((.*?)\)', content)
print(f'  图片引用数量: {len(img_refs)}')
for alt, path in img_refs:
    exists = os.path.exists(path) if not path.startswith('http') else 'URL'
    print(f'    [{alt}] => {path} (存在: {exists})')
print()

# 3. 表格
print('【表格统计】')
table_blocks = re.findall(r'\n\|[^\n]+\|[\s\S]*?\n\|[-:\s|]+\|[\s\S]*?(?=\n\n|\n#|$)', content)
print(f'  表格数量: {len(table_blocks)}')
print()

# 4. 脚注
footnotes = re.findall(r'\[\^\d+\]', content)
print(f'【脚注引用】 {len(footnotes)} 处')
print()

# 5. 图表引用文字
fig_refs = re.findall(r'如图\d+-\d+', content)
table_refs = re.findall(r'如表\d+-\d+', content)
print(f'【文中引用】 图引用: {len(fig_refs)} 处, 表引用: {len(table_refs)} 处')
print()

# 6. 章节结构
ch_headers = re.findall(r'^# 第[一二三四五六七八九十]章.+', content, re.MULTILINE)
print(f'【章节标题】 {len(ch_headers)} 个')
for h in ch_headers:
    print(f'  {h}')
print()

# 7. 重复内容检测
print('【高频词检测】')
words = ['数据口径幻觉', '开放数林指数', '4E框架', 'fsQCA', 'DEMATEL', 'TOPSIS', 'DEA']
for w in words:
    count = content.count(w)
    print(f'  "{w}": {count}次')
print()

# 8. 现有图表文件
print('【本地图表文件】')
if os.path.exists('static'):
    for f in sorted(os.listdir('static')):
        if f.endswith('.png') and ('thesis' in f or 'chart' in f or 'map' in f):
            size = os.path.getsize(f'static/{f}')
            print(f'  {f} ({size//1024}KB)')
print()

print('=== 诊断完成 ===')
