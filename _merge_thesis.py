# -*- coding: utf-8 -*-
import os

# 定义章节顺序和文件路径
chapters = [
    ('第一章 绪论', 'docs/新论文_第一章_绪论.md'),
    ('第二章 理论基础与文献综述', 'docs/新论文_第二章_扩充版.md'),
    ('第三章 4E评估框架构建', 'docs/新论文_第三章_扩充版.md'),
    ('第四章 研究设计', 'docs/chapter4_full_v2.md'),
    ('第五章 绩效评估', 'docs/chapter5_final_v2.md'),
    ('第六章 影响因素分析', 'docs/chapter6_full.md'),
    ('第七章 对策建议', 'docs/chapter7_full.md'),
    ('第八章 结论与展望', 'docs/chapter8_full.md'),
]

# 数据更新文件（用于补充引用）
data_updates = {
    1: 'docs/chapter1_data_update.md',
    2: 'docs/chapter2_data_update.md',
    3: 'docs/chapter3_data_update.md',
}

total_chars = 0
output_lines = []

# 论文标题
output_lines.append('# 中国省级政府数据开放平台绩效评估研究')
output_lines.append('')
output_lines.append('## ——基于4E框架的实证分析')
output_lines.append('')
output_lines.append('---')
output_lines.append('')

for ch_num, (ch_title, filepath) in enumerate(chapters, 1):
    print(f'正在处理第{ch_num}章: {ch_title}')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        chars = len(content)
        total_chars += chars
        print(f'  - 文件: {filepath}, 字符数: {chars}')
        
        # 添加章节标题
        output_lines.append('')
        output_lines.append('---')
        output_lines.append('')
        # 提取章节名称（去掉"第X章"前缀）
        short_title = ch_title
        if f'第{ch_num}章 ' in ch_title:
            short_title = ch_title.replace(f'第{ch_num}章 ', '')
        output_lines.append(f'# 第{ch_num}章 {short_title}')
        output_lines.append('')
        
        # 处理内容：移除文件中的顶级标题，避免重复
        lines = content.split('\n')
        skip_first_h1 = False
        for line in lines:
            if line.startswith('# ') and not skip_first_h1:
                skip_first_h1 = True
                continue
            # 调整标题层级：文件中的 ## -> ###（因为我们已经加了#章标题）
            if line.startswith('#') and not line.startswith('# '):
                output_lines.append('#' + line)
            else:
                output_lines.append(line)
        
        # 如果有数据更新，追加到章节末尾
        if ch_num in data_updates and os.path.exists(data_updates[ch_num]):
            with open(data_updates[ch_num], 'r', encoding='utf-8') as f:
                update_content = f.read()
            output_lines.append('')
            output_lines.append('---')
            output_lines.append('')
            output_lines.append('> **数据更新说明**：以下为本章实证数据的最新统计结果。')
            output_lines.append('')
            # 同样调整标题层级
            for line in update_content.split('\n'):
                if line.startswith('#') and not line.startswith('# '):
                    output_lines.append('#' + line)
                elif line.startswith('# '):
                    output_lines.append('## ' + line[2:])
                else:
                    output_lines.append(line)
    else:
        print(f'  - 警告: 文件不存在 {filepath}')

# 添加参考文献部分
output_lines.append('')
output_lines.append('---')
output_lines.append('')
output_lines.append('# 参考文献')
output_lines.append('')
output_lines.append('（详见参考文献管理文件）')
output_lines.append('')

# 写入完整论文
output_path = 'docs/博士论文_完整版_v4.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print('')
print('✅ 论文合并完成！')
print(f'总字符数: {total_chars}')
print(f'输出文件: {output_path}')
print(f'文件大小: {os.path.getsize(output_path)} 字节')
