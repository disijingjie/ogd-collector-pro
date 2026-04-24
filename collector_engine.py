"""
OGD-Collector Pro 采集引擎核心
三层架构数据开放平台采集系统 - 采集执行层
作者：文明（武汉大学信息管理学院博士生）
日期：2026-04-22
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime
import json
import time
import logging
import re
import os
import sqlite3
from urllib.parse import urljoin, urlparse
from pathlib import Path
import threading
import queue

from models import get_db, DB_PATH


class CollectorEngine:
    """
    三层架构数据采集引擎
    支持：省级31 + 副省级13 + 地级市287（抽样60）
    采集指标：4E框架（供给保障、平台服务、数据质量、利用效果）
    """
    
    def __init__(self, task_id=None, max_workers=3, delay=2):
        self.task_id = task_id
        self.max_workers = max_workers
        self.delay = delay
        self.is_running = False
        self.is_paused = False
        self.progress_queue = queue.Queue()
        
        # HTTP会话配置
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        })
        
        # 采集统计
        self.stats = {
            'total': 0,
            'completed': 0,
            'success': 0,
            'failed': 0,
            'current_platform': '',
            'start_time': None,
            'elapsed': 0
        }
        
        # 配置日志
        self._setup_logging()
        
    def _setup_logging(self):
        """配置采集日志"""
        log_dir = Path(__file__).parent / "data" / "logs"
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"task_{self.task_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        self.logger = logging.getLogger(f'collector_{self.task_id}')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            fh = logging.FileHandler(log_file, encoding='utf-8')
            fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(fh)
            
        self.log_path = str(log_file)
        
    def _log(self, level, message, platform_code=None):
        """记录日志到文件和数据库"""
        self.logger.log(getattr(logging, level), message)
        
        # 同时写入数据库日志表
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO collection_logs (task_id, platform_code, log_level, message, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (self.task_id, platform_code, level, message, datetime.now().isoformat()))
            conn.commit()
            conn.close()
        except Exception:
            pass
            
    def _save_snapshot(self, snapshot_type, data):
        """保存采集中间状态快照"""
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO collection_snapshots (task_id, snapshot_name, snapshot_type, snapshot_data, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                self.task_id,
                f"snapshot_{datetime.now().strftime('%H%M%S')}",
                snapshot_type,
                json.dumps(data, ensure_ascii=False),
                datetime.now().isoformat()
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            self._log('WARNING', f'保存快照失败: {e}')
            
    def _update_task_status(self, status, progress=None):
        """更新任务状态"""
        try:
            conn = get_db()
            cursor = conn.cursor()
            
            if progress:
                cursor.execute("""
                    UPDATE collection_tasks 
                    SET status=?, completed_count=?, success_count=?, fail_count=?, 
                        completed_at=CASE WHEN ?='completed' THEN ? ELSE completed_at END
                    WHERE id=?
                """, (status, progress['completed'], progress['success'], progress['failed'],
                      status, datetime.now().isoformat(), self.task_id))
            else:
                cursor.execute("UPDATE collection_tasks SET status=? WHERE id=?", 
                             (status, self.task_id))
            conn.commit()
            conn.close()
        except Exception as e:
            self._log('WARNING', f'更新任务状态失败: {e}')

    def detect_platform(self, url, platform_name):
        """
        检测平台可用性及功能特征
        返回: (status, details_dict)
        """
        result = {
            'status': 'unknown',
            'status_detail': '',
            'response_time': 0,
            'http_status': None,
            'has_https': 0,
            'has_search': 0,
            'has_download': 0,
            'has_api': 0,
            'has_register': 0,
            'has_preview': 0,
            'has_visualization': 0,
            'has_update_info': 0,
            'has_metadata': 0,
            'has_feedback': 0,
            'has_bulk_download': 0,
            'dataset_count': 0,
            'app_count': 0,
            'format_types': '[]',
            'raw_html': '',
            'error_message': ''
        }
        
        if not url or not url.startswith('http'):
            result['status'] = 'unavailable'
            result['status_detail'] = 'URL无效或为空'
            return result
            
        # 检测HTTPS
        result['has_https'] = 1 if url.startswith('https://') else 0
        
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=15, allow_redirects=True, verify=False)
            result['response_time'] = round(time.time() - start_time, 2)
            result['http_status'] = response.status_code
            
            # 根据HTTP状态判断
            if response.status_code == 200:
                result['status'] = 'available'
                result['status_detail'] = '平台可访问'
                self._parse_page_content(result, response.text)
                        
            elif response.status_code in [301, 302, 307, 308]:
                result['status'] = 'redirect'
                result['status_detail'] = f'重定向到 {response.headers.get("Location", "未知")}'
            elif response.status_code == 403:
                result['status'] = 'unavailable'
                result['status_detail'] = '访问被拒绝(403)'
            elif response.status_code == 404:
                result['status'] = 'unavailable'
                result['status_detail'] = '页面不存在(404)'
            elif response.status_code >= 500:
                result['status'] = 'unavailable'
                result['status_detail'] = f'服务器错误({response.status_code})'
            else:
                result['status'] = 'unavailable'
                result['status_detail'] = f'HTTP状态码: {response.status_code}'
                
        except requests.exceptions.Timeout:
            result['status'] = 'timeout'
            result['status_detail'] = '请求超时(>15秒)'
            result['error_message'] = 'Timeout'
        except requests.exceptions.ConnectionError as e:
            result['status'] = 'unavailable'
            result['status_detail'] = f'连接错误: {str(e)[:50]}'
            result['error_message'] = str(e)[:200]
        except Exception as e:
            result['status'] = 'error'
            result['status_detail'] = f'异常: {str(e)[:100]}'
            result['error_message'] = str(e)[:200]
        
        # 如果requests失败，尝试Playwright备用采集（SSL错误、反爬、连接错误）
        if result['status'] in ['unavailable', 'error', 'timeout'] and result['error_message']:
            self._log('INFO', f'{platform_name} requests采集失败，尝试Playwright备用: {result["status_detail"]}')
            pw_result = self._detect_with_playwright(url, platform_name)
            if pw_result['status'] == 'available':
                self._log('INFO', f'{platform_name} Playwright采集成功')
                return pw_result
            else:
                self._log('INFO', f'{platform_name} Playwright也失败: {pw_result["status_detail"]}')
        
        return result
    
    def _detect_with_playwright(self, url, platform_name):
        """使用Playwright浏览器自动化进行备用采集，应对SSL错误和反爬"""
        result = {
            'status': 'unknown',
            'status_detail': '',
            'response_time': 0,
            'http_status': None,
            'has_https': 1 if url.startswith('https://') else 0,
            'has_search': 0, 'has_download': 0, 'has_api': 0,
            'has_register': 0, 'has_preview': 0, 'has_visualization': 0,
            'has_update_info': 0, 'has_metadata': 0, 'has_feedback': 0,
            'has_bulk_download': 0,
            'dataset_count': 0, 'app_count': 0,
            'format_types': '[]', 'raw_html': '', 'error_message': ''
        }
        try:
            from playwright.sync_api import sync_playwright
            start_time = time.time()
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                page = context.new_page()
                page.goto(url, wait_until='domcontentloaded', timeout=30000)
                # 等待JS执行
                time.sleep(3)
                html = page.content()
                title = page.title()
                browser.close()
            
            result['response_time'] = round(time.time() - start_time, 2)
            result['http_status'] = 200
            
            # 判断是否为有效页面（非空、非拦截页）
            if len(html) < 200 or title == '' or '$_ts' in html[:500]:
                result['status'] = 'unavailable'
                result['status_detail'] = 'Playwright: 页面为空或被拦截'
                return result
            
            result['status'] = 'available'
            result['status_detail'] = f'平台可访问(Playwright) - {title[:30]}'
            self._parse_page_content(result, html)
            
        except Exception as e:
            result['status'] = 'error'
            result['status_detail'] = f'Playwright异常: {str(e)[:80]}'
            result['error_message'] = str(e)[:200]
        
        return result
    
    def _parse_page_content(self, result, html_text):
        """解析页面内容，提取功能特征和数据指标
        增强版：支持更多数据集计数模式、DOM元素解析、Script变量提取
        """
        soup = BeautifulSoup(html_text, 'html.parser')
        text = soup.get_text().lower()
        html_str = html_text.lower()
        
        # 保存HTML片段（前5000字符）
        result['raw_html'] = html_text[:5000]
        
        # 功能检测
        result['has_search'] = 1 if any(k in html_str for k in ['search', '搜索', 'query', 'q=']) else 0
        result['has_download'] = 1 if any(k in html_str for k in ['download', '下载', 'export', '导出']) else 0
        result['has_api'] = 1 if any(k in html_str for k in ['api', '接口', 'developer', '开发者']) else 0
        result['has_register'] = 1 if any(k in html_str for k in ['register', '注册', 'signup', '登录']) else 0
        result['has_preview'] = 1 if any(k in html_str for k in ['preview', '预览', '查看', 'view']) else 0
        result['has_visualization'] = 1 if any(k in html_str for k in ['chart', '可视化', '图表', 'map', '地图', 'visual']) else 0
        result['has_update_info'] = 1 if any(k in html_str for k in ['update', '更新', 'modified', '发布']) else 0
        result['has_metadata'] = 1 if any(k in html_str for k in ['metadata', '元数据', 'description', '描述']) else 0
        result['has_feedback'] = 1 if any(k in html_str for k in ['feedback', '反馈', 'contact', '联系', 'suggest']) else 0
        result['has_bulk_download'] = 1 if any(k in html_str for k in ['bulk', '批量', 'batch', 'zip']) else 0
        
        # ========== 数据集数量提取（增强版）==========
        dataset_count = 0
        
        # 策略1: 文本正则匹配（扩展模式）
        count_patterns = [
            # 标准模式
            r'(\d+)\s*个数据集',
            r'(\d+)\s*条数据',
            r'数据集[:：]\s*(\d+)',
            r'共\s*(\d+)\s*条',
            r'(\d+)\s*datasets?',
            r'total[:：]\s*(\d+)',
            # 山东模式: "现已开放58个部门，63,656个数据目录"
            r'(?:现已开放|已开放|开放)\s*[\d,]+\s*个[^，]*，\s*([\d,]+)\s*个(?:数据目录|目录)',
            # 四川模式: "9115个目录数量"
            r'([\d,]+)\s*个(?:数据)?目录',
            r'目录数量[:：]?\s*([\d,]+)',
            # 通用资源数
            r'([\d,]+)\s*个资源',
            r'资源数量[:：]?\s*([\d,]+)',
            # 数据总量
            r'数据总量[:：]?\s*([\d,]+)',
            r'([\d,]+)\s*(?:万|亿)?条数据',
            # 部门数+数据集数组合
            r'(?:部门|单位)[^\d]*(\d+)\s*个[^，]*数据集[^\d]*(\d+)',
        ]
        for pattern in count_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # 提取数字，去掉逗号
                num_str = match.group(1).replace(',', '')
                try:
                    val = int(num_str)
                    if 0 < val < 10000000:  # 合理范围过滤
                        dataset_count = val
                        break
                except ValueError:
                    continue
        
        # 策略2: 特定DOM元素解析
        if dataset_count == 0:
            # 搜索class/id包含count/num/total的元素
            selector_keywords = ['count', 'num', 'total', 'sum', 'amount', 'catalog', 'dataset']
            for keyword in selector_keywords:
                # class匹配
                for elem in soup.find_all(attrs={"class": re.compile(keyword, re.I)}):
                    elem_text = elem.get_text(strip=True)
                    # 提取纯数字
                    num_match = re.search(r'([\d,]+)', elem_text)
                    if num_match:
                        try:
                            val = int(num_match.group(1).replace(',', ''))
                            if 10 < val < 10000000:
                                dataset_count = val
                                break
                        except:
                            pass
                if dataset_count > 0:
                    break
                
                # id匹配
                for elem in soup.find_all(attrs={"id": re.compile(keyword, re.I)}):
                    elem_text = elem.get_text(strip=True)
                    num_match = re.search(r'([\d,]+)', elem_text)
                    if num_match:
                        try:
                            val = int(num_match.group(1).replace(',', ''))
                            if 10 < val < 10000000:
                                dataset_count = val
                                break
                        except:
                            pass
                if dataset_count > 0:
                    break
        
        # 策略3: Script变量提取
        if dataset_count == 0:
            for script in soup.find_all('script'):
                if script.string:
                    js_patterns = [
                        r'(?:datasetCount|totalCount|dataCount|catalogCount|resourceCount)\s*[:=]\s*(\d+)',
                        r'["\']?total["\']?\s*[:：]\s*(\d+)',
                        r'["\']?count["\']?\s*[:：]\s*(\d+)',
                    ]
                    for pattern in js_patterns:
                        match = re.search(pattern, script.string, re.I)
                        if match:
                            try:
                                val = int(match.group(1))
                                if 0 < val < 10000000:
                                    dataset_count = val
                                    break
                            except:
                                pass
                    if dataset_count > 0:
                        break
        
        # 策略4: 特定ID搜索（基于已知平台模式）
        if dataset_count == 0:
            known_ids = ['cataNums', 'resNums', 'dataNums', 'statistics-openDataCount', 
                        'statistics-openCatalogCount', 'dataset-count', 'catalog-count']
            for elem_id in known_ids:
                elem = soup.find(id=elem_id)
                if elem:
                    elem_text = elem.get_text(strip=True)
                    num_match = re.search(r'([\d,\.]+)', elem_text)
                    if num_match:
                        try:
                            val = int(float(num_match.group(1).replace(',', '')))
                            if 0 <= val < 10000000:
                                dataset_count = val
                                break
                        except:
                            pass
        
        result['dataset_count'] = dataset_count
        
        # 数据格式检测
        formats = []
        format_keywords = {
            'csv': ['csv'],
            'json': ['json'],
            'xml': ['xml'],
            'excel': ['xlsx', 'xls', 'excel'],
            'pdf': ['pdf'],
            'api': ['api', '接口'],
            'rdf': ['rdf', 'linked data'],
        }
        for fmt, keywords in format_keywords.items():
            if any(k in html_str for k in keywords):
                formats.append(fmt)
        result['format_types'] = json.dumps(formats)
        
        # 应用成果数（增强提取）
        app_count = 0
        app_patterns = [
            r'(\d+)\s*个应用',
            r'(\d+)\s*款应用',
            r'应用[:：]\s*(\d+)',
            r'创新应用[:：]?\s*(\d+)',
            r'([\d,]+)\s*个(?:创新)?应用',
        ]
        for pattern in app_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    val = int(match.group(1).replace(',', ''))
                    if 0 <= val < 10000:
                        app_count = val
                        break
                except:
                    continue
        result['app_count'] = app_count
        
    def calculate_4e_scores(self, details):
        """
        基于4E框架计算综合评分
        C1: 供给保障 (Economy) - 数据集数量、格式多样性、API、批量下载
        C2: 平台服务 (Efficiency) - 响应时间、HTTPS、搜索、下载、可视化
        C3: 数据质量 (Quality) - 更新信息、元数据、反馈渠道
        C4: 利用效果 (Effectiveness) - 注册、预览、应用成果
        """
        scores = {'C1': 0, 'C2': 0, 'C3': 0, 'C4': 0}
        
        if details['status'] != 'available':
            return scores
            
        # C1: 供给保障 (权重: 数据集数量40%, 格式20%, API20%, 批量下载20%)
        dataset_score = min(details['dataset_count'] / 1000, 1.0) if details['dataset_count'] > 0 else 0
        formats = json.loads(details.get('format_types', '[]'))
        format_score = min(len(formats) / 5, 1.0)
        scores['C1'] = (dataset_score * 0.4 + format_score * 0.2 + 
                       details['has_api'] * 0.2 + details['has_bulk_download'] * 0.2)
        
        # C2: 平台服务 (权重: 响应时间20%, HTTPS10%, 搜索20%, 下载20%, 可视化20%, API10%)
        response_score = 1.0 if details['response_time'] < 3 else (0.5 if details['response_time'] < 10 else 0)
        scores['C2'] = (response_score * 0.2 + details['has_https'] * 0.1 +
                       details['has_search'] * 0.2 + details['has_download'] * 0.2 +
                       details['has_visualization'] * 0.2 + details['has_api'] * 0.1)
        
        # C3: 数据质量 (权重: 更新信息40%, 元数据30%, 反馈渠道30%)
        scores['C3'] = (details['has_update_info'] * 0.4 + details['has_metadata'] * 0.3 +
                       details['has_feedback'] * 0.3)
        
        # C4: 利用效果 (权重: 注册30%, 预览30%, 应用成果40%)
        app_score = min(details['app_count'] / 50, 1.0) if details['app_count'] > 0 else 0
        scores['C4'] = (details['has_register'] * 0.3 + details['has_preview'] * 0.3 + app_score * 0.4)
        
        return scores
        
    def collect_single(self, platform):
        """
        采集单个平台
        platform: dict with keys: id, code, name, tier, region, url, url_pattern
        """
        platform_id = platform['id']
        code = platform['code']
        name = platform['name']
        tier = platform['tier']
        region = platform['region']
        url = platform['url'] or platform['url_pattern']
        
        self.stats['current_platform'] = name
        self._log('INFO', f'开始采集: {name} ({url})', code)
        
        # 执行检测
        details = self.detect_platform(url, name)
        
        # 计算4E得分
        scores = self.calculate_4e_scores(details)
        overall = round(np.mean(list(scores.values())), 3) if details['status'] == 'available' else 0
        
        # 保存到数据库
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO collection_records 
                (task_id, platform_id, platform_code, platform_name, tier, region, status, status_detail,
                 dataset_count, format_types, has_api, has_bulk_download,
                 response_time, has_https, has_search, has_download, has_visualization,
                 has_update_info, has_metadata, has_feedback,
                 has_register, has_preview, app_count,
                 score_c1, score_c2, score_c3, score_c4, overall_score,
                 raw_html_snippet, http_status, error_message, collected_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.task_id, platform_id, code, name, tier, region,
                details['status'], details['status_detail'],
                details['dataset_count'], details['format_types'], details['has_api'], details['has_bulk_download'],
                details['response_time'], details['has_https'], details['has_search'], details['has_download'], details['has_visualization'],
                details['has_update_info'], details['has_metadata'], details['has_feedback'],
                details['has_register'], details['has_preview'], details['app_count'],
                round(scores['C1'], 3), round(scores['C2'], 3), round(scores['C3'], 3), round(scores['C4'], 3), overall,
                details['raw_html'], details['http_status'], details['error_message'],
                datetime.now().isoformat()
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            self._log('ERROR', f'保存采集结果失败: {e}', code)
        
        # 更新统计
        self.stats['completed'] += 1
        if details['status'] == 'available':
            self.stats['success'] += 1
        else:
            self.stats['failed'] += 1
            
        self._log('INFO', f'采集完成: {name} - 状态:{details["status"]}, 综合得分:{overall}', code)
        
        # 发送进度到队列
        self.progress_queue.put({
            'platform': name,
            'status': details['status'],
            'overall_score': overall,
            'completed': self.stats['completed'],
            'total': self.stats['total'],
            'success': self.stats['success'],
            'failed': self.stats['failed']
        })
        
        return details
        
    def run_collection(self, platform_filter=None):
        """
        运行完整采集流程
        platform_filter: 可选过滤条件, 如 {'tier': '省级'} 或 {'region': '华东'}
        """
        self.is_running = True
        self.is_paused = False
        self.stats['start_time'] = datetime.now()
        self._update_task_status('running')
        
        # 获取平台列表
        conn = get_db()
        cursor = conn.cursor()
        query = "SELECT * FROM platforms WHERE 1=1"
        params = []
        if platform_filter:
            for key, value in platform_filter.items():
                query += f" AND {key}=?"
                params.append(value)
        cursor.execute(query, params)
        platforms = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        self.stats['total'] = len(platforms)
        self._update_task_status('running', {'completed': 0, 'success': 0, 'failed': 0})
        
        self._log('INFO', f'采集任务开始: 共{len(platforms)}个平台, 任务ID={self.task_id}')
        
        # 保存初始快照
        self._save_snapshot('start', {
            'total_platforms': len(platforms),
            'platform_list': [{'code': p['code'], 'name': p['name'], 'tier': p['tier']} for p in platforms],
            'config': {'max_workers': self.max_workers, 'delay': self.delay}
        })
        
        # 执行采集
        for i, platform in enumerate(platforms):
            if not self.is_running:
                self._log('INFO', '采集任务被终止')
                break
                
            # 暂停检查
            while self.is_paused:
                time.sleep(1)
                
            self.collect_single(platform)
            
            # 每10个平台保存一次进度快照
            if (i + 1) % 10 == 0:
                self._save_snapshot('progress', {
                    'completed': self.stats['completed'],
                    'success': self.stats['success'],
                    'failed': self.stats['failed'],
                    'current': platform['name']
                })
                self._update_task_status('running', {
                    'completed': self.stats['completed'],
                    'success': self.stats['success'],
                    'failed': self.stats['failed']
                })
            
            # 请求间隔
            if i < len(platforms) - 1:
                time.sleep(self.delay)
        
        # 任务完成
        self.is_running = False
        self._update_task_status('completed', {
            'completed': self.stats['completed'],
            'success': self.stats['success'],
            'failed': self.stats['failed']
        })
        
        # 保存最终快照
        self._save_snapshot('final', {
            'stats': self.stats,
            'duration': str(datetime.now() - self.stats['start_time'])
        })
        
        self._log('INFO', f'采集任务完成: 成功{self.stats["success"]}/{self.stats["total"]}')
        
        return self.stats
        
    def pause(self):
        """暂停采集"""
        self.is_paused = True
        self._update_task_status('paused')
        self._log('INFO', '采集任务已暂停')
        
    def resume(self):
        """恢复采集"""
        self.is_paused = False
        self._update_task_status('running')
        self._log('INFO', '采集任务已恢复')
        
    def stop(self):
        """停止采集"""
        self.is_running = False
        self._update_task_status('stopped')
        self._log('INFO', '采集任务已停止')


def create_collection_task(task_name, task_type='full'):
    """创建新的采集任务"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 统计平台数量
    if task_type == 'full':
        cursor.execute("SELECT COUNT(*) FROM platforms")
    elif task_type == 'provincial':
        cursor.execute("SELECT COUNT(*) FROM platforms WHERE tier='省级'")
    elif task_type == 'subprovincial':
        cursor.execute("SELECT COUNT(*) FROM platforms WHERE tier='副省级/计划单列市'")
    elif task_type == 'prefectural':
        cursor.execute("SELECT COUNT(*) FROM platforms WHERE tier='地级市'")
    else:
        cursor.execute("SELECT COUNT(*) FROM platforms")
        
    total_count = cursor.fetchone()[0]
    
    cursor.execute("""
        INSERT INTO collection_tasks (task_name, task_type, status, total_count, config_json, created_at)
        VALUES (?, ?, 'pending', ?, ?, ?)
    """, (task_name, task_type, total_count, json.dumps({'delay': 2, 'max_workers': 3}), datetime.now().isoformat()))
    
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return task_id


if __name__ == '__main__':
    # 测试运行
    from models import init_db, init_platforms_data
    init_db()
    init_platforms_data()
    
    task_id = create_collection_task('三层架构完整采集测试', 'full')
    print(f"创建任务ID: {task_id}")
    
    engine = CollectorEngine(task_id=task_id, max_workers=3, delay=2)
    stats = engine.run_collection()
    print(f"采集完成: {stats}")
