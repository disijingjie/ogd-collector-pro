import json
import re
from playwright.sync_api import sync_playwright

with open('v3_platform_rules.json', 'r', encoding='utf-8') as f:
    rules = json.load(f)

platforms = {p['code']: p for p in rules['platforms']}
results = []

# 所有15个平台
codes = ['beijing', 'guangdong', 'hainan', 'hubei', 'chongqing', 'guizhou', 'shandong', 
         'liaoning', 'neimenggu', 'jilin', 'jiangxi', 'fujian', 'guangxi', 'sichuan', 'hunan']

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    for code in codes:
        platform = platforms[code]
        name = platform['name']
        print(f'=== {name} ===')
        
        result = {
            'code': code, 'name': name, 'dataset_count': None,
            'confidence': 'low', 'status': 'pending', 'method': None
        }
        
        try:
            # 策略1: 访问首页
            page = browser.new_page()
            url = platform['urls']['homepage']
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(3000)
            text = page.inner_text('body')
            page.close()
            
            # 多模式匹配（按优先级）
            patterns = [
                (r'数据集\s*([0-9,]+)\s*个', '数据集', 'high'),
                (r'数据目录\s*([0-9,]+)\s*个', '数据目录', 'high'),
                (r'目录总数\s*（个）\s*([0-9,]+)', '目录总数', 'high'),
                (r'目录\s*([0-9,]+)\s*个', '目录', 'medium'),
                (r'开放目录\s*([0-9,]+)\s*个', '开放目录', 'medium'),
                (r'数据资源\s*([0-9,]+)\s*个', '数据资源', 'medium'),
            ]
            
            found = False
            for pattern, label, conf in patterns:
                match = re.search(pattern, text)
                if match:
                    num = int(match.group(1).replace(',', ''))
                    # 过滤掉太小的数字（可能是部门数）
                    if num > 50 or label in ['数据集', '数据目录', '目录总数']:
                        print(f'  首页找到({label}): {num}')
                        result['dataset_count'] = num
                        result['confidence'] = conf
                        result['status'] = 'success'
                        result['method'] = f'homepage:{label}'
                        found = True
                        break
            
            # 策略2: 访问数据目录页
            if not found and platform['urls'].get('dataset_page'):
                page = browser.new_page()
                dp_url = platform['urls']['dataset_page']
                try:
                    page.goto(dp_url, wait_until='networkidle', timeout=30000)
                    page.wait_for_timeout(3000)
                    text = page.inner_text('body')
                    page.close()
                    
                    # 在目录页查找
                    for pattern, label, conf in patterns:
                        match = re.search(pattern, text)
                        if match:
                            num = int(match.group(1).replace(',', ''))
                            if num > 10:
                                print(f'  目录页找到({label}): {num}')
                                result['dataset_count'] = num
                                result['confidence'] = conf
                                result['status'] = 'success'
                                result['method'] = f'dataset_page:{label}'
                                found = True
                                break
                    
                    # 查找分页信息
                    if not found:
                        match = re.search(r'共\s*([0-9,]+)\s*条', text)
                        if match:
                            num = int(match.group(1).replace(',', ''))
                            print(f'  目录页找到(共X条): {num}')
                            result['dataset_count'] = num
                            result['confidence'] = 'high'
                            result['status'] = 'success'
                            result['method'] = 'dataset_page:共X条'
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

# 保存
with open('data/v3_collection_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print()
print('='*60)
success = sum(1 for r in results if r['status']=='success')
print(f'成功: {success}/{len(results)}')
for r in results:
    if r['status'] == 'success':
        print(f'  {r["name"]}: {r["dataset_count"]} ({r["method"]})')
print('='*60)
