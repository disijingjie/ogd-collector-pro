import json
import re
from playwright.sync_api import sync_playwright
from datetime import datetime

# 加载规则
with open('v3_platform_rules.json', 'r', encoding='utf-8') as f:
    rules = json.load(f)

platforms = {p['code']: p for p in rules['platforms']}
results = []

# 高优先级平台（已确认有数据的）
priority_codes = ['beijing', 'guangdong', 'hainan', 'hubei', 'chongqing', 'guizhou', 'shandong', 'liaoning', 'neimenggu', 'jilin', 'jiangxi', 'fujian', 'guangxi', 'sichuan', 'hunan']

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    for code in priority_codes:
        platform = platforms[code]
        name = platform['name']
        print(f'=== {name} ===')
        
        try:
            page = browser.new_page()
            url = platform['urls']['homepage']
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(3000)
            text = page.inner_text('body')
            
            found = False
            
            # 策略1: 匹配'数据集X个'
            match = re.search(r'数据集\s*([0-9,]+)\s*个', text)
            if match:
                num = int(match.group(1).replace(',', ''))
                print(f'  找到(数据集): {num}')
                results.append({'code': code, 'name': name, 'dataset_count': num, 'confidence': 'high', 'status': 'success', 'method': 'regex:数据集'})
                found = True
            
            # 策略2: 匹配'数据目录X个'
            if not found:
                match = re.search(r'数据目录\s*([0-9,]+)\s*个', text)
                if match:
                    num = int(match.group(1).replace(',', ''))
                    print(f'  找到(数据目录): {num}')
                    results.append({'code': code, 'name': name, 'dataset_count': num, 'confidence': 'high', 'status': 'success', 'method': 'regex:数据目录'})
                    found = True
            
            # 策略3: 匹配'目录X个'
            if not found:
                match = re.search(r'目录\s*([0-9,]+)\s*个', text)
                if match:
                    num = int(match.group(1).replace(',', ''))
                    print(f'  找到(目录): {num}')
                    results.append({'code': code, 'name': name, 'dataset_count': num, 'confidence': 'medium', 'status': 'success', 'method': 'regex:目录'})
                    found = True
            
            # 策略4: 匹配'开放X个部门'中的数字（避免）
            if not found:
                match = re.search(r'现已开放\s*([0-9,]+)\s*个部门', text)
                if match:
                    print(f'  跳过(部门数): {match.group(1)}')
                    results.append({'code': code, 'name': name, 'dataset_count': None, 'confidence': 'low', 'status': 'not_found', 'note': '只找到部门数'})
                else:
                    print(f'  未找到')
                    results.append({'code': code, 'name': name, 'dataset_count': None, 'confidence': 'low', 'status': 'not_found'})
            
            page.close()
        except Exception as e:
            print(f'  错误: {e}')
            results.append({'code': code, 'name': name, 'dataset_count': None, 'confidence': 'low', 'status': 'error', 'error': str(e)[:100]})
    
    browser.close()

# 保存结果
with open('data/v3_collection_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print()
print('='*60)
print(f'成功: {sum(1 for r in results if r["status"]=="success")}/{len(results)}')
for r in results:
    if r['status'] == 'success':
        print(f'  {r["name"]}: {r["dataset_count"]} ({r["method"]})')
print('='*60)
