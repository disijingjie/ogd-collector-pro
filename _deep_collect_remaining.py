"""
深度采集：针对NO DATA FOUND和URL失效的平台
逐个访问数据目录页，提取数据集数量
同时修正重庆和辽宁的值
"""
import sqlite3
import json
import re
from playwright.sync_api import sync_playwright
from pathlib import Path
from urllib.parse import urljoin

DB_PATH = Path('data/ogd_database.db')

def get_platform_url(code):
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM platforms WHERE code=?", (code,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def collect_dataset_count(browser, platform_info):
    """
    platform_info: dict with keys: code, name, url, dataset_page_url, notes
    """
    code = platform_info['code']
    name = platform_info['name']
    base_url = platform_info['url']
    dataset_page = platform_info.get('dataset_page_url')
    
    result = {
        'code': code, 'name': name, 'base_url': base_url,
        'dataset_count': None, 'source_url': None, 'source_text': None,
        'method': None, 'status': 'pending', 'error': None
    }
    
    # 要尝试的URL列表
    urls_to_try = []
    if dataset_page:
        urls_to_try.append(dataset_page)
    urls_to_try.append(base_url)
    
    # 一些平台可能有标准的数据目录路径
    alt_paths = [
        '/oportal/catalog/', '/catalog/', '/dataset/',
        '/business/catalog/list.do', '/portal/catalog/',
        '/openportal/pages/catalog/', '/data/catalog/',
    ]
    for path in alt_paths:
        alt = urljoin(base_url, path)
        if alt not in urls_to_try:
            urls_to_try.append(alt)
    
    context = None
    try:
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080},
            ignore_https_errors=True,
        )
        page = context.new_page()
        
        for try_url in urls_to_try:
            try:
                page.goto(try_url, timeout=25000, wait_until='domcontentloaded')
                page.wait_for_timeout(4000)
                
                text = page.inner_text('body')
                html = page.content()
                current_url = page.url
                
                # 策略1: 搜索明确提到"数据集""数据目录""资源"的数字
                high_conf_patterns = [
                    (r'数据集[:：]?\s*(\d[\d,\s]*)', '数据集:'),
                    (r'数据目录[:：]?\s*(\d[\d,\s]*)', '数据目录:'),
                    (r'开放目录[:：]?\s*(\d[\d,\s]*)', '开放目录:'),
                    (r'资源目录[:：]?\s*(\d[\d,\s]*)', '资源目录:'),
                    (r'数据资源[:：]?\s*(\d[\d,\s]*)', '数据资源:'),
                    (r'(?:共|累计|已|现有)\s*(\d[\d,\s]*)\s*个数据集', 'X个数据集'),
                    (r'(?:共|累计|已|现有)\s*(\d[\d,\s]*)\s*条数据', 'X条数据'),
                    (r'(?:共|累计|已|现有)\s*(\d[\d,\s]*)\s*个目录', 'X个目录'),
                    (r'(?:共|累计|已|现有)\s*(\d[\d,\s]*)\s*个资源', 'X个资源'),
                ]
                
                for pattern, label in high_conf_patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for m in matches:
                        num_str = m.replace(',', '').replace(' ', '')
                        try:
                            val = int(num_str)
                            if 5 <= val <= 5000000:
                                idx = text.find(m)
                                ctx = text[max(0, idx-30):idx+len(m)+30].replace('\n', ' ')
                                result['dataset_count'] = val
                                result['source_url'] = current_url
                                result['source_text'] = ctx
                                result['method'] = 'text_pattern:%s' % label
                                result['status'] = 'success'
                                return result
                        except:
                            pass
                
                # 策略2: 搜索分页信息中的总数（如"共 1234 条"在列表区域）
                pagination_patterns = [
                    r'(?:显示|共有|总共|合计|共)\s*(\d[\d,\s]*)\s*条',
                    r'(?:找到|检索到|查询到)\s*(\d[\d,\s]*)\s*条',
                    r'(\d[\d,\s]*)\s*条记录',
                    r'(?:总共|合计)\s*(\d[\d,\s]*)\s*页',  # 页数不是数量，但可以作为参考
                ]
                for pattern in pagination_patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for m in matches:
                        num_str = m.replace(',', '').replace(' ', '')
                        try:
                            val = int(num_str)
                            if 5 <= val <= 5000000:
                                idx = text.find(m)
                                ctx = text[max(0, idx-30):idx+len(m)+30].replace('\n', ' ')
                                # 检查上下文是否包含"数据集""目录""资源"等关键词
                                nearby = text[max(0, idx-100):idx+100].lower()
                                if any(k in nearby for k in ['数据集', '数据目录', '资源', '目录', 'dataset', 'catalog']):
                                    result['dataset_count'] = val
                                    result['source_url'] = current_url
                                    result['source_text'] = ctx
                                    result['method'] = 'pagination_pattern'
                                    result['status'] = 'success'
                                    return result
                        except:
                            pass
                
                # 策略3: 搜索CSS计数器元素
                counter_selectors = [
                    '.count', '.num', '.total', '.sum', '.statistics',
                    '[class*="count"]', '[class*="num"]', '[class*="total"]',
                    '[id*="count"]', '[id*="num"]', '[id*="total"]',
                    '.data-count', '.catalog-count', '.dataset-count',
                ]
                for sel in counter_selectors:
                    try:
                        elems = page.query_selector_all(sel)
                        for elem in elems[:5]:
                            txt = elem.inner_text().strip()
                            num_match = re.search(r'(\d[\d,\s]*)', txt)
                            if num_match:
                                num_str = num_match.group(1).replace(',', '').replace(' ', '')
                                val = int(num_str)
                                if 5 <= val <= 5000000:
                                    # 检查元素附近是否有"数据集"等关键词
                                    nearby = elem.evaluate('el => el.parentElement ? el.parentElement.innerText : ""')
                                    if nearby and any(k in nearby.lower() for k in ['数据集', '数据目录', '资源', '目录', 'dataset', 'catalog', '数据', '开放']):
                                        result['dataset_count'] = val
                                        result['source_url'] = current_url
                                        result['source_text'] = txt[:80]
                                        result['method'] = 'css_selector:%s' % sel
                                        result['status'] = 'success'
                                        return result
                    except:
                        pass
                
                # 策略4: 搜索script中的计数变量
                script_tags = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
                for script in script_tags:
                    js_patterns = [
                        r'(datasetCount|totalCount|dataCount|catalogCount|resourceCount)\s*[:=]\s*["\']?(\d[\d,]*)["\']?',
                        r'(total|count)\s*[:=]\s*["\']?(\d[\d,]*)["\']?',
                    ]
                    for pattern in js_patterns:
                        matches = re.findall(pattern, script, re.IGNORECASE)
                        for m in matches:
                            num_str = m[1].replace(',', '')
                            try:
                                val = int(num_str)
                                if 5 <= val <= 5000000:
                                    result['dataset_count'] = val
                                    result['source_url'] = current_url
                                    result['source_text'] = '%s=%s' % (m[0], num_str)
                                    result['method'] = 'js_variable:%s' % m[0]
                                    result['status'] = 'success'
                                    return result
                            except:
                                pass
                
            except Exception as e:
                # 继续尝试下一个URL
                continue
        
        # 所有URL都尝试过，仍未找到
        result['status'] = 'not_found'
        
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)[:200]
    finally:
        if context:
            context.close()
    
    return result


def main():
    # 定义需要深入采集的平台
    platforms_to_collect = [
        # NO DATA FOUND 平台
        {'code': 'anhui', 'name': '安徽省', 'dataset_page_url': None},
        {'code': 'fujian', 'name': '福建省', 'dataset_page_url': 'https://www.fjbigdata.com.cn/'},
        {'code': 'guangxi', 'name': '广西壮族自治区', 'dataset_page_url': 'https://data.gxzf.gov.cn/portal/catalog/'},
        {'code': 'henan', 'name': '河南省', 'dataset_page_url': None},
        {'code': 'hunan', 'name': '湖南省', 'dataset_page_url': 'https://data.hunan.gov.cn/business/catalog/list.do'},
        {'code': 'jiangsu', 'name': '江苏省', 'dataset_page_url': 'https://data.jszwfw.gov.cn:8118/extranet'},
        {'code': 'shanghai', 'name': '上海市', 'dataset_page_url': None},
        {'code': 'sichuan', 'name': '四川省', 'dataset_page_url': 'https://scdata.net.cn/oportal/catalog/'},
        {'code': 'tianjin', 'name': '天津市', 'dataset_page_url': None},
        {'code': 'yunnan', 'name': '云南省', 'dataset_page_url': None},
        # URL失效平台（尝试原URL+备用URL）
        {'code': 'gansu', 'name': '甘肃省', 'dataset_page_url': None},
        {'code': 'hebei', 'name': '河北省', 'dataset_page_url': None},
        {'code': 'heilongjiang', 'name': '黑龙江省', 'dataset_page_url': None},
        {'code': 'ningxia', 'name': '宁夏回族自治区', 'dataset_page_url': None},
        {'code': 'qinghai', 'name': '青海省', 'dataset_page_url': None},
        {'code': 'shaanxi', 'name': '陕西省', 'dataset_page_url': None},
        {'code': 'xinjiang', 'name': '新疆维吾尔自治区', 'dataset_page_url': None},
        {'code': 'xizang', 'name': '西藏自治区', 'dataset_page_url': None},
    ]
    
    # 补充URL
    for p in platforms_to_collect:
        url = get_platform_url(p['code'])
        if url:
            p['url'] = url
    
    print('深度采集 %d 个平台' % len(platforms_to_collect))
    print()
    
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        for platform in platforms_to_collect:
            if 'url' not in platform:
                print('跳过 %s: 无URL' % platform['name'])
                continue
            
            print('深度采集: %s (%s) ...' % (platform['name'], platform['url']), end=' ')
            result = collect_dataset_count(browser, platform)
            results.append(result)
            
            if result['status'] == 'success':
                print('OK -> dc=%d | method=%s' % (result['dataset_count'], result['method']))
                print('  source: %s' % result['source_url'])
                print('  text: %s' % result['source_text'][:80])
            elif result['status'] == 'not_found':
                print('NOT FOUND')
            else:
                print('ERROR: %s' % result.get('error', 'unknown'))
        
        browser.close()
    
    # 保存结果
    output_path = Path('data/deep_collect_results.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print()
    print('=' * 70)
    print('深度采集完成，结果保存到: %s' % output_path)
    print('=' * 70)
    
    found = sum(1 for r in results if r['status'] == 'success')
    errors = sum(1 for r in results if r['status'] == 'error')
    not_found = sum(1 for r in results if r['status'] == 'not_found')
    print('成功: %d | 未找到: %d | 错误: %d' % (found, not_found, errors))
    
    print()
    print('成功结果汇总:')
    for r in results:
        if r['status'] == 'success':
            print('  %-10s: %d | %s | %s' % (r['name'], r['dataset_count'], r['method'], r['source_url']))

if __name__ == '__main__':
    main()
