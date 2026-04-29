"""
静态页面采集脚本
使用 Requests + BeautifulSoup 采集政府数据开放平台数据集数量
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import time
from datetime import datetime

# 平台列表
PLATFORMS = [
    {"code": "beijing", "name": "北京市", "url": "https://data.beijing.gov.cn/", "pattern": r"数据集\s*(\d+)"},
    {"code": "shandong", "name": "山东省", "url": "https://data.sd.gov.cn", "pattern": r"(\d+)\s*个数据目录"},
    {"code": "guangdong", "name": "广东省", "url": "https://gddata.gd.gov.cn", "pattern": r"数据集\s*(\d+)"},
    {"code": "hubei", "name": "湖北省", "url": "https://data.hubei.gov.cn", "pattern": r"(\d+)\s*条数据目录"},
    {"code": "chongqing", "name": "重庆市", "url": "https://data.dsjj.cq.gov.cn", "pattern": r"数据集\s*(\d+)"},
    # ... 更多平台
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def collect_platform(platform):
    """采集单个平台的数据集数量"""
    try:
        response = requests.get(platform['url'], headers=HEADERS, timeout=30)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 使用正则表达式提取数字
        text = soup.get_text()
        match = re.search(platform['pattern'], text)
        
        if match:
            count = int(match.group(1))
            return {
                'code': platform['code'],
                'name': platform['name'],
                'dataset_count': count,
                'status': 'success',
                'method': '静态解析',
                'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        else:
            return {
                'code': platform['code'],
                'name': platform['name'],
                'dataset_count': None,
                'status': 'not_found',
                'method': '静态解析',
                'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
    except Exception as e:
        return {
            'code': platform['code'],
            'name': platform['name'],
            'dataset_count': None,
            'status': 'error',
            'method': '静态解析',
            'error': str(e),
            'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def main():
    print("=" * 60)
    print("OGD-Collector Pro - 静态页面采集")
    print("=" * 60)
    
    results = []
    for platform in PLATFORMS:
        print(f"\n正在采集: {platform['name']} ...", end=" ")
        result = collect_platform(platform)
        results.append(result)
        
        if result['status'] == 'success':
            print(f"成功 | 数据集: {result['dataset_count']}")
        else:
            print(f"失败 | 状态: {result['status']}")
        
        time.sleep(2)  # 礼貌性延迟
    
    # 保存结果
    with open('collection_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"采集完成: {len([r for r in results if r['status'] == 'success'])}/{len(results)} 成功")
    print("结果已保存至 collection_results.json")
    print("=" * 60)

if __name__ == '__main__':
    main()
