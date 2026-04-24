#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上海平台WAF高级突破测试
使用stealth策略和真实用户行为模拟
"""
import sys
import io
import os
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

from playwright.sync_api import sync_playwright

def test_shanghai_stealth():
    """使用多种策略测试上海平台"""
    
    strategies = [
        {
            'name': '标准headless+长等待',
            'headless': True,
            'wait': 10,
            'args': ['--disable-blink-features=AutomationControlled']
        },
        {
            'name': 'headful+长等待+鼠标移动',
            'headless': False,
            'wait': 15,
            'args': ['--disable-blink-features=AutomationControlled']
        },
        {
            'name': 'headful+禁用websecurity',
            'headless': False,
            'wait': 10,
            'args': ['--disable-web-security', '--disable-features=IsolateOrigins,site-per-process']
        },
    ]
    
    url = "https://data.sh.gov.cn"
    
    for strategy in strategies:
        print(f"\n{'='*60}")
        print(f"策略: {strategy['name']}")
        print(f"{'='*60}")
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=strategy['headless'],
                    args=strategy['args']
                )
                
                context = browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    viewport={'width': 1920, 'height': 1080},
                    locale='zh-CN',
                    timezone_id='Asia/Shanghai',
                    extra_http_headers={
                        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Cache-Control': 'max-age=0',
                    }
                )
                
                # 注入反检测脚本
                context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [{name: 'Chrome PDF Plugin'}, {name: 'Native Client'}]
                    });
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['zh-CN', 'zh', 'en']
                    });
                    window.chrome = { runtime: {} };
                """)
                
                page = context.new_page()
                
                # 如果headful，模拟鼠标移动
                if not strategy['headless']:
                    page.mouse.move(100, 100)
                    time.sleep(0.5)
                    page.mouse.move(200, 300)
                    time.sleep(0.5)
                
                print(f"访问: {url}")
                response = page.goto(url, wait_until='domcontentloaded', timeout=45000)
                
                # 等待页面完全加载
                time.sleep(strategy['wait'])
                
                # 尝试滚动触发懒加载
                if not strategy['headless']:
                    page.evaluate("window.scrollTo(0, 500)")
                    time.sleep(2)
                
                html = page.content()
                title = page.title()
                
                print(f"标题: {title}")
                print(f"HTML长度: {len(html)}")
                print(f"URL: {page.url}")
                
                if len(html) < 200:
                    print(f"HTML内容: {html[:200]}")
                else:
                    print(f"HTML前500字符: {html[:500]}")
                
                # 检查是否有数据集相关元素
                dataset_keywords = ['数据集', 'dataset', '数据目录', 'data catalog', '开放数据']
                found_keywords = [k for k in dataset_keywords if k in html.lower()]
                print(f"找到关键词: {found_keywords}")
                
                browser.close()
                
        except Exception as e:
            print(f"错误: {str(e)[:200]}")

if __name__ == '__main__':
    test_shanghai_stealth()
