#!/usr/bin/env python3
"""
V19论文批量脚注转换脚本
功能：
1. 从_引用数据库.md读取所有引用条目
2. 读取博士论文_最终定稿版_v10.md全文
3. 基于关键词映射，为正文添加脚注引用
4. 在文末追加完整参考文献列表
5. 输出为新的Markdown文件
"""

import re
import os
from collections import OrderedDict

# ============ 配置路径 ============
DB_PATH = r"C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system\docs\_引用数据库.md"
THESIS_PATH = r"C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system\docs\博士论文_最终定稿版_v10.md"
OUTPUT_PATH = r"C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system\docs\博士论文_最终定稿版_v20.md"

# ============ 第一步：读取引用数据库 ============
def parse_reference_database(path):
    """解析引用数据库，返回编号→内容的字典"""
    refs = OrderedDict()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 匹配 [^数字]: 内容
            m = re.match(r'\[\^(\d+)\]:\s*(.+)', line)
            if m:
                num = m.group(1)
                content = m.group(2).strip()
                refs[num] = content
    return refs

# ============ 第二步：建立关键词→编号映射 ============
def build_keyword_map(refs):
    """
    从引用内容中提取关键词，建立关键词→编号的映射。
    策略：
    - 中文文献：提取作者名（逗号前的部分）
    - 英文文献：提取主要作者姓
    - 政策文件：提取文件名称中的关键词
    """
    keyword_map = {}
    
    for num, content in refs.items():
        keywords = []
        
        # 中文文献：提取作者名（第一个逗号前的部分）
        if re.search(r'[\u4e00-\u9fff]', content):
            # 中文作者名通常在开头，如"郑磊, 刘新萍"或"中共中央, 国务院"
            authors_part = content.split('.')[0] if '.' in content else content.split('[')[0]
            authors = [a.strip() for a in authors_part.split(',')]
            for author in authors[:2]:  # 取前两个作者
                if author and len(author) <= 10 and not re.match(r'\d', author):
                    keywords.append(author)
        else:
            # 英文文献：提取第一作者姓
            m = re.match(r'^([A-Z][a-zA-Z\-]+)', content)
            if m:
                keywords.append(m.group(1))
            # 也尝试提取第二作者（如果有 et al. 或 and）
            m2 = re.search(r',\s*([A-Z][a-zA-Z\-]+)', content)
            if m2:
                keywords.append(m2.group(1))
        
        # 提取标题中的关键词（对于政策文件等）
        title_match = re.search(r'《(.+?)》', content)
        if title_match:
            keywords.append(title_match.group(1))
        
        # 特殊关键词映射
        special_maps = {
            '243': ['OECD', 'Open Government Data'],
            '222': ['Data.gov'],
            '220': ['data.gov.uk'],
            '6': ['开放数林', '中国开放数林指数'],
            '10': ['数据二十条', '关于构建数据基础制度'],
            '49': ['促进大数据发展行动纲要'],
            '51': ['数据安全法'],
            '52': ['个人信息保护法'],
            '53': ['关于加快公共数据资源开发利用'],
            '225': ['Moore', 'Creating public value'],
            '228': ['Ragin', 'Redesigning social inquiry'],
            '231': ['Janssen', 'Zuiderwijk'],
            '272': ['Nardi', "O'Day", 'Information ecologies'],
            '274': ['Horton', 'Information resources management'],
            '269': ['马费成', '信息管理学基础'],
            '270': ['信息资源管理'],
            '276': ['Rawls', 'A theory of justice'],
            '277': ['Norris', 'Digital divide'],
        }
        if num in special_maps:
            for kw in special_maps[num]:
                if kw not in keywords:
                    keywords.append(kw)
        
        # 去重并加入映射
        for kw in keywords:
            kw = kw.strip()
            # 过滤掉过短或过于通用的关键词
            if not kw or len(kw) < 3:
                continue
            # 排除通用词（避免误匹配）
            stopwords = {'Open', 'Data', 'the', 'and', 'for', 'Government', 'Information', 'Management', 'Research', 'Public', 'Analysis', 'Evaluation', 'System', 'Model', 'Method', 'Framework', 'Theory', 'Study', 'Review', 'Based', 'Using', 'Application', 'Approach', 'Case', 'Development', 'Design', 'Process', 'Performance', 'Service', 'Quality', 'Technology', 'Digital', 'China', 'Chinese', 'Local', 'National', 'Regional', 'Social', 'Economic', 'Political', 'Policy', 'Strategies', 'Factors', 'Effects', 'Impact', 'Influence', 'Relationship', 'Between', 'Among', 'With', 'From', 'Into', 'Over', 'Under', 'Through', 'During', 'Before', 'After', 'Above', 'Below', 'Within', 'Without', 'Against', 'Towards', 'Regarding', 'Concerning', 'Considering', 'Following', 'Including', 'Excluding', 'Involving', 'Concerning'}
            if kw in stopwords:
                continue
            # 长关键词优先（避免短关键词误匹配）
            if kw not in keyword_map or len(kw) > len(keyword_map.get(kw, '')):
                keyword_map[kw] = num
    
    return keyword_map

# ============ 第三步：处理正文脚注 ============
def add_footnotes_to_text(text, keyword_map, refs):
    """
    为正文添加脚注引用。
    策略：
    1. 找出所有"裸露"的关键词（没有[^...]保护的）
    2. 在关键词后添加脚注引用
    3. 避免在URL、代码块、图片引用等位置添加
    """
    
    # 按关键词长度降序排列（长关键词先匹配，避免短关键词误匹配）
    sorted_keywords = sorted(keyword_map.keys(), key=lambda x: -len(x))
    
    # 记录已经处理过的位置
    processed_positions = set()
    
    # 统计替换次数
    replacements = {}
    
    new_text = text
    
    for kw in sorted_keywords:
        num = keyword_map[kw]
        footnote = f'[^{num}]'
        
        # 构建正则：匹配关键词，但要求后面不是 [^ 或 [^数字]
        # 同时避免在URL、图片引用、表格内部匹配
        pattern = re.compile(
            r'(?<![\w\u4e00-\u9fff])' + re.escape(kw) + 
            r'(?![\w\u4e00-\u9fff])(?!\[\^)(?!\s*\[\^)(?!.*?\]\(http)',
            re.IGNORECASE if not re.search(r'[\u4e00-\u9fff]', kw) else 0
        )
        
        def replace_fn(match):
            pos = match.start()
            # 检查这个位置是否已经被处理过
            if pos in processed_positions:
                return match.group(0)
            
            # 检查是否在图片引用、URL、表格分隔线内
            surrounding = new_text[max(0, pos-50):pos+len(kw)+50]
            if re.search(r'!\[.*?\]\(', surrounding):
                # 可能是图片alt文本内，跳过
                if abs(surrounding.find('![') - (pos - max(0, pos-50))) < 30:
                    return match.group(0)
            if re.search(r'\(https?://', surrounding):
                # URL附近，跳过
                return match.group(0)
            
            processed_positions.add(pos)
            replacements[kw] = replacements.get(kw, 0) + 1
            return match.group(0) + footnote
        
        new_text = pattern.sub(replace_fn, new_text)
    
    return new_text, replacements

# ============ 第四步：追加参考文献列表 ============
def append_references(text, refs):
    """在文末追加参考文献列表"""
    
    # 检查是否已有参考文献部分
    if '# 参考文献' in text or '## 参考文献' in text:
        return text
    
    ref_section = '\n\n---\n\n# 参考文献\n\n'
    
    # 分类输出
    cn_refs = []
    en_refs = []
    
    for num, content in refs.items():
        if re.search(r'[\u4e00-\u9fff]', content):
            cn_refs.append(f'[{num}] {content}')
        else:
            en_refs.append(f'[{num}] {content}')
    
    if cn_refs:
        ref_section += '## 中文文献\n\n'
        ref_section += '\n\n'.join(cn_refs)
        ref_section += '\n\n'
    
    if en_refs:
        ref_section += '## 英文文献\n\n'
        ref_section += '\n\n'.join(en_refs)
        ref_section += '\n\n'
    
    return text + ref_section

# ============ 主程序 ============
def main():
    print("=" * 60)
    print("V19论文批量脚注转换脚本")
    print("=" * 60)
    
    # 1. 读取引用数据库
    print("\n[1/4] 读取引用数据库...")
    refs = parse_reference_database(DB_PATH)
    print(f"    共读取 {len(refs)} 条引用")
    
    # 2. 建立关键词映射
    print("\n[2/4] 建立关键词映射...")
    keyword_map = build_keyword_map(refs)
    print(f"    共建立 {len(keyword_map)} 个关键词映射")
    
    # 3. 读取论文全文
    print("\n[3/4] 读取论文全文...")
    with open(THESIS_PATH, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"    论文总长度: {len(text)} 字符")
    
    # 4. 添加脚注
    print("\n[4/4] 批量添加脚注引用...")
    new_text, replacements = add_footnotes_to_text(text, keyword_map, refs)
    print(f"    共完成 {len(replacements)} 个关键词的脚注添加")
    print(f"    替换详情（前20个）：")
    for kw, count in sorted(replacements.items(), key=lambda x: -x[1])[:20]:
        print(f"      - {kw}: {count}次")
    
    # 5. 追加参考文献
    print("\n[5/5] 追加参考文献列表...")
    new_text = append_references(new_text, refs)
    
    # 6. 输出文件
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print(f"\n✅ 输出文件: {OUTPUT_PATH}")
    print(f"   文件大小: {os.path.getsize(OUTPUT_PATH) / 1024:.1f} KB")
    
    # 统计信息
    footnote_count = len(re.findall(r'\[\^\d+\]', new_text))
    unique_footnotes = len(set(re.findall(r'\[\^(\d+)\]', new_text)))
    print(f"   脚注总次数: {footnote_count}")
    print(f"   唯一引用数: {unique_footnotes}")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
