"""
V3 最终最终突破 - 基于用户提供的URL逐个采集
江苏、河南、云南、安徽（确认维护状态）
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
print("【江苏】访问新URL: data.jszwfw.gov.cn:8118")
print("=" * 60)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    try:
        page = browser.new_page()
        url = 'https://data.jszwfw.gov.cn:8118/extranet/openportal/pages/default/index.html'
        page.goto(url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(5000)
        
        title = page.title()
        text = page.inner_text('body')
        print(f"  标题: {title}")
        print(f"  文本长度: {len(text)}")
        print(f"  文本前800字: {text[:800]}")
        
        # 查找所有数字
        matches = re.findall(r'(\d{3,})', text)
        print(f"  找到的数字: {matches[:15]}")
        
        # 查找数据集数量
        match = re.search(r'数据集\s*([0-9,]+)\s*个', text)
        if match:
            num = int(match.group(1).replace(',', ''))
            print(f"  [OK] 找到数据集数量: {num}")
            update_result('jiangsu', '江苏省', num, '数据集', 'high',
                'homepage:新URL访问', url, '通过新URL成功访问')
        else:
            match = re.search(r'数据目录\s*([0-9,]+)\s*个', text)
            if match:
                num = int(match.group(1).replace(',', ''))
                print(f"  [OK] 找到数据目录数量: {num}")
                update_result('jiangsu', '江苏省', num, '数据目录', 'high',
                    'homepage:新URL访问', url, '通过新URL成功访问')
            else:
                print("  [WARN] 未找到数据集/目录数量")
                update_result('jiangsu', '江苏省', None, '未知', 'low',
                    'pending:新URL无数据', url, '平台显示数据目录总量0个，可能维护中')
        
        page.close()
    except Exception as e:
        print(f"  [FAIL] {str(e)[:100]}")
        update_result('jiangsu', '江苏省', None, '未知', 'low',
            'pending:访问失败', url, str(e)[:100])
    browser.close()

print()
print("=" * 60)
print("【河南】访问产品中心: hndataops.com/portal/product")
print("=" * 60)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    try:
        page = browser.new_page()
        url = 'https://hndataops.com/portal/product'
        page.goto(url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(5000)
        
        title = page.title()
        text = page.inner_text('body')
        print(f"  标题: {title}")
        print(f"  文本长度: {len(text)}")
        print(f"  文本前800字: {text[:800]}")
        
        # 查找所有数字
        matches = re.findall(r'(\d{3,})', text)
        print(f"  找到的数字: {matches[:15]}")
        
        # 查找产品数量
        match = re.search(r'(\d+)\s*个产品', text)
        if match:
            num = int(match.group(1))
            print(f"  [OK] 找到产品数量: {num}")
            update_result('henan', '河南省', num, '数据产品', 'medium',
                'dataset_page:产品中心', url, '平台转型为运营服务平台，统计的是数据产品数量')
        else:
            match = re.search(r'共\s*([0-9,]+)\s*条', text)
            if match:
                num = int(match.group(1).replace(',', ''))
                print(f"  [OK] 找到总条数: {num}")
                update_result('henan', '河南省', num, '数据产品', 'medium',
                    'dataset_page:产品中心', url, '平台转型为运营服务平台')
            else:
                print("  [WARN] 未找到产品数量")
                update_result('henan', '河南省', None, '未知', 'low',
                    'pending:产品中心无总数', url, '平台转型，未显示产品总数')
        
        page.close()
    except Exception as e:
        print(f"  [FAIL] {str(e)[:100]}")
        update_result('henan', '河南省', None, '未知', 'low',
            'pending:访问失败', url, str(e)[:100])
    browser.close()

print()
print("=" * 60)
print("【云南】访问登记中心: data.yn.gov.cn/sjdj/#/registrationCenter")
print("=" * 60)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    try:
        page = browser.new_page()
        url = 'https://data.yn.gov.cn/sjdj/#/registrationCenter'
        page.goto(url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(5000)
        
        title = page.title()
        text = page.inner_text('body')
        print(f"  标题: {title}")
        print(f"  文本长度: {len(text)}")
        print(f"  文本前800字: {text[:800]}")
        
        # 查找所有数字
        matches = re.findall(r'(\d{3,})', text)
        print(f"  找到的数字: {matches[:15]}")
        
        # 查找登记数量
        match = re.search(r'([0-9,]+)\s*条登记', text)
        if match:
            num = int(match.group(1).replace(',', ''))
            print(f"  [OK] 找到登记数量: {num}")
            update_result('yunnan', '云南省', num, '数据登记', 'medium',
                'dataset_page:登记中心', url, '平台转型为登记平台，统计的是数据登记数量')
        else:
            match = re.search(r'共\s*([0-9,]+)\s*条', text)
            if match:
                num = int(match.group(1).replace(',', ''))
                print(f"  [OK] 找到总条数: {num}")
                update_result('yunnan', '云南省', num, '数据登记', 'medium',
                    'dataset_page:登记中心', url, '平台转型为登记平台')
            else:
                print("  [WARN] 未找到登记数量")
                update_result('yunnan', '云南省', None, '未知', 'low',
                    'pending:登记中心无总数', url, '平台转型，未显示登记总数')
        
        page.close()
    except Exception as e:
        print(f"  [FAIL] {str(e)[:100]}")
        update_result('yunnan', '云南省', None, '未知', 'low',
            'pending:访问失败', url, str(e)[:100])
    browser.close()

print()
print("=" * 60)
print("【安徽】确认维护状态")
print("=" * 60)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    try:
        page = browser.new_page()
        url = 'https://data.ahzwfw.gov.cn/'
        page.goto(url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(5000)
        
        title = page.title()
        text = page.inner_text('body')
        print(f"  标题: {title}")
        print(f"  文本: {text[:200]}")
        
        if '维护' in text or '维护' in title:
            print("  [CONFIRMED] 平台确实在维护中")
            update_result('anhui', '安徽省', None, '未知', 'low',
                'pending:平台维护中', url, '平台显示系统维护中，暂无法获取数据')
        else:
            print("  [INFO] 平台似乎已恢复")
            # 尝试查找数据
            match = re.search(r'数据集\s*([0-9,]+)\s*个', text)
            if match:
                num = int(match.group(1).replace(',', ''))
                print(f"  [OK] 找到数据集数量: {num}")
                update_result('anhui', '安徽省', num, '数据集', 'high',
                    'homepage:平台恢复', url, '平台已恢复，成功获取数据')
            else:
                update_result('anhui', '安徽省', None, '未知', 'low',
                    'pending:未找到数据', url, '平台可访问但未找到数据集数量')
        
        page.close()
    except Exception as e:
        print(f"  [FAIL] {str(e)[:100]}")
        update_result('anhui', '安徽省', None, '未知', 'low',
            'pending:访问失败', url, str(e)[:100])
    browser.close()

print()
print("=" * 60)
print("【保存结果】")
print("=" * 60)

with open('data/v3_collection_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

success_count = sum(1 for r in results if r['status'] == 'success')
not_found = sum(1 for r in results if r['status'] == 'not_found')
print(f"\n总计成功: {success_count}/23个平台")
print(f"待确认: {not_found}/23个平台")

print("\n所有成功平台（按数量排序）:")
for r in sorted(results, key=lambda x: x['dataset_count'] or 0, reverse=True):
    if r['status'] == 'success':
        source_mark = '[自主]' if 'confirmed' in r.get('method', '') or 'homepage' in r.get('method', '') or 'dataset_page' in r.get('method', '') or 'api' in r.get('method', '') else '[第三方]'
        print(f"  {source_mark} {r['name']:12s}: {r['dataset_count']:8,} | {r.get('type', ''):10s} | {r.get('method', '')}")

print("\n待确认平台:")
for r in results:
    if r['status'] != 'success':
        print(f"  [X] {r['name']:12s}: {r.get('note', '')}")
