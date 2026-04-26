import re

with open('docs/博士论文_最终定稿版_v10.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找所有'22个'出现的位置
pattern = r'22个'
matches = [(m.start(), m.group()) for m in re.finditer(pattern, content)]
print(f"找到 {len(matches)} 处'22个'")

for pos, match in matches:
    start = max(0, pos-40)
    end = min(len(content), pos+len(match)+40)
    context = content[start:end].replace('\n', ' ')
    print(f"  ...{context}...")
