"""
OGD-Collector Pro V3 - 数据集数量采集引擎
基于平台规则映射表进行精准采集
"""

import json
import re
import sqlite3
from datetime import datetime
from playwright.sync_api import sync_playwright

# 加载平台规则
with open('v3_platform_rules.json', 'r', encoding='utf-8') as f:
    RULES = json.load(f)

PLATFORMS = {p['code']: p for p in RULES['platforms']}

def extract_dataset_count(code, debug=False):
    """
    为指定平台采集数据集数量
    返回: {
        'code': str,
        'name': str,
        'dataset_count': int or None,
        'source_url': str,
        'source_text': str,
        'confidence': str,
        'method': str,
        'status': str,
        'collected_at': str,
        'error': str or None
    }
    """
    platform = PLATFORMS.get(code)
    if not platform:
        return {'code': code, 'name': code, 'status': 'error', 'error': '平台未在规则表中定义'}

    result = {
        'code': code,
        'name': platform['name'],
        'dataset_count': None,
        'source_url': None,
        'source_text': None,
        'confidence': 'low',
        'method': None,
        'status': 'pending',
        'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'error': None
    }

    urls = platform['urls']
    rules = platform['extraction_rules']

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080}
        )

        try:
            # 策略1：尝试首页提取
            if 'primary' in rules and rules['primary']['location'] == 'homepage':
                page = context.new_page()
                page.goto(urls['homepage'], wait_until='networkidle', timeout=30000)
                page.wait_for_timeout(3000)
                text = page.inner_text('body')

                if debug:
                    print(f"[{code}] 首页文本长度: {len(text)}")

                # CSS选择器优先
                if rules['primary']['method'] == 'css_selector':
                    selector = rules['primary']['selector']
                    try:
                        elements = page.query_selector_all(selector)
                        for el in elements:
                            val = el.inner_text().strip()
                            match = re.search(rules['primary']['pattern'], val)
                            if match:
                                num = int(match.group(1).replace(',', ''))
                                result['dataset_count'] = num
                                result['source_url'] = urls['homepage']
                                result['source_text'] = val[:200]
                                result['confidence'] = 'high'
                                result['method'] = f"css_selector:{selector}"
                                result['status'] = 'success'
                                if debug:
                                    print(f"[{code}] CSS提取成功: {num}")
                                break
                    except Exception as e:
                        if debug:
                            print(f"[{code}] CSS选择器失败: {e}")

                # 正则匹配
                if result['status'] != 'success' and rules['primary']['method'] == 'regex':
                    pattern = rules['primary']['pattern']
                    match = re.search(pattern, text)
                    if match:
                        num = int(match.group(1).replace(',', ''))
                        result['dataset_count'] = num
                        result['source_url'] = urls['homepage']
                        result['source_text'] = match.group(0)[:200]
                        result['confidence'] = 'medium'
                        result['method'] = f"regex:{pattern[:50]}"
                        result['status'] = 'success'
                        if debug:
                            print(f"[{code}] 正则提取成功: {num}")

                page.close()

            # 策略2：尝试数据目录页提取
            if result['status'] != 'success' and urls.get('dataset_page'):
                page = context.new_page()
                page.goto(urls['dataset_page'], wait_until='networkidle', timeout=30000)
                page.wait_for_timeout(3000)
                text = page.inner_text('body')

                if debug:
                    print(f"[{code}] 目录页文本长度: {len(text)}")

                # 尝试secondary规则
                if 'secondary' in rules:
                    sec = rules['secondary']
                    if sec['location'] in ['dataset_page', 'dataset_page_text']:
                        if sec['method'] == 'css_selector':
                            selector = sec['selector']
                            try:
                                elements = page.query_selector_all(selector)
                                for el in elements:
                                    val = el.inner_text().strip()
                                    match = re.search(sec['pattern'], val)
                                    if match:
                                        num = int(match.group(1).replace(',', ''))
                                        result['dataset_count'] = num
                                        result['source_url'] = urls['dataset_page']
                                        result['source_text'] = val[:200]
                                        result['confidence'] = 'medium'
                                        result['method'] = f"css_selector:{selector}"
                                        result['status'] = 'success'
                                        if debug:
                                            print(f"[{code}] 目录页CSS提取成功: {num}")
                                        break
                            except Exception as e:
                                if debug:
                                    print(f"[{code}] 目录页CSS失败: {e}")

                        if result['status'] != 'success' and sec['method'] == 'regex':
                            pattern = sec['pattern']
                            match = re.search(pattern, text)
                            if match:
                                num = int(match.group(1).replace(',', ''))
                                result['dataset_count'] = num
                                result['source_url'] = urls['dataset_page']
                                result['source_text'] = match.group(0)[:200]
                                result['confidence'] = 'medium'
                                result['method'] = f"regex:{pattern[:50]}"
                                result['status'] = 'success'
                                if debug:
                                    print(f"[{code}] 目录页正则提取成功: {num}")

                # 通用策略：查找分页信息
                if result['status'] != 'success':
                    # 匹配 "共 X 页" 或 "共 X 条"
                    page_match = re.search(r'共\s*([0-9,]+)\s*页', text)
                    item_match = re.search(r'共\s*([0-9,]+)\s*条(?:目录|记录|数据)', text)

                    if item_match:
                        num = int(item_match.group(1).replace(',', ''))
                        result['dataset_count'] = num
                        result['source_url'] = urls['dataset_page']
                        result['source_text'] = item_match.group(0)[:200]
                        result['confidence'] = 'high'
                        result['method'] = '通用分页:共X条'
                        result['status'] = 'success'
                        if debug:
                            print(f"[{code}] 分页信息提取成功: {num}")
                    elif page_match:
                        # 需要计算：页数 * 每页条数
                        # 尝试找每页条数
                        per_page_match = re.search(r'每页\s*([0-9,]+)\s*条', text)
                        per_page = int(per_page_match.group(1).replace(',', '')) if per_page_match else 10
                        total_pages = int(page_match.group(1).replace(',', ''))
                        estimated = total_pages * per_page
                        result['dataset_count'] = estimated
                        result['source_url'] = urls['dataset_page']
                        result['source_text'] = f"{page_match.group(0)}, 每页{per_page}条, 估算{estimated}"
                        result['confidence'] = 'medium'
                        result['method'] = '分页估算'
                        result['status'] = 'success'
                        if debug:
                            print(f"[{code}] 分页估算: {total_pages}页 x {per_page} = {estimated}")

                page.close()

            # 如果都没成功，标记为not_found
            if result['status'] != 'success':
                result['status'] = 'not_found'
                result['error'] = '未找到数据集数量'

        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)[:200]
            if debug:
                print(f"[{code}] 错误: {e}")
        finally:
            browser.close()

    return result


def collect_all_platforms(codes=None, debug=False):
    """
    采集所有（或指定）平台的数据集数量
    """
    if codes is None:
        codes = list(PLATFORMS.keys())

    results = []
    for code in codes:
        if debug:
            print(f"\n{'='*60}")
            print(f"正在采集: {PLATFORMS[code]['name']}")
            print(f"{'='*60}")

        result = extract_dataset_count(code, debug=debug)
        results.append(result)

        if debug:
            print(f"结果: {result['dataset_count']} (置信度: {result['confidence']}, 状态: {result['status']})")

    return results


def save_results(results, filename='data/v3_collection_results.json'):
    """保存采集结果到JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"结果已保存到: {filename}")


def update_database(results):
    """更新数据库中的collection_records表"""
    conn = sqlite3.connect('data/ogd_database.db')
    cursor = conn.cursor()

    for r in results:
        if r['status'] == 'success' and r['dataset_count'] is not None:
            # 查找platform_id
            cursor.execute('SELECT id FROM platforms WHERE code = ?', (r['code'],))
            row = cursor.fetchone()
            if row:
                platform_id = row[0]
                # 插入新记录
                cursor.execute('''
                    INSERT INTO collection_records 
                    (platform_id, dataset_count, status, collected_at, notes)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    platform_id,
                    r['dataset_count'],
                    'available',
                    r['collected_at'],
                    f"V3采集: {r['method']}, 置信度: {r['confidence']}, 来源: {r['source_url']}"
                ))
                print(f"已更新数据库: {r['name']} -> {r['dataset_count']}")

    conn.commit()
    conn.close()
    print("数据库更新完成")


def generate_report(results):
    """生成采集报告"""
    total = len(results)
    success = sum(1 for r in results if r['status'] == 'success')
    high_conf = sum(1 for r in results if r['confidence'] == 'high')
    medium_conf = sum(1 for r in results if r['confidence'] == 'medium')
    not_found = sum(1 for r in results if r['status'] == 'not_found')
    errors = sum(1 for r in results if r['status'] == 'error')

    print("\n" + "="*80)
    print("V3采集报告")
    print("="*80)
    print(f"总平台数: {total}")
    print(f"采集成功: {success} ({success/total*100:.1f}%)")
    print(f"  - 高置信度: {high_conf}")
    print(f"  - 中置信度: {medium_conf}")
    print(f"未找到: {not_found}")
    print(f"错误: {errors}")
    print()

    # 显示成功结果
    print("成功采集的平台:")
    for r in sorted(results, key=lambda x: x['dataset_count'] or 0, reverse=True):
        if r['status'] == 'success':
            print(f"  {r['name']:12s} | {r['dataset_count']:8,d} | {r['confidence']:8s} | {r['method'][:40]}")

    print()
    if not_found > 0:
        print("未找到的平台:")
        for r in results:
            if r['status'] == 'not_found':
                print(f"  {r['name']}")

    if errors > 0:
        print("错误的平台:")
        for r in results:
            if r['status'] == 'error':
                print(f"  {r['name']}: {r['error']}")

    print("="*80)


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        # 采集指定平台
        code = sys.argv[1]
        result = extract_dataset_count(code, debug=True)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 采集所有平台
        print("开始V3全量采集...")
        results = collect_all_platforms(debug=True)
        save_results(results)
        update_database(results)
        generate_report(results)
