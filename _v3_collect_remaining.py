import json
import re
from playwright.sync_api import sync_playwright

with open('v3_platform_rules.json', 'r', encoding='utf-8') as f:
    rules = json.load(f)

platforms = {p['code']: p for p in rules['platforms']}

# 剩余8个需要采集的平台
remaining_codes = ['tianjin', 'shanxi', 'shanghai', 'jiangsu', 'zhejiang', 'anhui', 'henan', 'yunnan']

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    for code in remaining_codes:
        platform = platforms[code]
        name = platform['name']
        print(f'=== {name} ===')
        
        result = {
            'code': code, 'name': name, 'dataset_count': None,
            'type': None, 'confidence': 'low', 'status': 'pending',
            'method': None, 'source_url': None
        }
        
        try:
            page = browser.new_page()
            url = platform['urls']['homepage']
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(5000)
            text = page.inner_text('body')
            page.close()
            
            # 多模式匹配
            patterns = [
                (r'数据集\s*([0-9,]+)\s*个', '数据集'),
                (r'数据目录\s*([0-9,]+)\s*个', '数据目录'),
                (r'目录总数\s*[（(]个[)）]\s*([0-9,]+)', '目录总数'),
                (r'开放数据目录\s*([0-9,]+)\s*个', '开放数据目录'),
                (r'开放目录\s*([0-9,]+)\s*个', '开放目录'),
                (r'目录\s*([0-9,]+)\s*个', '目录'),
                (r'数据资源\s*([0-9,]+)\s*个', '数据资源'),
                (r'资源\s*([0-9,]+)\s*个', '资源'),
            ]
            
            found = False
            for pattern, label in patterns:
                match = re.search(pattern, text)
                if match:
                    num = int(match.group(1).replace(',', ''))
                    if num > 20:
                        print(f'  首页找到({label}): {num}')
                        result['dataset_count'] = num
                        result['type'] = label
                        result['confidence'] = 'medium'
                        result['status'] = 'success'
                        result['method'] = f'homepage:{label}'
                        result['source_url'] = url
                        found = True
                        break
            
            # 访问数据目录页
            if not found and platform['urls'].get('dataset_page'):
                page = browser.new_page()
                dp_url = platform['urls']['dataset_page']
                try:
                    page.goto(dp_url, wait_until='networkidle', timeout=30000)
                    page.wait_for_timeout(5000)
                    text = page.inner_text('body')
                    page.close()
                    
                    for pattern, label in patterns:
                        match = re.search(pattern, text)
                        if match:
                            num = int(match.group(1).replace(',', ''))
                            if num > 10:
                                print(f'  目录页找到({label}): {num}')
                                result['dataset_count'] = num
                                result['type'] = label
                                result['confidence'] = 'medium'
                                result['status'] = 'success'
                                result['method'] = f'dataset_page:{label}'
                                result['source_url'] = dp_url
                                found = True
                                break
                    
                    # 分页信息
                    if not found:
                        match = re.search(r'共\s*([0-9,]+)\s*条', text)
                        if match:
                            num = int(match.group(1).replace(',', ''))
                            print(f'  目录页找到(共X条): {num}')
                            result['dataset_count'] = num
                            result['type'] = '条目'
                            result['confidence'] = 'high'
                            result['status'] = 'success'
                            result['method'] = 'dataset_page:共X条'
                            result['source_url'] = dp_url
                            found = True
                except Exception as e:
                    print(f'  目录页错误: {e}')
                    if page:
                        page.close()
            
            if not found:
                print(f'  未找到')
                result['status'] = 'not_found'
                
        except Exception as e:
            print(f'  错误: {e}')
            result['status'] = 'error'
            result['error'] = str(e)[:100]
        
        results.append(result)
    
    browser.close()

# 加载已有结果并合并
with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
    existing = json.load(f)

existing_codes = {r['code'] for r in existing}
for r in results:
    if r['code'] not in existing_codes:
        existing.append(r)
    else:
        # 更新已有记录
        for i, e in enumerate(existing):
            if e['code'] == r['code']:
                existing[i] = r
                break

with open('data/v3_collection_results.json', 'w', encoding='utf-8') as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print()
print('='*60)
success = sum(1 for r in results if r['status']=='success')
not_found = sum(1 for r in results if r['status']=='not_found')
errors = sum(1 for r in results if r['status']=='error')
print(f'本次采集: 成功{success} | 未找到{not_found} | 错误{errors}')
print()
if success > 0:
    print('成功:')
    for r in results:
        if r['status'] == 'success':
            print(f'  {r["name"]}: {r["dataset_count"]} ({r["type"]})')
print('='*60)

# 总统计
total_success = sum(1 for r in existing if r['status']=='success')
print(f'\n总计已采集: {total_success}/23个平台')
