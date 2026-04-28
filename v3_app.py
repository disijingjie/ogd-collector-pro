"""
OGD-Collector Pro V3 - Flask应用
展示平台规则映射表、采集结果、采集详情
"""

import json
import sqlite3
from datetime import datetime
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# 加载平台规则
with open('v3_platform_rules.json', 'r', encoding='utf-8') as f:
    PLATFORM_RULES = json.load(f)

PLATFORMS = {p['code']: p for p in PLATFORM_RULES['platforms']}

def get_db_connection():
    conn = sqlite3.connect('data/ogd_database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """V3首页 - 采集状态总览"""
    # 加载最新采集结果
    try:
        with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
            collection_results = json.load(f)
    except FileNotFoundError:
        collection_results = []

    # 统计
    total = len(PLATFORMS)
    success = sum(1 for r in collection_results if r['status'] == 'success')
    high_conf = sum(1 for r in collection_results if r.get('confidence') == 'high')
    medium_conf = sum(1 for r in collection_results if r.get('confidence') == 'medium')
    not_found = total - success

    # 构建平台状态列表
    platform_status = []
    for code, platform in PLATFORMS.items():
        # 查找采集结果
        result = next((r for r in collection_results if r['code'] == code), None)
        status_entry = {
            'code': code,
            'name': platform['name'],
            'province': platform['province'],
            'dataset_count': result['dataset_count'] if result else platform['dataset_count']['value'],
            'confidence': result['confidence'] if result else platform['dataset_count']['confidence'],
            'type': platform['dataset_count']['type'],
            'status': result['status'] if result else 'pending',
            'source_url': result['source_url'] if result else platform['dataset_count']['source_url'],
            'collected_at': result.get('collected_at', '') if result else platform.get('dataset_count', {}).get('collected_at', ''),
        }
        platform_status.append(status_entry)

    # 按数据集数量排序
    platform_status.sort(key=lambda x: x['dataset_count'] or 0, reverse=True)

    return render_template('v3_index.html',
                         total=total,
                         success=success,
                         high_conf=high_conf,
                         medium_conf=medium_conf,
                         not_found=not_found,
                         platforms=platform_status,
                         rules_version=PLATFORM_RULES['version'],
                         last_updated=PLATFORM_RULES['last_updated'])

@app.route('/platform/<code>')
def platform_detail(code):
    """平台详情页 - 展示提取规则和采集详情"""
    platform = PLATFORMS.get(code)
    if not platform:
        return "平台未找到", 404

    # 加载采集结果
    try:
        with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
            collection_results = json.load(f)
        result = next((r for r in collection_results if r['code'] == code), None)
    except FileNotFoundError:
        result = None

    return render_template('v3_platform_detail.html',
                         platform=platform,
                         result=result)

@app.route('/rules')
def rules_table():
    """规则映射表页面"""
    return render_template('v3_rules.html', rules=PLATFORM_RULES)

@app.route('/api/platforms')
def api_platforms():
    """API：获取所有平台状态"""
    try:
        with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
            collection_results = json.load(f)
    except FileNotFoundError:
        collection_results = []

    data = []
    for code, platform in PLATFORMS.items():
        result = next((r for r in collection_results if r['code'] == code), None)
        data.append({
            'code': code,
            'name': platform['name'],
            'province': platform['province'],
            'dataset_count': result['dataset_count'] if result else platform['dataset_count']['value'],
            'confidence': result['confidence'] if result else platform['dataset_count']['confidence'],
            'type': platform['dataset_count']['type'],
            'status': result['status'] if result else 'pending',
            'source_url': result['source_url'] if result else platform['dataset_count']['source_url'],
            'extraction_rules': platform['extraction_rules'],
            'urls': platform['urls']
        })

    return jsonify({
        'version': PLATFORM_RULES['version'],
        'last_updated': PLATFORM_RULES['last_updated'],
        'total': len(data),
        'platforms': data
    })

@app.route('/api/collect/<code>', methods=['POST'])
def api_collect(code):
    """API：触发单个平台采集"""
    from v3_collector import extract_dataset_count
    result = extract_dataset_count(code, debug=False)

    # 保存到结果文件
    try:
        with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
    except FileNotFoundError:
        results = []

    # 更新或添加
    existing = next((i for i, r in enumerate(results) if r['code'] == code), None)
    if existing is not None:
        results[existing] = result
    else:
        results.append(result)

    with open('data/v3_collection_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return jsonify(result)

@app.route('/api/stats')
def api_stats():
    """API：获取统计信息"""
    try:
        with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
            collection_results = json.load(f)
    except FileNotFoundError:
        collection_results = []

    total = len(PLATFORMS)
    success = sum(1 for r in collection_results if r['status'] == 'success')
    high_conf = sum(1 for r in collection_results if r.get('confidence') == 'high')

    dataset_counts = [r['dataset_count'] for r in collection_results if r['status'] == 'success' and r['dataset_count']]

    return jsonify({
        'total_platforms': total,
        'success_count': success,
        'success_rate': round(success/total*100, 1) if total > 0 else 0,
        'high_confidence_count': high_conf,
        'total_datasets': sum(dataset_counts) if dataset_counts else 0,
        'avg_datasets': round(sum(dataset_counts)/len(dataset_counts), 0) if dataset_counts else 0,
        'max_platform': max(collection_results, key=lambda x: x['dataset_count'] or 0)['name'] if collection_results else None,
        'last_collection': max((r.get('collected_at', '') for r in collection_results), default=None) if collection_results else None
    })

# ========== 新增可视化页面路由 ==========

@app.route('/charts/topsis')
def charts_topsis():
    """TOPSIS绩效评估可视化页面"""
    return render_template('v3_topsis_chart.html')

@app.route('/charts/dematel')
def charts_dematel():
    """DEMATEL影响因素分析可视化页面"""
    return render_template('v3_dematel_chart.html')

@app.route('/charts/fsqa')
def charts_fsqa():
    """fsQCA组态路径分析可视化页面"""
    return render_template('v3_fsqa_chart.html')

@app.route('/provenance')
def provenance():
    """数据溯源中心页面"""
    return render_template('v3_provenance.html')

@app.route('/dashboard')
def dashboard():
    """采集中心数据看板"""
    return render_template('v3_collection_dashboard.html')

@app.route('/api/csv')
def api_csv():
    """API：下载CSV格式的平台数据"""
    import csv
    import io
    
    try:
        with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
            collection_results = json.load(f)
    except FileNotFoundError:
        collection_results = []
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['省份', '平台名称', '数据集数量', '数据口径', '采集方法', '置信度', '状态', '采集时间', '来源URL'])
    
    for r in collection_results:
        writer.writerow([
            r.get('province', ''),
            r.get('name', ''),
            r.get('dataset_count', ''),
            r.get('type', ''),
            r.get('method', ''),
            r.get('confidence', ''),
            r.get('status', ''),
            r.get('collected_at', ''),
            r.get('source_url', '')
        ])
    
    output.seek(0)
    from flask import Response
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=platforms_data.csv'}
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
