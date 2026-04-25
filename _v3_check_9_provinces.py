"""
核实31省中另外9个未纳入讨论的平台状态
甘肃、河北、黑龙江、宁夏、青海、陕西、新疆、西藏 + 安徽
"""

from playwright.sync_api import sync_playwright

provinces = [
    ('gansu', '甘肃省', 'https://data.gansu.gov.cn/'),
    ('hebei', '河北省', 'https://data.hebei.gov.cn/'),
    ('heilongjiang', '黑龙江省', 'https://data.hlj.gov.cn/'),
    ('ningxia', '宁夏回族自治区', 'https://data.nx.gov.cn/'),
    ('qinghai', '青海省', 'https://data.qinghai.gov.cn/'),
    ('shaanxi', '陕西省', 'https://data.shaanxi.gov.cn/'),
    ('xinjiang', '新疆维吾尔自治区', 'https://data.xinjiang.gov.cn/'),
    ('xizang', '西藏自治区', 'https://data.xizang.gov.cn/'),
]

print("=" * 60)
print("核实9个未纳入讨论的平台状态")
print("=" * 60)

results = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for code, name, url in provinces:
        print(f"\n【{name}】{url}")
        try:
            page = browser.new_page()
            page.goto(url, wait_until='domcontentloaded', timeout=15000)
            page.wait_for_timeout(3000)
            
            title = page.title()
            text = page.inner_text('body')[:200]
            
            print(f"  标题: {title}")
            print(f"  文本: {text[:150]}")
            
            # 判断状态
            if '404' in text or 'Not Found' in text:
                status = '平台不存在/已关闭'
            elif '502' in text or '503' in text or '504' in text:
                status = '服务器错误'
            elif len(text) < 50:
                status = '页面内容极少/可能关闭'
            else:
                status = '平台存在'
            
            print(f"  状态: {status}")
            results.append((name, url, status, title))
            page.close()
        except Exception as e:
            error_msg = str(e)[:80]
            if 'ERR_NAME_NOT_RESOLVED' in error_msg:
                status = 'DNS失败/域名不存在'
            elif 'Timeout' in error_msg:
                status = '连接超时'
            else:
                status = f'访问失败: {error_msg}'
            print(f"  状态: {status}")
            results.append((name, url, status, 'N/A'))
    browser.close()

print("\n" + "=" * 60)
print("汇总结果")
print("=" * 60)
print(f"{'省份':<15} {'状态':<30} {'标题':<20}")
print("-" * 60)
for name, url, status, title in results:
    print(f"{name:<15} {status:<30} {title[:20]:<20}")

# 统计
existing = sum(1 for _, _, status, _ in results if '平台存在' in status)
closed = sum(1 for _, _, status, _ in results if '不存在' in status or '关闭' in status or 'DNS' in status or '超时' in status)
print(f"\n平台存在: {existing}个")
print(f"平台关闭/不存在: {closed}个")
