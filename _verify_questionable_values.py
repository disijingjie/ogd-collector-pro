"""
验证有疑问的平台数据集数量值
重点验证：福建4851、四川3465、广西10037（是否有"次"后缀）
同时重新验证重庆22550和辽宁4120的上下文
"""
import json
import re
from playwright.sync_api import sync_playwright
from pathlib import Path

def verify_platform(browser, url, name, code):
    result = {'code': code, 'name': name, 'url': url, 'verified_count': None, 'context': None, 'status': 'pending'}
    
    context = None
    try:
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080},
            ignore_https_errors=True,
        )
        page = context.new_page()
        page.goto(url, timeout=30000, wait_until='domcontentloaded')
        page.wait_for_timeout(5000)
        
        text = page.inner_text('body')
        html = page.content()
        result['status'] = 'success'
        
        # 搜索页面中所有包含数字+"数据集"/"目录"/"资源"的模式
        patterns = [
            r'(\d[\d,\s]*)\s*个数据集',
            r'(\d[\d,\s]*)\s*条数据',
            r'(\d[\d,\s]*)\s*个目录',
            r'(\d[\d,\s]*)\s*个资源',
            r'数据集[:：]?\s*(\d[\d,\s]*)',
            r'目录[:：]?\s*(\d[\d,\s]*)',
            r'资源[:：]?\s*(\d[\d,\s]*)',
            r'(?:共|累计|已|现有|开放)\s*(\d[\d,\s]*)\s*个',
        ]
        
        all_matches = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                num_str = m.replace(',', '').replace(' ', '')
                try:
                    val = int(num_str)
                    if 5 <= val <= 5000000:
                        idx = text.find(m)
                        ctx = text[max(0, idx-50):idx+len(m)+50].replace('\n', ' ')
                        all_matches.append({'value': val, 'context': ctx})
                except:
                    pass
        
        # 也搜索"X次"模式（可能是访问次数）
        count_patterns = []
        count_matches = re.findall(r'(\d[\d,\s]*)\s*次', text, re.IGNORECASE)
        for m in count_matches:
            num_str = m.replace(',', '').replace(' ', '')
            try:
                val = int(num_str)
                if 5 <= val <= 5000000:
                    idx = text.find(m)
                    ctx = text[max(0, idx-50):idx+len(m)+50].replace('\n', ' ')
                    count_patterns.append({'value': val, 'context': ctx})
            except:
                pass
        
        result['all_matches'] = all_matches
        result['count_patterns'] = count_patterns
        
        # 选取最可能的值：优先选择上下文中明确包含"数据集""目录""资源"的
        best = None
        for match in all_matches:
            ctx_lower = match['context'].lower()
            if any(k in ctx_lower for k in ['数据集', '数据目录', '目录', '资源', 'dataset', 'catalog']):
                if not best or match['value'] > best['value']:
                    best = match
        
        if best:
            result['verified_count'] = best['value']
            result['context'] = best['context']
        elif all_matches:
            # 如果没有明确的上下文，取最大值（通常数据集数比部门数大）
            best = max(all_matches, key=lambda x: x['value'])
            result['verified_count'] = best['value']
            result['context'] = best['context']
            result['note'] = 'uncertain_context'
        
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)[:200]
    finally:
        if context:
            context.close()
    
    return result


def main():
    platforms = [
        ('fujian', '福建省', 'https://data.fujian.gov.cn'),
        ('sichuan', '四川省', 'https://scdata.net.cn'),
        ('guangxi', '广西壮族自治区', 'https://data.gxzf.gov.cn'),
        ('chongqing', '重庆市', 'https://data.cq.gov.cn'),
        ('liaoning', '辽宁省', 'https://data.ln.gov.cn'),
    ]
    
    print('验证5个有疑问的平台')
    print()
    
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        for code, name, url in platforms:
            print('验证: %s ...' % name, end=' ')
            result = verify_platform(browser, url, name, code)
            results.append(result)
            
            if result['status'] == 'success':
                if result.get('verified_count'):
                    note = result.get('note', '')
                    print('OK -> dc=%d %s' % (result['verified_count'], note))
                    print('  context: %s' % result['context'][:100])
                else:
                    print('NO DATA')
            else:
                print('ERROR: %s' % result.get('error', 'unknown'))
            
            # 打印所有匹配到的候选值
            if result.get('all_matches'):
                print('  all dataset matches:')
                for m in result['all_matches'][:5]:
                    print('    %d | %s' % (m['value'], m['context'][:70]))
            if result.get('count_patterns'):
                print('  count patterns (可能为访问次数):')
                for m in result['count_patterns'][:3]:
                    print('    %d | %s' % (m['value'], m['context'][:70]))
            print()
        
        browser.close()
    
    # 保存
    with open('data/verification_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print('结果保存到 data/verification_results.json')

if __name__ == '__main__':
    main()
