"""
逐个分析22个省级平台的首页结构，定位数据集数量的显示位置
使用Playwright获取渲染后的页面内容（包括JS动态加载的内容）
"""
import sqlite3
import json
import re
from playwright.sync_api import sync_playwright
from pathlib import Path

DB_PATH = Path('data/ogd_database.db')

def get_platforms():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("SELECT code, name, province, url FROM platforms WHERE tier='省级' ORDER BY code")
    rows = cursor.fetchall()
    conn.close()
    return rows

def analyze_platform(page, url, name, code):
    """分析单个平台的首页结构"""
    result = {
        'code': code,
        'name': name,
        'url': url,
        'status': 'unknown',
        'dataset_count_homepage': None,
        'dataset_count_patterns': [],
        'dataset_page_url': None,
        'api_endpoints': [],
        'html_snippets': [],
        'error': None
    }
    
    try:
        # 访问首页，等待页面加载
        page.goto(url, timeout=30000, wait_until='networkidle')
        page.wait_for_timeout(3000)  # 等待JS渲染
        
        html = page.content()
        text = page.inner_text('body')
        result['status'] = 'success'
        
        # 策略1: 在页面文本中搜索数据集数量相关模式
        patterns = [
            (r'(\d[\d,]*)\s*个数据集', '个数据集'),
            (r'(\d[\d,]*)\s*条数据', '条数据'),
            (r'数据集[:：]\s*(\d[\d,]*)', '数据集:'),
            (r'共\s*(\d[\d,]*)\s*条', '共X条'),
            (r'(\d[\d,]*)\s*个目录', '个目录'),
            (r'目录[:：]\s*(\d[\d,]*)', '目录:'),
            (r'(\d[\d,]*)\s*个资源', '个资源'),
            (r'资源[:：]\s*(\d[\d,]*)', '资源:'),
            (r'数据总量[:：]\s*(\d[\d,]*)', '数据总量:'),
            (r'开放[:：]\s*(\d[\d,]*)\s*个', '开放X个'),
            (r'(\d[\d,]*)\s*万条', '万条'),
            (r'(\d[\d,]*)\s*万.+数据', '万+数据'),
            (r'累计[:：]\s*(\d[\d,]*)', '累计:'),
            (r'已发布[:：]\s*(\d[\d,]*)', '已发布:'),
            (r'数据[:：]\s*(\d[\d,]*)\s*个', '数据X个'),
            (r'(\d[\d,]*)\s*datasets?', 'datasets'),
            (r'total[:：]\s*(\d[\d,]*)', 'total:'),
            (r'count[:：]\s*(\d[\d,]*)', 'count:'),
        ]
        
        for pattern, label in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                num_str = m if isinstance(m, str) else m[0]
                num_str = num_str.replace(',', '').replace(' ', '')
                try:
                    val = int(num_str)
                    if 10 <= val <= 10000000:
                        result['dataset_count_patterns'].append({
                            'pattern': label,
                            'value': val,
                            'context': text[max(0, text.find(num_str)-30):text.find(num_str)+len(num_str)+30].replace('\n', ' ')
                        })
                except:
                    pass
        
        # 策略2: 查找可能的数据集列表页面链接
        nav_links = page.query_selector_all('a')
        for link in nav_links:
            try:
                href = link.get_attribute('href') or ''
                link_text = (link.inner_text() or '').strip()
                if any(k in link_text for k in ['数据集', '数据目录', '数据资源', '资源目录', '开放目录', 'catalog', 'dataset', '数据开放']):
                    if href and not href.startswith('javascript') and not href.startswith('#'):
                        if not href.startswith('http'):
                            from urllib.parse import urljoin
                            href = urljoin(url, href)
                        result['dataset_page_url'] = href
                        break
            except:
                pass
        
        # 策略3: 查找页面中的数字计数器元素（class或id包含count/num/total等）
        counter_selectors = [
            '[class*="count"]', '[class*="num"]', '[class*="total"]', 
            '[class*="data"]', '[class*="catalog"]', '[class*="dataset"]',
            '[id*="count"]', '[id*="num"]', '[id*="total"]',
            '[id*="data"]', '[id*="catalog"]', '[id*="dataset"]',
            '.statistics', '.stats', '.numbers', '.counter'
        ]
        for sel in counter_selectors:
            try:
                elems = page.query_selector_all(sel)
                for elem in elems[:3]:  # 最多取3个
                    try:
                        txt = elem.inner_text().strip()
                        num_match = re.search(r'(\d[\d,\s]*)', txt)
                        if num_match:
                            num_str = num_match.group(1).replace(',', '').replace(' ', '')
                            val = int(num_str)
                            if 10 <= val <= 10000000:
                                result['dataset_count_patterns'].append({
                                    'pattern': 'css_selector:%s' % sel,
                                    'value': val,
                                    'context': txt[:80]
                                })
                    except:
                        pass
            except:
                pass
        
        # 策略4: 查找可能的API端点
        api_patterns = [
            r'["\']([^"\']*api[^"\']*dataset[^"\']*)["\']',
            r'["\']([^"\']*api[^"\']*catalog[^"\']*)["\']',
            r'["\']([^"\']*api[^"\']*data[^"\']*)["\']',
            r'["\']([^"\']*dataset[^"\']*count[^"\']*)["\']',
            r'["\']([^"\']*total[^"\']*count[^"\']*)["\']',
        ]
        for pattern in api_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for m in matches[:3]:
                result['api_endpoints'].append(m)
        
        # 策略5: 搜索script标签中的计数变量
        script_tags = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
        for script in script_tags[:5]:
            js_patterns = [
                r'(datasetCount|totalCount|dataCount|catalogCount|resourceCount|openCount)\s*[:=]\s*["\']?(\d[\d,]*)["\']?',
                r'(total|count|num)\s*[:=]\s*["\']?(\d[\d,]*)["\']?',
            ]
            for pattern in js_patterns:
                matches = re.findall(pattern, script, re.IGNORECASE)
                for m in matches:
                    var_name = m[0]
                    num_str = m[1].replace(',', '')
                    try:
                        val = int(num_str)
                        if 10 <= val <= 10000000:
                            result['dataset_count_patterns'].append({
                                'pattern': 'js_var:%s' % var_name,
                                'value': val,
                                'context': '%s=%s' % (var_name, num_str)
                            })
                    except:
                        pass
        
        # 去重并选择最可能的值
        if result['dataset_count_patterns']:
            # 按value分组，选择出现次数最多的
            from collections import Counter
            values = [p['value'] for p in result['dataset_count_patterns']]
            most_common = Counter(values).most_common(1)
            if most_common:
                result['dataset_count_homepage'] = most_common[0][0]
        
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)
    
    return result


def main():
    platforms = get_platforms()
    print('需要分析 %d 个省级平台' % len(platforms))
    print()
    
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        for code, name, province, url in platforms:
            print('分析: %s (%s) ...' % (name, url), end=' ')
            result = analyze_platform(page, url, name, code)
            results.append(result)
            
            if result['status'] == 'success':
                if result['dataset_count_homepage']:
                    print('OK -> dataset_count=%d' % result['dataset_count_homepage'])
                else:
                    print('NO DATA FOUND')
                    if result['dataset_page_url']:
                        print('  -> 发现数据目录页: %s' % result['dataset_page_url'])
            else:
                print('ERROR: %s' % result['error'])
        
        browser.close()
    
    # 保存结果
    output_path = Path('data/platform_structure_analysis.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print()
    print('=' * 70)
    print('分析完成，结果保存到: %s' % output_path)
    print('=' * 70)
    
    # 汇总
    found = sum(1 for r in results if r.get('dataset_count_homepage'))
    errors = sum(1 for r in results if r['status'] == 'error')
    print('成功找到数据集数量: %d/%d' % (found, len(results)))
    print('访问失败: %d/%d' % (errors, len(results)))
    print('未找到: %d/%d' % (len(results) - found - errors, len(results)))
    
    print()
    print('详细结果:')
    for r in results:
        dc = r.get('dataset_count_homepage')
        status = 'FOUND' if dc else ('ERROR' if r['status'] == 'error' else 'NOT FOUND')
        print('  %-10s | %-8s | %s | dc=%s' % (r['name'], r['code'], status, dc if dc else 'N/A'))

if __name__ == '__main__':
    main()
