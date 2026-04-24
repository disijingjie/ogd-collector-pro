#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度挖掘16个unavailable平台的真实地址
批量验证URL可用性
"""
import requests
import json
import time
import sys
import io
import os

# 强制UTF-8输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

from urllib.parse import urljoin

# 汇总所有待验证的省级平台URL
# 格式: (平台名, 当前系统中URL, 新发现的可能URL列表, 备注)
PLATFORMS = [
    # 1. 反爬拦截（2个）
    ("上海", "https://data.sh.gov.cn", ["https://data.sh.gov.cn"], "有WAF，测试Playwright"),
    ("江苏", "http://data.jiangsu.gov.cn", ["https://data.jszwfw.gov.cn:8118/extranet/openportal/pages/default/index.html"], "域名可能变更"),
    
    # 2. Timeout（3个）
    ("山西", "http://data.shanxi.gov.cn", ["https://data.shanxi.gov.cn", "http://data.shanxi.gov.cn"], "2023年上线，可能https问题"),
    ("青海", "http://data.qinghai.gov.cn", ["http://data.qinghai.gov.cn"], ""),
    ("黑龙江", "http://data.hlj.gov.cn", ["http://data.hlj.gov.cn", "http://116.182.12.53:8001/oportal/index"], "可能无独立省级平台"),
    
    # 3. 疑似整合/域名废弃（9个）
    ("河北", "http://data.hebei.gov.cn", ["https://hebopendata.hebei.gov.cn/", "http://data.hebei.gov.cn"], ""),
    ("河南", "http://data.henan.gov.cn", ["https://data.hnzwfw.gov.cn/", "http://data.henan.gov.cn"], ""),
    ("四川", "http://data.sc.gov.cn", ["https://scdata.net.cn/", "https://www.scdata.net.cn/", "http://data.sc.gov.cn"], "新域名scdata.net.cn"),
    ("陕西", "http://data.shaanxi.gov.cn", ["http://www.sndata.gov.cn/", "https://www.sndata.gov.cn/", "http://data.shaanxi.gov.cn"], "新域名sndata.gov.cn"),
    ("甘肃", "http://data.gansu.gov.cn", ["https://data.gansu.gov.cn/", "http://data.gansu.gov.cn"], ""),
    ("宁夏", "http://data.nx.gov.cn", ["https://nxdata.gov.cn/", "http://opendata.nx.gov.cn", "http://data.nx.gov.cn"], ""),
    ("新疆", "http://data.xinjiang.gov.cn", ["https://data.xinjiang.gov.cn/", "http://data.xinjiang.gov.cn"], ""),
    ("西藏", "http://data.xizang.gov.cn", ["https://data.xizang.gov.cn/", "http://data.xizang.gov.cn"], ""),
    
    # 4. 额外验证一些已确认的平台
    ("吉林", "http://data.jl.gov.cn", ["https://data.jl.gov.cn/", "http://data.jl.gov.cn"], "2022年文章说查不到，但2025年有了"),
    ("辽宁", "http://data.ln.gov.cn", ["https://data.ln.gov.cn/", "http://data.ln.gov.cn"], ""),
    ("海南", "http://data.hainan.gov.cn", ["https://data.hainan.gov.cn/", "http://data.hainan.gov.cn"], ""),
]

def test_url(url, timeout=15):
    """测试URL可用性"""
    result = {
        'url': url,
        'status_code': None,
        'is_available': False,
        'error': None,
        'title': None,
        'has_dataset_count': False,
        'redirect_url': None
    }
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True, verify=False)
        result['status_code'] = resp.status_code
        result['redirect_url'] = resp.url if resp.url != url else None
        
        if resp.status_code == 200:
            result['is_available'] = True
            # 提取标题
            import re
            title_match = re.search(r'<title[^>]*>(.*?)</title>', resp.text, re.IGNORECASE|re.DOTALL)
            if title_match:
                result['title'] = title_match.group(1).strip()[:80]
            # 检查是否有数据集数量
            if any(k in resp.text.lower() for k in ['数据集', 'dataset', 'data count', '目录']):
                result['has_dataset_count'] = True
        
    except requests.exceptions.Timeout:
        result['error'] = 'Timeout'
    except requests.exceptions.ConnectionError as e:
        result['error'] = f'ConnectionError: {str(e)[:50]}'
    except Exception as e:
        result['error'] = f'Error: {str(e)[:50]}'
    
    return result

def main():
    print("=" * 80)
    print("省级政府数据开放平台真实地址深度验证")
    print("=" * 80)
    
    all_results = []
    
    for name, old_url, new_urls, note in PLATFORMS:
        print(f"\n【{name}】")
        print(f"  系统中URL: {old_url}")
        if note:
            print(f"  备注: {note}")
        
        best_result = None
        for url in new_urls:
            print(f"  测试: {url}", end=" ", flush=True)
            result = test_url(url)
            
            if result['is_available']:
                print(f"[OK] 200 OK | 标题: {result['title'] or 'N/A'}")
                if result['redirect_url']:
                    print(f"      重定向到: {result['redirect_url']}")
                if not best_result:
                    best_result = result
            elif result['error']:
                print(f"[FAIL] {result['error']}")
            else:
                print(f"[FAIL] HTTP {result['status_code']}")
            
            time.sleep(0.5)
        
        if best_result:
            all_results.append({
                'name': name,
                'old_url': old_url,
                'new_url': best_result['url'],
                'status': 'available',
                'title': best_result['title'],
                'has_data_indicator': best_result['has_dataset_count']
            })
        else:
            all_results.append({
                'name': name,
                'old_url': old_url,
                'new_url': None,
                'status': 'unavailable',
                'title': None,
                'has_data_indicator': False
            })
    
    # 汇总报告
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("验证结果汇总")
    report_lines.append("=" * 80)
    
    available = [r for r in all_results if r['status'] == 'available']
    unavailable = [r for r in all_results if r['status'] == 'unavailable']
    
    report_lines.append(f"\n[OK] 可访问: {len(available)}/{len(all_results)}")
    for r in available:
        report_lines.append(f"  {r['name']}: {r['new_url']}")
        if r['title']:
            report_lines.append(f"    标题: {r['title']}")
    
    report_lines.append(f"\n[FAIL] 仍不可访问: {len(unavailable)}")
    for r in unavailable:
        report_lines.append(f"  {r['name']}: {r['old_url']}")
    
    # 输出JSON供后续处理
    report_lines.append("\n" + "=" * 80)
    report_lines.append("JSON格式更新建议")
    report_lines.append("=" * 80)
    updates = {}
    for r in available:
        if r['new_url'] and r['new_url'] != r['old_url']:
            updates[r['name']] = r['new_url']
    
    report_lines.append(json.dumps(updates, ensure_ascii=False, indent=2))
    
    report_text = "\n".join(report_lines)
    print(report_text)
    
    # 写入文件
    with open('_verify_platform_urls_result.txt', 'w', encoding='utf-8') as f:
        f.write(report_text)
    print("\n结果已保存到 _verify_platform_urls_result.txt")

if __name__ == '__main__':
    main()
