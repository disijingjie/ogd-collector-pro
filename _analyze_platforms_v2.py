"""
改进版平台结构分析 - 解决重定向污染和精确提取数据集数量
为每个平台创建独立的browser context
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
    cursor.execute("SELECT code, name, province, url FROM platforms WHERE tier='省级' ORDER BY code")
    rows = cursor.fetchall()
    conn.close()
    return rows

def extract_dataset_count_from_text(text, html):
    """
    从页面文本中精确提取数据集数量
    策略：优先匹配明确包含"数据集""数据目录""数据资源"等关键词的模式
    """
    candidates = []
    
    # 高置信度模式（明确提到数据集/目录/资源）
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
        (r'(?:已|现有)?开放[:：]?\s*(\d[\d,\s]*)\s*个(?:数据)?', '开放X个'),
    ]
    
    for pattern, label in high_conf_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            num_str = m.replace(',', '').replace(' ', '')
            try:
                val = int(num_str)
                if 10 <= val <= 5000000:
                    # 查找上下文
                    idx = text.find(m)
                    ctx = text[max(0, idx-40):idx+len(m)+40].replace('\n', ' ')
                    candidates.append({'value': val, 'confidence': 'high', 'pattern': label, 'context': ctx})
            except:
                pass
    
    # 中置信度模式（数字+单位，在统计区域）
    medium_conf_patterns = [
        (r'(\d[\d,\s]*)\s*个数据集', '个数据集'),
        (r'(\d[\d,\s]*)\s*条数据', '条数据'),
        (r'(\d[\d,\s]*)\s*个目录', '个目录'),
        (r'(\d[\d,\s]*)\s*个资源', '个资源'),
        (r'(\d[\d,\s]*)\s*万条', '万条'),
    ]
    
    for pattern, label in medium_conf_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            num_str = m.replace(',', '').replace(' ', '')
            try:
                val = int(num_str)
                if 10 <= val <= 5000000:
                    idx = text.find(m)
                    ctx = text[max(0, idx-40):idx+len(m)+40].replace('\n', ' ')
                    candidates.append({'value': val, 'confidence': 'medium', 'pattern': label, 'context': ctx})
            except:
                pass
    
    return candidates

def analyze_single_platform(browser, url, name, code):
    """为单个平台创建独立context进行分析"""
    result = {
        'code': code, 'name': name, 'url': url,
        'status': 'unknown', 'dataset_count': None,
        'candidates': [], 'dataset_page_url': None,
        'notes': []
    }
    
    context = None
    try:
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080},
            ignore_https_errors=True,
        )
        page = context.new_page()
        
        # 访问首页
        page.goto(url, timeout=30000, wait_until='domcontentloaded')
        page.wait_for_timeout(5000)  # 等待JS渲染
        
        text = page.inner_text('body')
        html = page.content()
        result['status'] = 'success'
        
        # 提取候选数据集数量
        candidates = extract_dataset_count_from_text(text, html)
        result['candidates'] = candidates
        
        # 查找数据目录页链接
        nav_links = page.query_selector_all('a')
        for link in nav_links:
            try:
                href = link.get_attribute('href') or ''
                link_text = (link.inner_text() or '').strip()
                if any(k in link_text for k in ['数据集', '数据目录', '数据资源', '资源目录', '开放目录', 'catalog', 'dataset', '数据开放']):
                    if href and not href.startswith('javascript') and not href.startswith('#'):
                        if not href.startswith('http'):
                            href = urljoin(url, href)
                        result['dataset_page_url'] = href
                        break
            except:
                pass
        
        # 如果首页没找到，尝试访问数据目录页
        if not candidates and result['dataset_page_url']:
            try:
                page.goto(result['dataset_page_url'], timeout=20000, wait_until='domcontentloaded')
                page.wait_for_timeout(3000)
                text2 = page.inner_text('body')
                candidates2 = extract_dataset_count_from_text(text2, html)
                if candidates2:
                    result['candidates'] = candidates2
                    result['notes'].append('dataset_page_found')
            except Exception as e:
                result['notes'].append('dataset_page_error:%s' % str(e)[:50])
        
        # 选择最佳候选
        if candidates:
            # 优先高置信度，然后取最大值（数据集数量通常比部门数大）
            high_conf = [c for c in candidates if c['confidence'] == 'high']
            if high_conf:
                best = max(high_conf, key=lambda x: x['value'])
            else:
                best = max(candidates, key=lambda x: x['value'])
            result['dataset_count'] = best['value']
            result['best_candidate'] = best
        
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)[:200]
    finally:
        if context:
            context.close()
    
    return result


def main():
    platforms = get_platforms()
    print('需要分析 %d 个省级平台' % len(platforms))
    print()
    
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        for code, name, province, url in platforms:
            print('分析: %s (%s) ...' % (name, url), end=' ')
            result = analyze_single_platform(browser, url, name, code)
            results.append(result)
            
            if result['status'] == 'success':
                if result['dataset_count']:
                    print('OK -> dataset_count=%d' % result['dataset_count'])
                    if result['notes']:
                        print('  notes: %s' % result['notes'])
                else:
                    print('NO DATA FOUND')
                    if result['dataset_page_url']:
                        print('  -> 数据目录页: %s' % result['dataset_page_url'])
            else:
                print('ERROR: %s' % result.get('error', 'unknown'))
        
        browser.close()
    
    # 保存结果
    output_path = Path('data/platform_analysis_v2.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print()
    print('=' * 70)
    print('分析完成，结果保存到: %s' % output_path)
    print('=' * 70)
    
    found = sum(1 for r in results if r.get('dataset_count'))
    errors = sum(1 for r in results if r['status'] == 'error')
    print('成功找到: %d/%d' % (found, len(results)))
    print('访问失败: %d/%d' % (errors, len(results)))
    print('未找到: %d/%d' % (len(results) - found - errors, len(results)))
    
    print()
    print('详细结果:')
    for r in results:
        dc = r.get('dataset_count')
        status = 'FOUND' if dc else ('ERROR' if r['status'] == 'error' else 'NOT FOUND')
        candidates_info = ''
        if r.get('candidates'):
            vals = [c['value'] for c in r['candidates']]
            candidates_info = ' candidates=%s' % vals
        print('  %-10s | %-8s | %s | dc=%s%s' % (r['name'], r['code'], status, dc if dc else 'N/A', candidates_info))

if __name__ == '__main__':
    main()
