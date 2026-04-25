"""
V3 最终突破 - 最后4个平台
河南(hndataops.com深度挖掘)、江苏(找正确URL)、安徽(缓存/历史)、云南(构造URL)
"""

import json
import re
from playwright.sync_api import sync_playwright
from datetime import datetime

# 加载已有结果
with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

results_dict = {r['code']: r for r in results}

def update_result(code, name, dataset_count, data_type, confidence, method, source_url, note):
    result = {
        'code': code, 'name': name, 'dataset_count': dataset_count, 'type': data_type,
        'confidence': confidence, 'status': 'success' if dataset_count else 'not_found',
        'method': method, 'source_url': source_url, 'note': note,
        'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    if code in results_dict:
        for i, r in enumerate(results):
            if r['code'] == code:
                results[i] = result
                break
    else:
        results.append(result)
    results_dict[code] = result
    return result

print("=" * 60)
print("【河南】hndataops.com 深度挖掘")
print("=" * 60)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    try:
        page = browser.new_page()
        # 先访问首页
        page.goto('https://hndataops.com/', wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(5000)
        
        title = page.title()
        text = page.inner_text('body')
        print(f"  标题: {title}")
        print(f"  文本长度: {len(text)}")
        
        # 查找任何数字
        matches = re.findall(r'(\d{3,})', text)
        print(f"  找到的数字: {matches[:10]}")
        
        # 尝试点击"产品中心"或"数据产品"
        try:
            print("  尝试点击'产品中心'...")
            page.click('text=产品中心')
            page.wait_for_timeout(5000)
            text2 = page.inner_text('body')
            print(f"  产品中心页面文本前500字: {text2[:500]}")
            matches2 = re.findall(r'(\d{3,})', text2)
            print(f"  产品中心页面数字: {matches2[:10]}")
        except Exception as e:
            print(f"  点击失败: {str(e)[:100]}")
        
        # 尝试访问数据产品列表页
        try:
            print("  尝试直接访问产品列表...")
            page.goto('https://hndataops.com/product', wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(5000)
            text3 = page.inner_text('body')
            print(f"  产品列表页文本前500字: {text3[:500]}")
            matches3 = re.findall(r'(\d{3,})', text3)
            print(f"  产品列表页数字: {matches3[:10]}")
        except Exception as e:
            print(f"  访问失败: {str(e)[:100]}")
        
        page.close()
    except Exception as e:
        print(f"  [FAIL] {str(e)[:100]}")
    browser.close()

print()
print("=" * 60)
print("【江苏】查找正确的数据目录页URL")
print("=" * 60)

jiangsu_urls = [
    'https://jszwb.jiangsu.gov.cn/',
    'https://data.jiangsu.gov.cn/',
    'http://data.jiangsu.gov.cn/',
    'https://www.jiangsu.gov.cn/art/2024/4/art_83566_11234567.html',
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for url in jiangsu_urls:
        try:
            print(f"  尝试: {url}")
            page = browser.new_page()
            page.goto(url, wait_until='domcontentloaded', timeout=15000)
            page.wait_for_timeout(3000)
            title = page.title()
            text = page.inner_text('body')[:300]
            print(f"    标题: {title}")
            print(f"    文本: {text[:200]}")
            
            # 查找数据集数量
            match = re.search(r'数据集\s*([0-9,]+)\s*个', text)
            if match:
                num = int(match.group(1).replace(',', ''))
                print(f"    [OK] 找到: {num}")
                update_result('jiangsu', '江苏省', num, '数据集', 'high',
                    f'homepage:{url}', url, '找到正确的访问地址')
                page.close()
                break
            page.close()
        except Exception as e:
            print(f"    [FAIL] {str(e)[:80]}")
            continue
    browser.close()

print()
print("=" * 60)
print("【安徽】尝试历史缓存/快照")
print("=" * 60)

# 尝试百度搜索缓存
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    try:
        page = browser.new_page()
        # 百度搜索安徽省数据开放平台
        search_url = 'https://www.baidu.com/s?wd=安徽省政务数据开放平台+数据集数量'
        print(f"  百度搜索: {search_url}")
        page.goto(search_url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(5000)
        
        text = page.inner_text('body')
        print(f"  搜索结果前500字: {text[:500]}")
        
        # 查找数字
        matches = re.findall(r'(\d{3,})', text)
        print(f"  找到的数字: {matches[:10]}")
        
        page.close()
    except Exception as e:
        print(f"  [FAIL] {str(e)[:100]}")
    browser.close()

print()
print("=" * 60)
print("【云南】构造数据目录页URL直接访问")
print("=" * 60)

yunnan_urls = [
    'https://data.yn.gov.cn/catalog',
    'https://data.yn.gov.cn/dataset',
    'https://data.yn.gov.cn/open-data',
    'https://data.yn.gov.cn/#/catalog',
    'https://data.yn.gov.cn/#/dataset',
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for url in yunnan_urls:
        try:
            print(f"  尝试: {url}")
            page = browser.new_page()
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(5000)
            
            title = page.title()
            text = page.inner_text('body')
            print(f"    标题: {title}")
            print(f"    文本长度: {len(text)}")
            print(f"    文本前300字: {text[:300]}")
            
            # 查找数据集数量
            match = re.search(r'数据集\s*([0-9,]+)\s*个', text)
            if match:
                num = int(match.group(1).replace(',', ''))
                print(f"    [OK] 找到: {num}")
                update_result('yunnan', '云南省', num, '数据集', 'high',
                    f'dataset_page:{url}', url, '通过构造URL访问数据目录页成功')
                page.close()
                break
            else:
                match = re.search(r'共\s*([0-9,]+)\s*条', text)
                if match:
                    num = int(match.group(1).replace(',', ''))
                    print(f"    [OK] 找到: {num}")
                    update_result('yunnan', '云南省', num, '数据目录', 'high',
                        f'dataset_page:{url}', url, '通过构造URL访问数据目录页成功')
                    page.close()
                    break
            page.close()
        except Exception as e:
            print(f"    [FAIL] {str(e)[:80]}")
            continue
    browser.close()

print()
print("=" * 60)
print("【保存结果】")
print("=" * 60)

with open('data/v3_collection_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

success_count = sum(1 for r in results if r['status'] == 'success')
print(f"\n总计成功: {success_count}/23个平台")

print("\n所有成功平台（按数量排序）:")
for r in sorted(results, key=lambda x: x['dataset_count'] or 0, reverse=True):
    if r['status'] == 'success':
        source_mark = '[自主]' if 'confirmed' in r.get('method', '') or 'homepage' in r.get('method', '') or 'dataset_page' in r.get('method', '') or 'api' in r.get('method', '') else '[第三方]'
        print(f"  {source_mark} {r['name']:12s}: {r['dataset_count']:8,} | {r.get('type', ''):10s} | {r.get('method', '')}")

print("\n待确认平台:")
for r in results:
    if r['status'] != 'success':
        print(f"  [X] {r['name']:12s}: {r.get('note', '')}")
