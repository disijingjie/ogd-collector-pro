"""
再次尝试采集剩余失败的5个平台（延长超时时间）
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sqlite3
import time
import json
from datetime import datetime
from pathlib import Path
from collector_engine import CollectorEngine
from models import get_db

# 仍然失败的5个平台（28样本中）
REMAINING = [
    ('heilongjiang', '黑龙江省', 'https://data.hlj.gov.cn'),
    ('shanghai', '上海市', 'https://data.sh.gov.cn'),
    ('hebei', '河北省', 'https://data.hebei.gov.cn'),
    ('shaanxi', '陕西省', 'https://data.shaanxi.gov.cn'),
    ('xinjiang', '新疆维吾尔自治区', 'https://data.xinjiang.gov.cn'),
]

def recollect_with_longer_timeout():
    print("=" * 80)
    print("再次尝试采集剩余失败平台（超时30秒）")
    print("采集时间:", datetime.now().isoformat())
    print("=" * 80)
    
    engine = CollectorEngine(task_id=None, max_workers=1, delay=5)
    engine.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    
    results = []
    for code, name, url in REMAINING:
        print("\n[%s] %s -> %s" % (code, name, url))
        
        # 尝试不同变体URL
        urls_to_try = [url]
        if code == 'shanghai':
            urls_to_try = ['https://data.sh.gov.cn', 'http://data.sh.gov.cn']
        elif code == 'hebei':
            urls_to_try = ['https://data.hebei.gov.cn', 'http://data.hebei.gov.cn']
        elif code == 'shaanxi':
            urls_to_try = ['https://data.shaanxi.gov.cn', 'http://data.shaanxi.gov.cn']
        elif code == 'xinjiang':
            urls_to_try = ['https://data.xinjiang.gov.cn', 'http://data.xinjiang.gov.cn']
        elif code == 'heilongjiang':
            urls_to_try = ['https://data.hlj.gov.cn', 'http://data.hlj.gov.cn']
        
        best_result = None
        for try_url in urls_to_try:
            try:
                import requests
                start = time.time()
                resp = requests.get(try_url, timeout=30, allow_redirects=True, verify=False,
                                    headers={'User-Agent': 'Mozilla/5.0'})
                elapsed = time.time() - start
                print("  尝试 %s -> HTTP %d, 耗时 %.2fs" % (try_url, resp.status_code, elapsed))
                
                if resp.status_code == 200:
                    best_result = {
                        'status': 'available',
                        'status_detail': '平台可访问(重试)',
                        'response_time': round(elapsed, 2),
                        'http_status': resp.status_code,
                        'url_used': try_url
                    }
                    break
                elif not best_result:
                    best_result = {
                        'status': 'unavailable',
                        'status_detail': 'HTTP状态码: %d' % resp.status_code,
                        'response_time': round(elapsed, 2),
                        'http_status': resp.status_code,
                        'url_used': try_url
                    }
            except Exception as e:
                print("  尝试 %s -> 失败: %s" % (try_url, str(e)[:60]))
                if not best_result:
                    best_result = {
                        'status': 'unavailable',
                        'status_detail': str(e)[:80],
                        'response_time': 0,
                        'http_status': None,
                        'url_used': try_url
                    }
        
        if not best_result:
            best_result = {'status': 'unavailable', 'status_detail': '所有URL尝试失败', 'response_time': 0, 'http_status': None}
        
        print("  最终状态: %s | %s" % (best_result['status'], best_result['status_detail']))
        results.append({
            'code': code, 'name': name, 'status': best_result['status'],
            'detail': best_result['status_detail'], 'response_time': best_result['response_time'],
            'http_status': best_result['http_status'], 'collected_at': datetime.now().isoformat()
        })
        time.sleep(3)
    
    # 保存验证报告
    report_path = Path('data') / ("recollection_remaining_%s.json" % datetime.now().strftime('%Y%m%d_%H%M%S'))
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            'collected_at': datetime.now().isoformat(),
            'total': len(REMAINING),
            'results': results
        }, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 80)
    success = sum(1 for r in results if r['status'] == 'available')
    print("重试完成: 成功 %d / %d" % (success, len(REMAINING)))
    print("报告已保存:", report_path)
    return results

if __name__ == '__main__':
    recollect_with_longer_timeout()
