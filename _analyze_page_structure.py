#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析各省级平台页面结构，找出数据集数量的显示位置
"""
import sys
import io
import os
import requests
import re
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

from bs4 import BeautifulSoup

# 测试几个已知可用的平台
PLATFORMS = [
    ("浙江", "https://data.zj.gov.cn"),
    ("山东", "https://data.sd.gov.cn"),
    ("广东", "https://gddata.gd.gov.cn"),
    ("江苏", "https://data.jszwfw.gov.cn:8118/extranet/openportal/pages/default/index.html"),
    ("四川", "https://scdata.net.cn"),
    ("贵州", "https://data.guizhou.gov.cn"),
    ("湖北", "https://data.hubei.gov.cn"),
]

# 常见的数据目录页面路径
CATALOG_PATHS = [
    "/oportal/catalog",
    "/oportal/catalog/index",
    "/dataset",
    "/catalog",
    "/data",
    "/directory",
    "/list",
]

def analyze_homepage(name, url):
    """分析首页结构"""
    print(f"\n{'='*60}")
    print(f"平台: {name} ({url})")
    print(f"{'='*60}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        resp = requests.get(url, headers=headers, timeout=15, verify=False)
        
        print(f"状态码: {resp.status_code}")
        print(f"内容长度: {len(resp.text)}")
        
        if resp.status_code != 200:
            return
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        text = soup.get_text()
        
        # 1. 搜索所有包含数字的文本节点
        print("\n--- 可能的计数显示 ---")
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        count_lines = []
        for line in lines:
            # 找包含数字+数据集/目录/条数等关键词的行
            if re.search(r'\d+', line) and any(k in line for k in ['数据集', '目录', '条数', '数据', '开放', '资源', '部门', '下载', '访问']):
                if len(line) < 100:  # 只显示短文本
                    count_lines.append(line)
        
        # 去重并显示前15个
        seen = set()
        for line in count_lines[:15]:
            if line not in seen:
                print(f"  {line}")
                seen.add(line)
        
        # 2. 搜索特定的DOM元素（class/id包含count/number/total等）
        print("\n--- 计数元素(class/id) ---")
        for elem in soup.find_all(attrs={"class": re.compile(r'count|num|total|sum|amount', re.I)}):
            text = elem.get_text(strip=True)
            if text and re.search(r'\d+', text):
                print(f"  class={elem.get('class')}: {text[:50]}")
        
        for elem in soup.find_all(attrs={"id": re.compile(r'count|num|total|sum|amount', re.I)}):
            text = elem.get_text(strip=True)
            if text and re.search(r'\d+', text):
                print(f"  id={elem.get('id')}: {text[:50]}")
        
        # 3. 搜索script中的数据
        print("\n--- Script中的数据变量 ---")
        for script in soup.find_all('script'):
            if script.string:
                # 搜索常见的数据变量名
                patterns = [
                    r'(datasetCount|totalCount|dataCount|catalogCount)\s*[:=]\s*(\d+)',
                    r'["\'](数据集|目录|总数)["\']\s*[:：]\s*(\d+)',
                ]
                for pattern in patterns:
                    matches = re.findall(pattern, script.string, re.I)
                    for m in matches[:5]:
                        print(f"  {m}")
        
        # 4. 探测子页面
        print("\n--- 探测数据目录页 ---")
        from urllib.parse import urljoin
        for path in CATALOG_PATHS[:3]:  # 只测前3个路径
            catalog_url = urljoin(url, path)
            try:
                cat_resp = requests.get(catalog_url, headers=headers, timeout=10, verify=False)
                if cat_resp.status_code == 200 and len(cat_resp.text) > 5000:
                    print(f"  {catalog_url}: OK (长度{len(cat_resp.text)})")
                    # 尝试在新页面中找计数
                    cat_soup = BeautifulSoup(cat_resp.text, 'html.parser')
                    cat_text = cat_soup.get_text()
                    count_match = re.search(r'(\d+)\s*个数据集', cat_text)
                    if count_match:
                        print(f"    找到数据集数: {count_match.group(1)}")
            except Exception as e:
                pass
        
    except Exception as e:
        print(f"错误: {str(e)[:100]}")

def main():
    print("=" * 60)
    print("省级平台页面结构分析")
    print("=" * 60)
    
    for name, url in PLATFORMS:
        analyze_homepage(name, url)
    
    print("\n" + "=" * 60)
    print("分析完成")
    print("=" * 60)

if __name__ == '__main__':
    main()
