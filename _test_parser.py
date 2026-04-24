#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试增强版解析逻辑
"""
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

import requests
from collector_engine import CollectorEngine

def test_parser_on_platform(name, url):
    """测试解析器在真实平台上的表现"""
    print(f"\n{'='*60}")
    print(f"测试: {name} ({url})")
    print(f"{'='*60}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        resp = requests.get(url, headers=headers, timeout=15, verify=False)
        
        if resp.status_code != 200:
            print(f"状态码: {resp.status_code}，跳过")
            return
        
        # 使用增强版解析器
        engine = CollectorEngine(task_id=0)
        result = {
            'status': 'unknown', 'status_detail': '', 'response_time': 0,
            'http_status': None, 'has_https': 0, 'has_search': 0,
            'has_download': 0, 'has_api': 0, 'has_register': 0,
            'has_preview': 0, 'has_visualization': 0, 'has_update_info': 0,
            'has_metadata': 0, 'has_feedback': 0, 'has_bulk_download': 0,
            'dataset_count': 0, 'app_count': 0, 'format_types': '[]',
            'raw_html': '', 'error_message': ''
        }
        
        engine._parse_page_content(result, resp.text)
        
        print(f"数据集数量: {result['dataset_count']}")
        print(f"应用数量: {result['app_count']}")
        print(f"格式类型: {result['format_types']}")
        print(f"搜索: {result['has_search']} | 下载: {result['has_download']} | API: {result['has_api']}")
        print(f"注册: {result['has_register']} | 预览: {result['has_preview']} | 可视化: {result['has_visualization']}")
        
    except Exception as e:
        print(f"错误: {str(e)[:100]}")

def main():
    platforms = [
        ("山东", "https://data.sd.gov.cn"),
        ("四川", "https://scdata.net.cn"),
        ("江苏", "https://data.jszwfw.gov.cn:8118/extranet/openportal/pages/default/index.html"),
        ("广东", "https://gddata.gd.gov.cn"),
        ("浙江", "https://data.zj.gov.cn"),
        ("贵州", "https://data.guizhou.gov.cn"),
        ("湖北", "https://data.hubei.gov.cn"),
    ]
    
    print("=" * 60)
    print("增强版解析器测试")
    print("=" * 60)
    
    for name, url in platforms:
        test_parser_on_platform(name, url)
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == '__main__':
    main()
