"""
最终版高精度采集脚本
为每个平台使用独立browser context
精确提取数据集数量，并保存完整上下文作为证据
"""
import sqlite3
import json
import re
from playwright.sync_api import sync_playwright
from pathlib import Path
from urllib.parse import urljoin

DB_PATH = Path('data/ogd_database.db')

def get_platforms():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("SELECT code, name, url FROM platforms WHERE tier='省级' ORDER BY code")
    rows = cursor.fetchall()
    conn.close()
    return rows

def find_dataset_count(page, current_url):
    """在页面上精确查找数据集数量，返回最佳匹配和完整上下文"""
    text = page.inner_text('body')
    html = page.content()
    
    candidates = []
    
    # 模式1: 高置信度 - 明确提到数据集/目录/资源+数字
    patterns = [
        (r'(?:共|累计|已|现有|开放|共计|合计)\s*(\d[\d,\s]*)\s*个数据集', 'X个数据集'),
        (r'(?:共|累计|已|现有|开放|共计|合计)\s*(\d[\d,\s]*)\s*条数据', 'X条数据'),
        (r'(?:共|累计|已|现有|开放|共计|合计)\s*(\d[\d,\s]*)\s*个目录', 'X个目录'),
        (r'(?:共|累计|已|现有|开放|共计|合计)\s*(\d[\d,\s]*)\s*个资源', 'X个资源'),
        (r'(?:共|累计|已|现有|开放|共计|合计)\s*(\d[\d,\s]*)\s*条记录', 'X条记录'),
        (r'数据集[:：]?\s*(\d[\d,\s]*)', '数据集:'),
        (r'数据目录[:：]?\s*(\d[\d,\s]*)', '数据目录:'),
        (r'开放目录[:：]?\s*(\d[\d,\s]*)', '开放目录:'),
        (r'资源目录[:：]?\s*(\d[\d,\s]*)', '资源目录:'),
        (r'(?:已|现有)?开放\s*(\d[\d,\s]*)\s*个(?:数据)?(?:目录)?', '开放X个'),
    ]
    
    for pattern, label in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            num_str = m.replace(',', '').replace(' ', '')
            try:
                val = int(num_str)
                if 5 <= val <= 5000000:
                    idx = text.find(m)
                    ctx = text[max(0, idx-60):idx+len(m)+60].replace('\n', ' ').replace('\r', ' ')
                    # 排除"部门"上下文
                    if '部门' in ctx and '数据集' not in ctx and '目录' not in ctx and '资源' not in ctx:
                        continue
                    candidates.append({'value': val, 'context': ctx, 'confidence': 'high', 'pattern': label})
            except:
                pass
    
    # 模式2: 搜索CSS计数器元素
    selectors = [
        '.count-num', '.data-count', '.catalog-count', '.dataset-count',
        '.statistics-num', '.total-num', '.num',
        '[class*="count"]', '[class*="num"]', '[class*="total"]',
        '[class*="data"]', '[class*="catalog"]',
    ]
    for sel in selectors:
        try:
            elems = page.query_selector_all(sel)
            for elem in elems[:5]:
                txt = elem.inner_text().strip()
                num_match = re.search(r'(\d[\d,\s]*)', txt)
                if num_match:
                    num_str = num_match.group(1).replace(',', '').replace(' ', '')
                    val = int(num_str)
                    if 5 <= val <= 5000000:
                        # 获取父元素文本以判断上下文
                        parent_txt = ''
                        try:
                            parent = elem.evaluate('el => el.parentElement ? el.parentElement.innerText : ""')
                            if parent:
                                parent_txt = parent
                        except:
                            pass
                        full_ctx = (parent_txt + ' | ' + txt)[:150]
                        # 排除"次"（访问次数）
                        if '次' in txt and '数据集' not in full_ctx and '目录' not in full_ctx:
                            continue
                        candidates.append({'value': val, 'context': full_ctx, 'confidence': 'medium', 'pattern': 'css:%s' % sel})
        except:
            pass
    
    # 模式3: 搜索script中的变量
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
    for script in scripts:
        js_patterns = [
            r'(datasetCount|catalogCount|dataCount|totalCount|resourceCount)\s*[:=]\s*["\']?(\d[\d,]*)["\']?',
        ]
        for pattern in js_patterns:
            matches = re.findall(pattern, script, re.IGNORECASE)
            for m in matches:
                num_str = m[1].replace(',', '')
                try:
                    val = int(num_str)
                    if 5 <= val <= 5000000:
                        candidates.append({'value': val, 'context': '%s=%s' % (m[0], num_str), 'confidence': 'high', 'pattern': 'js:%s' % m[0]})
                except:
                    pass
    
    # 选取最佳候选：优先高置信度，然后取最大值
    if candidates:
        high_conf = [c for c in candidates if c['confidence'] == 'high']
        if high_conf:
            best = max(high_conf, key=lambda x: x['value'])
        else:
            best = max(candidates, key=lambda x: x['value'])
        return best, candidates
    
    return None, []


def collect_platform(browser, code, name, base_url):
    result = {
        'code': code, 'name': name, 'base_url': base_url,
        'dataset_count': None, 'source_url': None, 'context': None,
        'confidence': None, 'all_candidates': [], 'status': 'pending', 'error': None
    }
    
    # 要尝试的URL
    urls = [base_url]
    alt_paths = [
        '/oportal/catalog/', '/catalog/', '/dataset/',
        '/portal/catalog/', '/openportal/pages/catalog/',
        '/business/catalog/list.do',
    ]
    for path in alt_paths:
        urls.append(urljoin(base_url, path))
    
    context = None
    try:
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            ignore_https_errors=True,
        )
        page = context.new_page()
        
        for url in urls:
            try:
                page.goto(url, timeout=25000, wait_until='domcontentloaded')
                page.wait_for_timeout(4000)
                current_url = page.url
                
                best, candidates = find_dataset_count(page, current_url)
                if best:
                    result['dataset_count'] = best['value']
                    result['source_url'] = current_url
                    result['context'] = best['context']
                    result['confidence'] = best['confidence']
                    result['all_candidates'] = candidates
                    result['status'] = 'success'
                    return result
            except Exception:
                continue
        
        result['status'] = 'not_found'
        
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)[:200]
    finally:
        if context:
            context.close()
    
    return result


def main():
    platforms = get_platforms()
    print('最终版高精度采集: %d 个省级平台' % len(platforms))
    print()
    
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        for code, name, url in platforms:
            print('采集: %-8s (%s) ...' % (name, url), end=' ')
            result = collect_platform(browser, code, name, url)
            results.append(result)
            
            if result['status'] == 'success':
                print('OK -> dc=%d [%s]' % (result['dataset_count'], result['confidence']))
                print('  context: %s' % result['context'][:100])
            elif result['status'] == 'not_found':
                print('NOT FOUND')
            else:
                print('ERROR: %s' % result.get('error', 'unknown')[:50])
        
        browser.close()
    
    # 保存
    with open('data/final_precise_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print()
    print('=' * 80)
    print('最终采集完成')
    print('=' * 80)
    
    found = sum(1 for r in results if r['status'] == 'success')
    not_found = sum(1 for r in results if r['status'] == 'not_found')
    errors = sum(1 for r in results if r['status'] == 'error')
    print('成功: %d | 未找到: %d | 错误: %d' % (found, not_found, errors))
    
    print()
    print('成功结果:')
    for r in results:
        if r['status'] == 'success':
            print('  %-10s: %d | %s | %s' % (r['name'], r['dataset_count'], r['confidence'], r['context'][:70]))

if __name__ == '__main__':
    main()
