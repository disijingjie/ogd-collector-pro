import re

def final_fix():
    input_file = 'docs/博士论文_终极重构版_v8_1.md'
    output_file = 'docs/博士论文_最终定稿版_v9.md'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print("开始执行最终修正...")

    # 1. 清理模糊图表引用
    print("  -> 清理模糊图表引用...")
    content = re.sub(r'如下表所示', '如相关表格所示', content)
    content = re.sub(r'如下图所示', '如相关图表所示', content)
    # 保留"如图X-X所示"的精确引用，只清理模糊的

    # 2. 检查第八章结构 - 查找是否有附录内容混入了第八章
    print("  -> 检查第八章结构...")
    ch8_start = content.find('# 第8章 第八章 结论与展望')
    if ch8_start > 0:
        ch8_content = content[ch8_start:]
        # 检查是否有附录标记
        appendix_markers = re.findall(r'#{1,3}\s*附录[ABCDEFG]', ch8_content)
        if appendix_markers:
            print(f"     发现附录标记在第八章后: {appendix_markers}")
            # 在第一个附录标记前插入分隔
            first_appendix = ch8_content.find('附录')
            if first_appendix > 0:
                # 找到附录前的换行位置
                before_appendix = ch8_content[:first_appendix].rfind('\n')
                if before_appendix > 0:
                    insert_pos = ch8_start + before_appendix
                    content = content[:insert_pos] + '\n\n---\n\n' + content[insert_pos:]
                    print("     已在附录前插入分隔符")

    # 3. 保存最终定稿版
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"最终定稿版已保存: {output_file}")
    print(f"字符数: {len(content)}")

if __name__ == '__main__':
    final_fix()
