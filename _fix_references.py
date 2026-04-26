import re

# 读取论文
with open('docs/博士论文_最终定稿版_v10.md', 'r', encoding='utf-8') as f:
    content = f.read()

original = content
changes = []

# 1. 删除重复文献并映射引用
# [69] = [6] 郑磊同一篇文章
# [128] = [118] Veljkovic同一篇文章（拼写差异）
# [129] = [100] Attard同一篇文章

# 先删除重复文献条目
for dup_num in [69, 128, 129]:
    pattern = rf'\n\n\[{dup_num}\] [^\n]+\n\n'
    match = re.search(pattern, content)
    if match:
        content = content[:match.start()] + content[match.end():]
        changes.append(f'删除重复文献[{dup_num}]')

# 2. 更新正文中的引用编号
ref_map = {69: 6, 128: 118, 129: 100}

for old_num, new_num in ref_map.items():
    # 匹配引用格式：[数字] 或 [数字, 数字] 或 [数字-数字]
    # 需要小心处理，避免误替换
    old_str = f'[{old_num}]'
    new_str = f'[{new_num}]'
    
    count = 0
    # 只在非参考文献区域替换（参考文献区域在2576行之后）
    # 找到参考文献开始位置
    ref_start = content.find('## 中文文献')
    if ref_start == -1:
        ref_start = len(content)
    
    # 替换参考文献之前的区域
    pre_ref = content[:ref_start]
    post_ref = content[ref_start:]
    
    # 在pre_ref中替换
    pre_ref_new = pre_ref.replace(old_str, new_str)
    if pre_ref_new != pre_ref:
        count = pre_ref.count(old_str)
        pre_ref = pre_ref_new
        changes.append(f'正文引用[{old_num}]→[{new_num}]: {count}处')
    
    content = pre_ref + post_ref

# 3. 修正明显的格式错误
# [11] 作者名"赵需要的"→"赵需要"
content = content.replace('张涛, 赵需要的. 基于平衡计分卡', '张涛, 赵需要. 基于平衡计分卡')
changes.append('修正[11]作者名: 赵需要的→赵需要')

# 4. 英文文献作者格式统一：将", &"统一为" & "（GB/T 7714要求英文作者之间用&连接最后两个）
# 这个已经在格式中了，不需要修改

# 保存
if content != original:
    with open('docs/博士论文_最终定稿版_v10.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'参考文献修复完成，共{len(changes)}项变更：')
    for c in changes:
        print(f'  - {c}')
else:
    print('未检测到需要修复的参考文献问题')
