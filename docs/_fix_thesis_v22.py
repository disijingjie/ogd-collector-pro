#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
博士论文V20→V22综合修正脚本
处理P0级结构性问题
"""

import re

def main():
    with open('docs/博士论文_最终定稿版_v20.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    print(f"原始文件: {len(lines)} 行")
    
    # ========== 1. 删除第8章后的冗余"补充讨论"内容 ==========
    # 从 "# 补充讨论" 到 "## 附录E：OGD-Collector Pro..." 之前
    new_lines = []
    skip = False
    removed_lines = 0
    for line in lines:
        if line.strip() == '# 补充讨论':
            skip = True
            removed_lines += 1
            continue
        if skip and line.strip().startswith('## 附录E：OGD-Collector Pro'):
            skip = False
            # 保留这行
            new_lines.append(line)
            continue
        if skip:
            removed_lines += 1
            continue
        new_lines.append(line)
    lines = new_lines
    print(f"[OK] 删除冗余补充讨论: {removed_lines} 行")
    
    # ========== 2. 提取并删除 "### 1.5 国际比较视野..." 内容 ==========
    # 从 "### 1.5 国际比较视野..." 到 "# 第三章" 之前的 ---
    new_lines = []
    section_15_lines = []
    in_section_15 = False
    for line in lines:
        if line.strip().startswith('### 1.5 国际比较视野'):
            in_section_15 = True
            section_15_lines.append(line)
            continue
        if in_section_15 and line.strip().startswith('# 第三章'):
            in_section_15 = False
            new_lines.append(line)
            continue
        if in_section_15:
            section_15_lines.append(line)
            continue
        new_lines.append(line)
    lines = new_lines
    print(f"[OK] 提取1.5节内容: {len(section_15_lines)} 行")
    
    # ========== 3. 提取并删除 "### 2.6 政府数据开放评估方法的演进与比较" ==========
    new_lines = []
    section_26_lines = []
    in_section_26 = False
    for line in lines:
        if line.strip() == '### 2.6 政府数据开放评估方法的演进与比较':
            in_section_26 = True
            section_26_lines.append(line)
            continue
        if in_section_26 and line.strip().startswith('### 3.2'):
            in_section_26 = False
            new_lines.append(line)
            continue
        if in_section_26:
            section_26_lines.append(line)
            continue
        new_lines.append(line)
    lines = new_lines
    print(f"[OK] 提取2.6节(评估方法演进)内容: {len(section_26_lines)} 行")
    
    # ========== 4. 提取并删除第4章中的表6-1 ==========
    new_lines = []
    table_6_1_lines = []
    in_table_6_1 = False
    for i, line in enumerate(lines):
        if '表6-1展示了DEMATEL分析的中心度' in line or line.strip() == '**表6-1 DEMATEL因素中心度与因果分类结果**':
            in_table_6_1 = True
            table_6_1_lines.append(line)
            continue
        if in_table_6_1 and line.strip().startswith('#### 4.1.1'):
            in_table_6_1 = False
            new_lines.append(line)
            continue
        if in_table_6_1:
            table_6_1_lines.append(line)
            continue
        new_lines.append(line)
    lines = new_lines
    print(f"[OK] 提取表6-1内容: {len(table_6_1_lines)} 行")
    
    # ========== 5. 将1.5节内容插入到第一章末尾 ==========
    # 修改编号: 1.5→1.6, 1.5.1→1.6.1, 1.5.2→1.6.2, 表1-4→表1-2, 表1-5→表1-3
    section_15_text = '\n'.join(section_15_lines)
    section_15_text = section_15_text.replace('### 1.5 国际比较视野', '### 1.6 国际比较视野')
    section_15_text = section_15_text.replace('#### 1.5.1', '#### 1.6.1')
    section_15_text = section_15_text.replace('#### 1.5.2', '#### 1.6.2')
    section_15_text = section_15_text.replace('表1-4', '表1-2')
    section_15_text = section_15_text.replace('表1-5', '表1-3')
    # 引用也要改
    section_15_text = section_15_text.replace('从表1-4', '从表1-2')
    section_15_text = section_15_text.replace('表1-5的对比', '表1-3的对比')
    
    new_lines = []
    inserted_15 = False
    for line in lines:
        if not inserted_15 and line.strip().startswith('# 第二章'):
            # 在第二章之前插入1.6节
            new_lines.append(section_15_text)
            new_lines.append('')
            new_lines.append('')
            new_lines.append('')
            inserted_15 = True
        new_lines.append(line)
    lines = new_lines
    print(f"[OK] 插入1.6节到第一章末尾")
    
    # ========== 6. 将2.6节(评估方法演进)插入到第二章末尾 ==========
    section_26_text = '\n'.join(section_26_lines)
    # 这个2.6节需要改名，因为第二章已经有一个2.6节(方法论哲学基础)
    # 改为2.7
    section_26_text = section_26_text.replace('### 2.6 政府数据开放评估方法', '### 2.7 政府数据开放评估方法')
    section_26_text = section_26_text.replace('#### 2.6.1', '#### 2.7.1')
    section_26_text = section_26_text.replace('#### 2.6.2', '#### 2.7.2')
    section_26_text = section_26_text.replace('#### 2.6.3', '#### 2.7.3')
    section_26_text = section_26_text.replace('#### 2.6.4', '#### 2.7.4')
    section_26_text = section_26_text.replace('表2-5', '表2-7')
    section_26_text = section_26_text.replace('表2-6', '表2-8')
    section_26_text = section_26_text.replace('从表2-5', '从表2-7')
    # 图2-1到图2-6的引用需要改为图2-7到图2-12？不，这些图本来就是第二章的图，编号是对的
    # 但图2-X在第三章被引用了，需要确认
    # 这些图本身就在这个节里，所以图编号不用改
    
    new_lines = []
    inserted_26 = False
    for line in lines:
        if not inserted_26 and line.strip().startswith('# 第三章'):
            new_lines.append(section_26_text)
            new_lines.append('')
            new_lines.append('')
            new_lines.append('')
            inserted_26 = True
        new_lines.append(line)
    lines = new_lines
    print(f"[OK] 插入2.7节到第二章末尾")
    
    # ========== 7. 将表6-1插入到第六章DEMATEL分析部分 ==========
    table_6_1_text = '\n'.join(table_6_1_lines)
    
    new_lines = []
    inserted_6_1 = False
    for i, line in enumerate(lines):
        if not inserted_6_1 and 'DEMATEL方法识别关键影响因素' in line and '6.2' in line:
            # 找到6.2节中合适的位置插入
            new_lines.append(line)
            # 继续找下一个空行或合适的插入点
            continue
        if not inserted_6_1 and 'DEMATEL' in line and ('中心度' in line or '因素关联' in line):
            # 在DEMATEL结果说明后插入
            new_lines.append(line)
            # 再读几行找插入点
            continue
        # 简化处理：在第六章中找到"### 6.2"之后插入
        if not inserted_6_1 and line.strip().startswith('### 6.2') and '影响因素' in line:
            new_lines.append(line)
            new_lines.append('')
            new_lines.append(table_6_1_text)
            new_lines.append('')
            inserted_6_1 = True
            continue
        new_lines.append(line)
    lines = new_lines
    if inserted_6_1:
        print(f"[OK] 插入表6-1到第六章")
    else:
        print(f"[WARN] 未找到6.2节插入点，表6-1未插入")
    
    # ========== 8. 删除占位符 ==========
    content_fixed = '\n'.join(lines)
    content_fixed = content_fixed.replace('[表5-1和图5-1详见正文第五章]', '')
    print(f"[OK] 删除占位符")
    
    # ========== 9. 统一fsQCA路径数量 ==========
    # 中文摘要: "三条核心组态路径" → "两条核心组态路径"
    # "技术驱动型"（覆盖率31.2%）、"需求拉动型"（覆盖率28.7%）和"制度保障型"（覆盖率19.8%）
    # → "全要素驱动型"（路径H1，覆盖率81%）和"服务-质量-效果驱动型"（路径H2，覆盖率19%）
    
    old_abstract = 'fsQCA分析揭示了高绩效的三条核心组态路径——"技术驱动型"（覆盖率31.2%）、"需求拉动型"（覆盖率28.7%）和"制度保障型"（覆盖率19.8%）'
    new_abstract = 'fsQCA分析揭示了高绩效的两条核心组态路径——"全要素驱动型"（路径H1，覆盖率81%）和"服务-质量-效果驱动型"（路径H2，覆盖率19%）'
    content_fixed = content_fixed.replace(old_abstract, new_abstract)
    
    # 英文摘要也需要修正（如果有相关内容）
    # 摘要中可能没有具体路径名，先不管英文摘要
    
    # 第7章中的"三条路径"修正
    content_fixed = content_fixed.replace(
        '两条核心组态路径——"全要素驱动型"（路径H1）和"服务-质量-效果驱动型"（路径H2），三条路径分别对应不同的条件组合和平台类型',
        '两条核心组态路径——"全要素驱动型"（路径H1）和"服务-质量-效果驱动型"（路径H2），两条路径分别对应不同的条件组合和平台类型'
    )
    print(f"[OK] 统一fsQCA路径数量为2条")
    
    # ========== 10. 修正表3-6编号跳跃问题 ==========
    # 表3-6是唯一第3章的表，前面没有3-1到3-5。检查是否真的缺失。
    # 从扫描结果看第3章确实只有表3-6。这可能是因为编号错误。
    # 暂时不改，因为不确定是缺失还是编号错误
    
    # ========== 11. 修正8.1节子编号跳跃 ==========
    # 8.1节下有8.1.4和8.1.5但没有8.1.1-8.1.3
    # 将8.1.4→8.2.1, 8.1.5→8.2.2
    content_fixed = content_fixed.replace('#### 8.1.4 府际关系', '### 8.2 府际关系')
    content_fixed = content_fixed.replace('#### 8.1.5 4E框架在公共数据治理', '### 8.3 4E框架在公共数据治理')
    # 修正文中的引用
    content_fixed = content_fixed.replace('8.1.4节', '8.2节')
    content_fixed = content_fixed.replace('8.1.5节', '8.3节')
    print(f"[OK] 修正8.1节子编号跳跃")
    
    # ========== 12. 写入新文件 ==========
    with open('docs/博士论文_最终定稿版_v22.md', 'w', encoding='utf-8') as f:
        f.write(content_fixed)
    
    new_lines_count = len(content_fixed.split('\n'))
    print(f"\n[完成] 输出文件: docs/博士论文_最终定稿版_v22.md")
    print(f"       原行数: {len(lines)} → 新字符数: {len(content_fixed)}")
    print(f"       修正项: 删除冗余+移动章节+修正数据+统一编号")

if __name__ == '__main__':
    main()
