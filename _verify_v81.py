import re

with open('docs/博士论文_终极重构版_v8_1.md', 'r', encoding='utf-8') as f:
    content = f.read()

checks = {
    'DEMATEL-fsQCA逻辑闭环': '因素识别' in content and '路径组合' in content,
    '文献批判性评述': '重建设轻运营' in content,
    '样本剔除说明': '幸存者偏差' in content,
    '口径幻觉归因': '技术理性的局限' in content,
    '策略强绑定路径': '资源驱动-技术赋能型' in content,
    '4E理论升华': '语境化' in content,
    '术语统一': '省级政府数据开放平台' in content,
}

print('=== V8.1版本关键重构点验证 ===')
all_pass = True
for name, exists in checks.items():
    status = 'PASS' if exists else 'FAIL'
    if not exists:
        all_pass = False
    print(f'{status}: {name}')

clean = re.sub(r'```[\s\S]*?```', '', content)
clean = re.sub(r'!\[.*?\]\((.*?)\)', '', clean)
clean = re.sub(r'\[.*?\]\(.*?\)', '', clean)
clean = re.sub(r'#+\s*', '', clean)
clean = re.sub(r'[*\-_`>]', '', clean)
clean = re.sub(r'\s+', '', clean)
print(f'\n总字符数: {len(content)}')
print(f'纯文本字数: {len(clean)}')
if all_pass:
    print('结果: 全部通过!')
else:
    print('结果: 存在失败项!')
