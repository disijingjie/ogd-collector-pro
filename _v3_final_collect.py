import json
import re
from playwright.sync_api import sync_playwright

# 加载规则
with open('v3_platform_rules.json', 'r', encoding='utf-8') as f:
    rules = json.load(f)

platforms = {p['code']: p for p in rules['platforms']}

# 基于第一轮分析已确认的正确值（手工验证过的）
confirmed_values = {
    'beijing': {'value': 4454, 'type': '数据集', 'source': 'homepage'},
    'chongqing': {'value': 22550, 'type': '数据集', 'source': 'homepage'},
    'fujian': {'value': 6722, 'type': '目录数', 'source': 'homepage'},
    'guangdong': {'value': 97528, 'type': '数据集', 'source': 'homepage'},
    'guangxi': {'value': 10162, 'type': '目录总数', 'source': 'dataset_page'},
    'guizhou': {'value': 9042, 'type': '数据集', 'source': 'homepage'},
    'hainan': {'value': 35835, 'type': '目录', 'source': 'homepage'},
    'hubei': {'value': 24119, 'type': '数据目录', 'source': 'homepage'},
    'hunan': {'value': 634, 'type': '目录', 'source': 'dataset_page'},
    'jiangxi': {'value': 534, 'type': '开放数据目录', 'source': 'homepage'},
    'jilin': {'value': 303, 'type': '开放目录', 'source': 'homepage'},
    'liaoning': {'value': 4120, 'type': '数据目录', 'source': 'homepage'},
    'neimenggu': {'value': 219, 'type': '数据目录', 'source': 'homepage'},
    'shandong': {'value': 63656, 'type': '数据目录', 'source': 'homepage'},
    'sichuan': {'value': 9115, 'type': '目录数量', 'source': 'dataset_page'},
}

results = []

# 需要深度采集的平台（未确认或需要验证的）
need_collect = ['tianjin', 'shanxi', 'shanghai', 'jiangsu', 'zhejiang', 'anhui', 'henan', 'yunnan']

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 1. 填充已确认值
    for code, data in confirmed_values.items():
        platform = platforms[code]
        results.append({
            'code': code,
            'name': platform['name'],
            'dataset_count': data['value'],
            'type': data['type'],
            'confidence': 'high',
            'status': 'success',
            'method': f"confirmed:{data['source']}",
            'source_url': platform['urls']['homepage'],
            'note': '基于第一轮深度分析确认的值'
        })
        print(f"[确认] {platform['name']}: {data['value']}")
    
    # 2. 深度采集未确认平台
    for code in need_collect:
        platform = platforms[code]
        name = platform['name']
        print(f"\n[采集] {name}")
        
        result = {
            'code': code, 'name': name, 'dataset_count': None,
            'type': None, 'confidence': 'low', 'status': 'pending',
            'method': None, 'source_url': None
        }
        
        try:
            page = browser.new_page()
            url = platform['urls']['homepage']
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(5000)  # 增加等待时间让JS渲染
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
                    if num > 20:  # 过滤小数字
                        print(f"  首页找到({label}): {num}")
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
                                print(f"  目录页找到({label}): {num}")
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
                            print(f"  目录页找到(共X条): {num}")
                            result['dataset_count'] = num
                            result['type'] = '条目'
                            result['confidence'] = 'high'
                            result['status'] = 'success'
                            result['method'] = 'dataset_page:共X条'
                            result['source_url'] = dp_url
                            found = True
                except Exception as e:
                    print(f"  目录页错误: {e}")
                    if page:
                        page.close()
            
            if not found:
                print(f"  未找到")
                result['status'] = 'not_found'
                
        except Exception as e:
            print(f"  错误: {e}")
            result['status'] = 'error'
            result['error'] = str(e)[:100]
        
        results.append(result)
    
    browser.close()

# 保存结果
with open('data/v3_collection_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# 输出报告
print()
print('='*70)
print('V3最终采集报告')
print('='*70)
success = sum(1 for r in results if r['status']=='success')
not_found = sum(1 for r in results if r['status']=='not_found')
errors = sum(1 for r in results if r['status']=='error')
print(f'总平台: {len(results)} | 成功: {success} | 未找到: {not_found} | 错误: {errors}')
print()
print('成功采集:')
for r in sorted(results, key=lambda x: x['dataset_count'] or 0, reverse=True):
    if r['status'] == 'success':
        conf_mark = '[H]' if r['confidence']=='high' else '[M]'
        print(f'  {conf_mark} {r["name"]:12s}: {r["dataset_count"]:8,d} | {r["type"]:10s} | {r["method"]}')
print()
if not_found > 0:
    print('未找到:')
    for r in results:
        if r['status'] == 'not_found':
            print(f'  [X] {r["name"]}')
if errors > 0:
    print('错误:')
    for r in results:
        if r['status'] == 'error':
            print(f'  [X] {r["name"]}: {r.get("error", "")}')
print('='*70)
