"""
安徽平台动态数据采集脚本 - 使用Playwright
目标: https://data.ahzwfw.gov.cn/dataopen-web/index.html
技术难点: 单页应用(SPA)，数据需JavaScript渲染后加载
"""
from playwright.sync_api import sync_playwright
import json
import time

def collect_anhui_data():
    """采集安徽省公共数据开放平台首页统计数据"""
    
    url = "https://data.ahzwfw.gov.cn/dataopen-web/index.html"
    
    with sync_playwright() as p:
        # 启动浏览器（无头模式）
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        try:
            print(f"正在访问: {url}")
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            # 等待页面加载完成（SPA需要额外等待）
            time.sleep(3)
            
            # 尝试多种选择器获取统计数据
            selectors = [
                # 可能的统计数字选择器
                '.statistics-number',
                '.stat-num',
                '.data-count',
                '[class*="num"]',
                '[class*="count"]',
                '.el-statistic__content',
                '.number',
                # 更通用的
                'span[class*="num"]',
                'div[class*="num"]',
            ]
            
            results = {
                'url': url,
                'title': page.title(),
                'status': 'success',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'selectors_attempted': [],
                'page_text_sample': page.inner_text('body')[:500] if page.locator('body').count() > 0 else 'N/A'
            }
            
            # 尝试获取页面所有数字
            all_numbers = []
            for selector in selectors:
                try:
                    elements = page.locator(selector).all()
                    if elements:
                        for i, elem in enumerate(elements[:10]):  # 最多取前10个
                            text = elem.inner_text().strip()
                            if text and any(c.isdigit() for c in text):
                                all_numbers.append({
                                    'selector': selector,
                                    'index': i,
                                    'text': text
                                })
                        results['selectors_attempted'].append({
                            'selector': selector,
                            'found': len(elements),
                            'samples': [e.inner_text().strip() for e in elements[:3]]
                        })
                except Exception as e:
                    results['selectors_attempted'].append({
                        'selector': selector,
                        'error': str(e)
                    })
            
            results['all_numbers_found'] = all_numbers
            
            # 尝试通过API请求获取数据
            print("尝试拦截API请求...")
            # 这里可以添加网络拦截逻辑
            
            browser.close()
            return results
            
        except Exception as e:
            browser.close()
            return {
                'url': url,
                'status': 'error',
                'error': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }

def collect_anhui_by_api():
    """尝试直接调用API获取数据"""
    import requests
    
    # 常见的数据接口路径
    api_endpoints = [
        "https://data.ahzwfw.gov.cn/dataopen-web/api/catalog/count",
        "https://data.ahzwfw.gov.cn/dataopen-web/api/dataset/count",
        "https://data.ahzwfw.gov.cn/dataopen-web/api/statistics",
        "https://data.ahzwfw.gov.cn/dataopen-web/api/openData/statistics",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://data.ahzwfw.gov.cn/dataopen-web/index.html'
    }
    
    results = []
    for endpoint in api_endpoints:
        try:
            resp = requests.get(endpoint, headers=headers, timeout=10, verify=False)
            results.append({
                'endpoint': endpoint,
                'status_code': resp.status_code,
                'content': resp.text[:200] if resp.status_code == 200 else None
            })
        except Exception as e:
            results.append({
                'endpoint': endpoint,
                'error': str(e)
            })
    
    return results

if __name__ == '__main__':
    print("=" * 60)
    print("安徽省公共数据开放平台 - 动态数据采集")
    print("=" * 60)
    
    # 方法1: Playwright动态渲染
    print("\n【方法1】Playwright动态渲染采集...")
    result1 = collect_anhui_data()
    print(json.dumps(result1, ensure_ascii=False, indent=2))
    
    # 方法2: API直接请求
    print("\n【方法2】API直接请求...")
    result2 = collect_anhui_by_api()
    print(json.dumps(result2, ensure_ascii=False, indent=2))
    
    print("\n" + "=" * 60)
    print("采集完成")
    print("=" * 60)
