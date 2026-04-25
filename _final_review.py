import re

with open('docs/博士论文_终极重构版_v8_1.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查各章字数分布
chapters = re.findall(r'^# 第\d+章 .+', content, re.MULTILINE)
print('=== 各章字数分布 ===')
for i, c in enumerate(chapters):
    ch_num = re.search(r'第(\d+)章', c).group(1)
    pattern = f'^# 第{ch_num}章 .+'
    parts = re.split(pattern, content, flags=re.MULTILINE)
    if len(parts) > 1:
        next_ch = re.search(r'^# 第\d+章 .+', parts[1], re.MULTILINE)
        if next_ch:
            ch_content = parts[1][:next_ch.start()]
        else:
            ch_content = parts[1]
        clean = re.sub(r'```[\s\S]*?```', '', ch_content)
        clean = re.sub(r'!\[.*?\]\((.*?)\)', '', clean)
        clean = re.sub(r'\[.*?\]\(.*?\)', '', clean)
        clean = re.sub(r'#+\s*', '', clean)
        clean = re.sub(r'[*\-_`>]', '', clean)
        clean = re.sub(r'\s+', '', clean)
        print(f'第{ch_num}章: {len(clean)}字')

# 检查关键术语一致性
terms = ['省级政府数据开放平台', '开放数据平台', '地方数据平台', '公共数据开放平台']
print('\n=== 术语一致性检查 ===')
for t in terms:
    count = content.count(t)
    print(f'{t}: {count}次')

# 检查口语化表达残留
oral = ['我们可以看出', '很明显', '非常有意思', '有意思的是', '这说明']
print('\n=== 口语化表达检查 ===')
for o in oral:
    count = content.count(o)
    if count > 0:
        print(f'FAIL "{o}": {count}次')
    else:
        print(f'PASS "{o}": 0次')

# 检查图表引用规范性
vague_refs = len(re.findall(r'如下表所示|如下图所示|如图', content))
precise_refs = len(re.findall(r'如表\d+-\d+', content)) + len(re.findall(r'如图\d+-\d+', content))
print(f'\n=== 图表引用规范性 ===')
print(f'模糊引用（如下表所示）: {vague_refs}次')
print(f'精确引用（如表X-X）: {precise_refs}次')

# 总字数
clean_all = re.sub(r'```[\s\S]*?```', '', content)
clean_all = re.sub(r'!\[.*?\]\((.*?)\)', '', clean_all)
clean_all = re.sub(r'\[.*?\]\(.*?\)', '', clean_all)
clean_all = re.sub(r'#+\s*', '', clean_all)
clean_all = re.sub(r'[*\-_`>]', '', clean_all)
clean_all = re.sub(r'\s+', '', clean_all)
print(f'\n总字符数: {len(content)}')
print(f'纯文本字数: {len(clean_all)}')
