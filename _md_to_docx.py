"""
将Markdown论文转换为Word文档（按武汉大学博士论文格式）
"""
import os
import re
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

def set_chinese_font(run, font_name='宋体', size=12, bold=False):
    """设置中文字体"""
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)

def md_to_docx(md_path, output_path):
    print("=" * 80)
    print("Markdown转Word")
    print("=" * 80)
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    doc = Document()
    
    # 设置页面大小（A4）
    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(3.17)
    
    # 设置默认字体
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)
    style._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    style.paragraph_format.line_spacing = 1.5
    style.paragraph_format.first_line_indent = Cm(0.74)  # 两个字符缩进
    
    # 处理标题样式
    heading_styles = {}
    for i in range(1, 4):
        h_style = doc.styles[f'Heading {i}']
        h_style.font.name = 'Times New Roman'
        h_style.font.size = Pt([16, 14, 12][i-1])
        h_style.font.bold = True
        h_style._element.rPr.rFonts.set(qn('w:eastAsia'), ['黑体', '黑体', '楷体'][i-1])
        h_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        h_style.paragraph_format.first_line_indent = Cm(0)
    
    # 解析Markdown
    lines = content.split('\n')
    i = 0
    in_table = False
    table_lines = []
    
    while i < len(lines):
        line = lines[i].strip()
        
        # 跳过分隔线和元数据
        if line.startswith('---') or line.startswith('> '):
            i += 1
            continue
        
        # 处理标题
        if line.startswith('# '):
            title = line[2:].strip()
            p = doc.add_heading(title, level=1)
            i += 1
            continue
        elif line.startswith('## '):
            title = line[3:].strip()
            p = doc.add_heading(title, level=2)
            i += 1
            continue
        elif line.startswith('### '):
            title = line[4:].strip()
            p = doc.add_heading(title, level=3)
            i += 1
            continue
        
        # 处理表格
        if line.startswith('|'):
            table_lines.append(line)
            i += 1
            # 检查是否表格结束
            if i < len(lines) and not lines[i].strip().startswith('|'):
                # 处理表格
                if len(table_lines) >= 2:
                    process_table(doc, table_lines)
                table_lines = []
            continue
        else:
            if table_lines:
                if len(table_lines) >= 2:
                    process_table(doc, table_lines)
                table_lines = []
        
        # 处理普通段落
        if line:
            # 处理Markdown格式
            p = doc.add_paragraph()
            # 简单的粗体和斜体处理
            parts = re.split(r'(\*\*.*?\*\*|\*.*?\*)', line)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    run = p.add_run(part[2:-2])
                    set_chinese_font(run, '宋体', 12, bold=True)
                elif part.startswith('*') and part.endswith('*'):
                    run = p.add_run(part[1:-1])
                    run.font.italic = True
                    set_chinese_font(run, '宋体', 12)
                else:
                    run = p.add_run(part)
                    set_chinese_font(run, '宋体', 12)
        else:
            # 空行
            pass
        
        i += 1
    
    # 保存
    doc.save(output_path)
    print("Word文档已保存:", output_path)
    
    # 统计
    total_chars = sum(len(p.text) for p in doc.paragraphs)
    chinese_chars = sum(len(re.findall(r'[\u4e00-\u9fff]', p.text)) for p in doc.paragraphs)
    print("总字符数:", total_chars)
    print("中文字符数:", chinese_chars)
    
    return output_path

def process_table(doc, table_lines):
    """处理Markdown表格"""
    # 过滤分隔行
    data_lines = [l for l in table_lines if not re.match(r'\|[-:\s|]+\|', l)]
    if len(data_lines) < 1:
        return
    
    # 解析单元格
    rows = []
    for line in data_lines:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if cells:
            rows.append(cells)
    
    if not rows:
        return
    
    num_cols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=num_cols)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    for i, row_data in enumerate(rows):
        row = table.rows[i]
        for j, cell_text in enumerate(row_data):
            if j < num_cols:
                cell = row.cells[j]
                cell.text = cell_text
                # 设置单元格字体
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        set_chinese_font(run, '宋体', 10)
                    paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

def main():
    md_path = 'docs/新论文_完整版_V15_扩充版.md'
    output_path = 'docs/博士论文_V15_真实数据版.docx'
    
    if not Path(md_path).exists():
        md_path = 'docs/新论文_完整版_V15_真实数据.md'
    
    md_to_docx(md_path, output_path)

if __name__ == '__main__':
    main()
