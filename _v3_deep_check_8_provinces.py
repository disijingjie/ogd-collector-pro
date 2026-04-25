"""
深入核实8个"无平台"省份的数据开放形式
查找：政务服务平台嵌入、地市平台、专题开放、数据局官网等
"""

from playwright.sync_api import sync_playwright
import re

provinces = [
    ('gansu', '甘肃省', [
        'https://zwfw.gansu.gov.cn/',
        'https://data.gansu.gov.cn/',
        'https://gansu.gov.cn/',
        'https://www.gansu.gov.cn/zwgk/zcwj/zcjd/',
    ]),
    ('hebei', '河北省', [
        'https://www.hebei.gov.cn/',
        'https://hebei.gov.cn/',
        'https://www.hebei.gov.cn/columns/4a408627-4b1c-4b6e-bf63-1f5a5b5b5b5b/',
        'https://zwfw.hebei.gov.cn/',
    ]),
    ('heilongjiang', '黑龙江省', [
        'https://www.hlj.gov.cn/',
        'https://hlj.gov.cn/',
        'https://zwfw.hlj.gov.cn/',
    ]),
    ('ningxia', '宁夏回族自治区', [
        'https://www.nx.gov.cn/',
        'https://zwfw.nx.gov.cn/',
        'https://ningxia.gov.cn/',
    ]),
    ('qinghai', '青海省', [
        'https://www.qinghai.gov.cn/',
        'https://qinghai.gov.cn/',
        'https://zwfw.qinghai.gov.cn/',
    ]),
    ('shaanxi', '陕西省', [
        'https://www.shaanxi.gov.cn/',
        'https://shaanxi.gov.cn/',
        'https://zwfw.shaanxi.gov.cn/',
    ]),
    ('xinjiang', '新疆维吾尔自治区', [
        'https://www.xinjiang.gov.cn/',
        'https://xinjiang.gov.cn/',
        'https://zwfw.xinjiang.gov.cn/',
    ]),
    ('xizang', '西藏自治区', [
        'https://www.xizang.gov.cn/',
        'https://xizang.gov.cn/',
        'https://zwfw.xizang.gov.cn/',
    ]),
]

print("=" * 70)
print("深入核实8个省份的数据开放形式")
print("=" * 70)

results = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for code, name, urls in provinces:
        print(f"\n【{name}】")
        province_found = False
        for url in urls:
            try:
                print(f"  尝试: {url}")
                page = browser.new_page()
                page.goto(url, wait_until='domcontentloaded', timeout=15000)
                page.wait_for_timeout(3000)
                
                title = page.title()
                text = page.inner_text('body')
                html = page.content()
                
                print(f"    标题: {title[:50]}")
                
                # 查找数据开放相关关键词
                keywords = ['数据开放', '开放数据', '数据共享', '公共数据', '数据资源', '数据目录']
                found_keywords = [k for k in keywords if k in text]
                if found_keywords:
                    print(f"    找到关键词: {found_keywords}")
                
                # 查找数据集/目录数量
                matches = re.findall(r'(\d{3,})', text)
                if matches:
                    print(f"    找到数字: {matches[:10]}")
                
                # 查找数据平台链接
                if 'data' in html.lower() or '开放' in text:
                    # 提取所有链接
                    links = page.eval_on_selector_all('a', 'elements => elements.map(e => e.href)')
                    data_links = [l for l in links if l and ('data' in l.lower() or '开放' in l or '数据' in l)]
                    if data_links:
                        print(f"    数据相关链接: {data_links[:5]}")
                
                page.close()
            except Exception as e:
                print(f"    [FAIL] {str(e)[:80]}")
                continue
    browser.close()

print("\n" + "=" * 70)
print("核实完成")
print("=" * 70)
