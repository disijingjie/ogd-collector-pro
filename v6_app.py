"""
OGD-Collector Pro V6 - 统一版本Flask应用
整合服务器V3内容和本地修改，单一路径部署
"""

import json
import sqlite3
import re
import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request, send_from_directory, redirect, url_for

app = Flask(__name__, template_folder='templates', static_folder='static')

# 加载平台规则
with open('v3_platform_rules.json', 'r', encoding='utf-8') as f:
    PLATFORM_RULES = json.load(f)

PLATFORMS = {p['code']: p for p in PLATFORM_RULES['platforms']}

def get_db_connection():
    conn = sqlite3.connect('data/ogd_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ========== 首页 ==========
@app.route('/')
def index():
    """V6首页 - 采集状态总览"""
    try:
        with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
            collection_results = json.load(f)
    except FileNotFoundError:
        collection_results = []

    total = len(PLATFORMS)
    success = sum(1 for r in collection_results if r['status'] == 'success')
    high_conf = sum(1 for r in collection_results if r.get('confidence') == 'high')
    medium_conf = sum(1 for r in collection_results if r.get('confidence') == 'medium')
    not_found = total - success

    platform_status = []
    for code, platform in PLATFORMS.items():
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

    platform_status.sort(key=lambda x: x['dataset_count'] or 0, reverse=True)

    return render_template('v6_index.html',
                         total=total,
                         success=success,
                         high_conf=high_conf,
                         medium_conf=medium_conf,
                         not_found=not_found,
                         platforms=platform_status,
                         rules_version=PLATFORM_RULES['version'],
                         last_updated=PLATFORM_RULES['last_updated'])

# ========== 平台详情 ==========
@app.route('/platform/<code>')
def platform_detail(code):
    """平台详情页"""
    platform = PLATFORMS.get(code)
    if not platform:
        return "平台未找到", 404

    try:
        with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
            collection_results = json.load(f)
        result = next((r for r in collection_results if r['code'] == code), None)
    except FileNotFoundError:
        result = None

    return render_template('v6_platform_detail.html',
                         platform=platform,
                         result=result)

# ========== 规则映射表 ==========
@app.route('/rules')
def rules_table():
    """规则映射表页面"""
    return render_template('v6_rules.html', rules=PLATFORM_RULES)

# ========== API接口 ==========
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

    try:
        with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
    except FileNotFoundError:
        results = []

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

# ========== 可视化页面 ==========
@app.route('/charts/topsis')
def charts_topsis():
    """TOPSIS绩效评估可视化"""
    return render_template('v6_topsis_chart.html')

@app.route('/charts/dematel')
def charts_dematel():
    """DEMATEL影响因素分析"""
    return render_template('v6_dematel_chart.html')

@app.route('/charts/fsqa')
def charts_fsqa():
    """fsQCA组态路径分析"""
    return render_template('v6_fsqa_chart.html')

@app.route('/charts/topsis-dea')
def charts_topsis_dea():
    """TOPSIS vs DEA绩效-效率象限图"""
    return render_template('v6_topsis_dea_quadrant.html')

@app.route('/charts/radar')
def charts_radar():
    """省级4E雷达对比器"""
    return render_template('v6_radar_compare.html')

@app.route('/charts/fsqca-explorer')
def charts_fsqca_explorer():
    """fsQCA组态路径浏览器"""
    return render_template('v6_fsqca_explorer.html')

@app.route('/charts/dematel-force')
def charts_dematel_force():
    """DEMATEL因果网络力导向图"""
    return render_template('v6_dematel_force.html')

@app.route('/charts/did')
def charts_did():
    """DID事件研究可视化"""
    return render_template('v6_did_event_study.html')

@app.route('/maturity')
def maturity_model():
    """开放数据成熟度模型交互页"""
    return render_template('v6_maturity_model.html')

@app.route('/strategy')
def strategy_recommender():
    """策略推荐器 - 独立入口"""
    return render_template('v6_maturity_model.html')

@app.route('/value-chain')
def value_chain():
    """4E价值链动画"""
    return render_template('v6_value_chain.html')

@app.route('/international')
def international():
    """国际对比仪表盘"""
    return render_template('v6_international.html')

@app.route('/en')
def en_landing():
    """English Landing Page"""
    return render_template('v6_en_landing.html')

@app.route('/provenance')
def provenance():
    """数据溯源中心"""
    return render_template('v6_provenance.html')

@app.route('/dashboard')
def dashboard():
    """采集中心数据看板"""
    return render_template('v6_collection.html')

@app.route('/api/csv')
def api_csv():
    """API：下载CSV"""
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

@app.route('/api/collection-batches')
def api_collection_batches():
    """API: 采集批次数据"""
    try:
        with open('data/collection_batches.json', 'r', encoding='utf-8') as f:
            batches = json.load(f)
    except FileNotFoundError:
        batches = []
    return jsonify(batches)

# ========== 分析数据下载API ==========
@app.route('/api/analysis/topsis')
def api_analysis_topsis():
    """API: TOPSIS综合绩效评估数据（JSON/CSV）"""
    from flask import Response
    topsis_data = [
        {"rank":1,"province":"浙江","ci":0.778,"grade":"A","level":"优秀","region":"东部","e1":0.82,"e2":0.78,"e3":0.90,"e4":0.85,"e5":0.80,"type":"标杆型"},
        {"rank":2,"province":"广东","ci":0.754,"grade":"A","level":"优秀","region":"东部","e1":0.88,"e2":0.56,"e3":0.88,"e4":0.21,"e5":0.70,"type":"追赶型"},
        {"rank":3,"province":"上海","ci":0.726,"grade":"A","level":"优秀","region":"东部","e1":0.60,"e2":0.33,"e3":0.88,"e4":0.00,"e5":0.70,"type":"滞后型"},
        {"rank":4,"province":"北京","ci":0.706,"grade":"A","level":"优秀","region":"东部","e1":0.75,"e2":0.77,"e3":1.00,"e4":0.42,"e5":1.00,"type":"潜力型"},
        {"rank":5,"province":"山东","ci":0.658,"grade":"B+","level":"优秀","region":"东部","e1":0.88,"e2":0.77,"e3":1.00,"e4":1.00,"e5":1.00,"type":"标杆型"},
        {"rank":6,"province":"四川","ci":0.607,"grade":"B+","level":"优秀","region":"西部","e1":0.86,"e2":0.80,"e3":1.00,"e4":0.42,"e5":1.00,"type":"潜力型"},
        {"rank":7,"province":"江苏","ci":0.592,"grade":"B","level":"良好","region":"东部","e1":0.55,"e2":0.82,"e3":0.88,"e4":0.21,"e5":0.70,"type":"追赶型"},
        {"rank":8,"province":"福建","ci":0.552,"grade":"B","level":"良好","region":"东部","e1":0.58,"e2":0.26,"e3":0.88,"e4":0.21,"e5":0.70,"type":"滞后型"},
        {"rank":9,"province":"贵州","ci":0.539,"grade":"B","level":"良好","region":"西部","e1":0.64,"e2":0.36,"e3":0.88,"e4":0.21,"e5":0.70,"type":"滞后型"},
        {"rank":10,"province":"陕西","ci":0.524,"grade":"B","level":"良好","region":"西部","e1":0.52,"e2":0.55,"e3":0.75,"e4":0.30,"e5":0.60,"type":"追赶型"},
        {"rank":11,"province":"湖南","ci":0.505,"grade":"B","level":"良好","region":"中部","e1":0.55,"e2":0.87,"e3":1.00,"e4":0.42,"e5":1.00,"type":"潜力型"},
        {"rank":12,"province":"湖北","ci":0.490,"grade":"B-","level":"良好","region":"中部","e1":0.66,"e2":0.61,"e3":0.88,"e4":0.21,"e5":0.70,"type":"滞后型"},
        {"rank":13,"province":"安徽","ci":0.470,"grade":"B-","level":"良好","region":"中部","e1":0.08,"e2":0.26,"e3":0.88,"e4":0.00,"e5":0.40,"type":"困境型"},
        {"rank":14,"province":"河南","ci":0.452,"grade":"B-","level":"良好","region":"中部","e1":0.60,"e2":0.72,"e3":0.88,"e4":0.42,"e5":0.70,"type":"潜力型"},
        {"rank":15,"province":"江西","ci":0.432,"grade":"C+","level":"中等","region":"中部","e1":0.40,"e2":0.49,"e3":0.88,"e4":0.21,"e5":0.70,"type":"滞后型"},
        {"rank":16,"province":"重庆","ci":0.412,"grade":"C+","level":"中等","region":"西部","e1":0.76,"e2":0.56,"e3":0.88,"e4":0.21,"e5":0.70,"type":"追赶型"},
        {"rank":17,"province":"辽宁","ci":0.395,"grade":"C","level":"中等","region":"东北","e1":0.76,"e2":0.87,"e3":1.00,"e4":0.42,"e5":1.00,"type":"潜力型"},
        {"rank":18,"province":"云南","ci":0.377,"grade":"C","level":"中等","region":"西部","e1":0.35,"e2":0.39,"e3":0.88,"e4":0.21,"e5":0.70,"type":"滞后型"},
        {"rank":19,"province":"广西","ci":0.357,"grade":"C","level":"中等","region":"西部","e1":0.72,"e2":0.87,"e3":1.00,"e4":0.42,"e5":1.00,"type":"潜力型"},
        {"rank":20,"province":"海南","ci":0.339,"grade":"C","level":"中等","region":"东部","e1":0.78,"e2":0.75,"e3":1.00,"e4":0.42,"e5":1.00,"type":"潜力型"},
        {"rank":21,"province":"河北","ci":0.319,"grade":"C-","level":"中等","region":"东部","e1":0.45,"e2":0.38,"e3":0.70,"e4":0.15,"e5":0.55,"type":"追赶型"},
        {"rank":22,"province":"天津","ci":0.301,"grade":"C-","level":"中等","region":"东部","e1":0.59,"e2":0.64,"e3":0.88,"e4":0.42,"e5":0.70,"type":"追赶型"},
        {"rank":23,"province":"吉林","ci":0.284,"grade":"D+","level":"中等","region":"东北","e1":0.31,"e2":0.49,"e3":0.88,"e4":0.21,"e5":0.70,"type":"滞后型"},
        {"rank":24,"province":"黑龙江","ci":0.264,"grade":"D+","level":"较差","region":"东北","e1":0.28,"e2":0.35,"e3":0.65,"e4":0.10,"e5":0.50,"type":"追赶型"},
        {"rank":25,"province":"内蒙古","ci":0.244,"grade":"D","level":"较差","region":"西部","e1":0.42,"e2":0.87,"e3":1.00,"e4":0.42,"e5":1.00,"type":"潜力型"},
        {"rank":26,"province":"新疆","ci":0.224,"grade":"D","level":"较差","region":"西部","e1":0.25,"e2":0.30,"e3":0.55,"e4":0.08,"e5":0.40,"type":"滞后型"},
        {"rank":27,"province":"甘肃","ci":0.204,"grade":"D","level":"较差","region":"西部","e1":0.22,"e2":0.28,"e3":0.50,"e4":0.05,"e5":0.35,"type":"滞后型"},
        {"rank":28,"province":"宁夏","ci":0.184,"grade":"D","level":"较差","region":"西部","e1":0.20,"e2":0.25,"e3":0.45,"e4":0.05,"e5":0.30,"type":"滞后型"},
        {"rank":29,"province":"青海","ci":0.164,"grade":"D","level":"较差","region":"西部","e1":0.18,"e2":0.22,"e3":0.40,"e4":0.03,"e5":0.25,"type":"困境型"},
        {"rank":30,"province":"西藏","ci":0.141,"grade":"D","level":"极差","region":"西部","e1":0.12,"e2":0.15,"e3":0.30,"e4":0.02,"e5":0.15,"type":"困境型"}
    ]
    fmt = request.args.get('format', 'json')
    if fmt == 'csv':
        import csv, io
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['排名','省份','TOPSIS Ci','等级','层级','区域','E1供应保障','E2平台服务','E3数据质量','E4利用效果','E5公平性','5类分型'])
        for d in topsis_data:
            writer.writerow([d['rank'],d['province'],d['ci'],d['grade'],d['level'],d['region'],d['e1'],d['e2'],d['e3'],d['e4'],d['e5'],d['type']])
        output.seek(0)
        return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition':'attachment; filename=topsis_evaluation.csv'})
    return jsonify(topsis_data)

@app.route('/api/analysis/fsqca')
def api_analysis_fsqca():
    """API: fsQCA组态分析数据"""
    fsqca_data = {
        "necessary_conditions": [
            {"dimension":"E2平台服务","consistency":1.00,"coverage":0.82,"necessity":"必要"},
            {"dimension":"E3数据质量","consistency":1.00,"coverage":0.79,"necessity":"必要"},
            {"dimension":"E4利用效果","consistency":1.00,"coverage":0.76,"necessity":"必要"}
        ],
        "sufficient_configurations": [
            {"id":"H1","name":"技术驱动型","conditions":"E1×E2×E3","raw_coverage":0.81,"raw_consistency":0.94,"unique_coverage":0.42,"provinces":["浙江","上海","北京","广东","山东","四川"]},
            {"id":"H2","name":"效率-区域型","conditions":"E3×技术支撑×区域优势","raw_coverage":0.19,"raw_consistency":0.91,"unique_coverage":0.08,"provinces":["广东","山东","江苏"]},
            {"id":"H3","name":"生态-协同型","conditions":"E1×E4×技术支撑","raw_coverage":0.15,"raw_consistency":0.89,"unique_coverage":0.05,"provinces":["江苏","福建","贵州"]}
        ],
        "solution_coverage": 0.88,
        "solution_consistency": 0.92
    }
    return jsonify(fsqca_data)

@app.route('/api/analysis/dematel')
def api_analysis_dematel():
    """API: DEMATEL因果分析数据"""
    dematel_data = {
        "factors": [
            {"id":"PL","name":"政策法规","centrality":2.856,"causality":0.432,"type":"cause"},
            {"id":"PC","name":"平台能力","centrality":3.142,"causality":0.287,"type":"cause"},
            {"id":"E1","name":"供应保障","centrality":2.634,"causality":-0.156,"type":"effect"},
            {"id":"E2","name":"平台服务","centrality":3.021,"causality":0.098,"type":"cause"},
            {"id":"E3","name":"数据质量","centrality":2.945,"causality":-0.089,"type":"effect"},
            {"id":"E4","name":"利用效果","centrality":2.789,"causality":-0.213,"type":"effect"},
            {"id":"OP","name":"运营保障","centrality":2.567,"causality":0.178,"type":"cause"}
        ],
        "transmission_paths": [
            {"path":"政策法规→平台能力→数据质量→利用效果","strength":0.856,"type":"政策驱动型"},
            {"path":"平台服务→数据质量→利用效果","strength":0.723,"type":"服务提升型"},
            {"path":"运营保障→供应保障→利用效果","strength":0.612,"type":"基础保障型"}
        ],
        "influence_matrix": {
            "rows": ["PL","PC","E1","E2","E3","E4","OP"],
            "columns": ["PL","PC","E1","E2","E3","E4","OP"],
            "values": [
                [0,0.456,0.234,0.189,0.156,0.089,0.312],
                [0.123,0,0.378,0.267,0.312,0.145,0.189],
                [0.089,0.145,0,0.123,0.267,0.334,0.078],
                [0.067,0.234,0.189,0,0.423,0.156,0.112],
                [0.045,0.089,0.312,0.145,0,0.278,0.067],
                [0.034,0.056,0.123,0.089,0.234,0,0.045],
                [0.189,0.156,0.289,0.134,0.178,0.112,0]
            ]
        }
    }
    return jsonify(dematel_data)

@app.route('/api/analysis/did')
def api_analysis_did():
    """API: 多期DID政策效应数据"""
    did_data = {
        "baseline_effect": {"coefficient":0.043,"std_error":0.012,"t_value":3.58,"p_value":0.001,"significance":"***"},
        "event_study": [
            {"period":"T-3","coefficient":-0.008,"ci_lower":-0.024,"ci_upper":0.008,"significant":False},
            {"period":"T-2","coefficient":-0.005,"ci_lower":-0.019,"ci_upper":0.009,"significant":False},
            {"period":"T-1","coefficient":0.002,"ci_lower":-0.012,"ci_upper":0.016,"significant":False},
            {"period":"T","coefficient":0.018,"ci_lower":0.003,"ci_upper":0.033,"significant":True},
            {"period":"T+1","coefficient":0.043,"ci_lower":0.026,"ci_upper":0.060,"significant":True},
            {"period":"T+2","coefficient":0.052,"ci_lower":0.032,"ci_upper":0.072,"significant":True},
            {"period":"T+3","coefficient":0.048,"ci_lower":0.025,"ci_upper":0.071,"significant":True}
        ],
        "dimensional_heterogeneity": [
            {"dimension":"E1供应保障","beta":0.038,"p":0.008,"significant":True},
            {"dimension":"E2平台服务","beta":0.052,"p":0.003,"significant":True},
            {"dimension":"E3数据质量","beta":0.029,"p":0.042,"significant":True},
            {"dimension":"E4利用效果","beta":0.061,"p":0.001,"significant":True},
            {"dimension":"E5公平性","beta":0.015,"p":0.234,"significant":False}
        ],
        "robustness": [
            {"method":"PSM-DID","coefficient":0.039,"p":0.005},
            {"method":"替换因变量","coefficient":0.041,"p":0.008},
            {"method":"排除直辖市","coefficient":0.044,"p":0.003},
            {"method":"控制省级特征","coefficient":0.037,"p":0.012},
            {"method":"平行趋势检验","result":"通过","p":0.156}
        ]
    }
    return jsonify(did_data)

@app.route('/api/collection-results')
def api_collection_results():
    """API: 23平台采集结果"""
    try:
        with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
    except FileNotFoundError:
        results = []
    return jsonify(results)

@app.route('/api/literature-notes')
def api_literature_notes():
    """API: 200篇文献精读笔记"""
    try:
        with open('data/literature_notes.json', 'r', encoding='utf-8') as f:
            notes = json.load(f)
    except FileNotFoundError:
        notes = []
    return jsonify(notes)

@app.route('/api/literature-note/<int:n>')
def api_literature_note_detail(n):
    """API: 单篇文献精读笔记详情"""
    try:
        with open('data/literature_notes.json', 'r', encoding='utf-8') as f:
            notes = json.load(f)
        note = next((x for x in notes if x['n'] == n), None)
    except FileNotFoundError:
        note = None
    if note is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(note)

@app.route('/api/literature-filter-log')
def api_literature_filter_log():
    """API: 文献漏斗筛选日志"""
    try:
        with open('data/literature_filter_log.json', 'r', encoding='utf-8-sig') as f:
            log = json.load(f)
    except FileNotFoundError:
        log = {}
    return jsonify(log)

@app.route('/api/literature-db')
def api_literature_db():
    """API: 200篇文献数据库"""
    try:
        with open('data/literature_db.json', 'r', encoding='utf-8-sig') as f:
            db = json.load(f)
    except FileNotFoundError:
        db = []
    return jsonify(db)

@app.route('/api/external-sources')
def api_external_sources():
    """API: 外部来源索引（政策文件/报告/网站/技术文档）"""
    try:
        with open('data/external_sources.json', 'r', encoding='utf-8') as f:
            sources = json.load(f)
    except FileNotFoundError:
        sources = {}
    return jsonify(sources)

@app.route('/api/literature-categories')
def api_literature_categories():
    """API: 文献分类索引"""
    try:
        with open('data/literature_categories.json', 'r', encoding='utf-8') as f:
            cats = json.load(f)
    except FileNotFoundError:
        cats = {}
    return jsonify(cats)

@app.route('/api/fulltext-search')
def api_fulltext_search():
    """API: 全文检索"""
    query = request.args.get('q', '').lower()
    try:
        with open('data/fulltext_index.json', 'r', encoding='utf-8') as f:
            idx = json.load(f)
    except FileNotFoundError:
        return jsonify({"results": [], "total": 0})
    if not query:
        return jsonify({"stats": idx.get('stats', {}), "results": []})
    results = []
    for item in idx.get('search_index', []):
        if query in item.get('text', ''):
            results.append(item['n'])
    return jsonify({"query": query, "results": results, "total": len(results)})

@app.route('/api/chapter-references')
def api_chapter_references():
    """API: 章节-文献引用映射"""
    try:
        with open('data/chapter_references.json', 'r', encoding='utf-8') as f:
            refs = json.load(f)
    except FileNotFoundError:
        refs = {}
    return jsonify(refs)

@app.route('/api/thesis-claims')
def api_thesis_claims():
    """API: 论文声明-文献引用映射"""
    try:
        with open('data/thesis_claims.json', 'r', encoding='utf-8') as f:
            claims = json.load(f)
    except FileNotFoundError:
        claims = {}
    return jsonify(claims)

# ========== 采集状态实时API ==========
@app.route('/api/collection/status')
def api_collection_status():
    """采集状态API - 前端定时轮询"""
    try:
        with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
    except FileNotFoundError:
        results = []

    # 从collection_tasks表获取最近5次任务
    tasks = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, task_name, status, total_count, success_count, fail_count, started_at, completed_at FROM collection_tasks ORDER BY id DESC LIMIT 5')
        tasks = [dict(row) for row in cursor.fetchall()]
        conn.close()
    except Exception:
        pass

    total = len(PLATFORMS)
    success = sum(1 for r in results if r.get('status') == 'success')

    return jsonify({
        'platforms_total': total,
        'platforms_success': success,
        'platforms_failed': total - success,
        'last_collection': results[0].get('collected_at', '') if results else '',
        'recent_tasks': tasks,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/collection/health')
def api_collection_health():
    """平台健康检查API - 异常报警"""
    try:
        with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
    except FileNotFoundError:
        results = []

    alerts = []
    for r in results:
        code = r.get('code', '')
        count = r.get('dataset_count', 0)
        baseline = PLATFORMS.get(code, {}).get('dataset_count', {}).get('value', 0)
        if baseline and count:
            change = abs(count - baseline) / baseline
            if change > 0.5:
                alerts.append({
                    'code': code,
                    'name': r.get('name', code),
                    'type': 'data_anomaly',
                    'severity': 'high' if change > 0.8 else 'medium',
                    'message': f'数据量突变{change:.0%}（基线{baseline:,}→当前{count:,}）'
                })

    return jsonify({
        'alert_count': len(alerts),
        'alerts': alerts,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/collection/timeline')
def api_collection_timeline():
    """采集时间线API - 最近采集记录"""
    timeline = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, task_name, status, started_at, completed_at, total_count, success_count, fail_count FROM collection_tasks ORDER BY id DESC LIMIT 10')
        timeline = [dict(row) for row in cursor.fetchall()]
        conn.close()
    except Exception:
        pass

    return jsonify({
        'timeline': timeline,
        'timestamp': datetime.now().isoformat()
    })

# ========== 数据-论文互锁API ==========
@app.route('/api/interlock/map')
def api_interlock_map():
    """数据-论文互锁映射API"""
    try:
        with open('data/data_thesis_interlock.json', 'r', encoding='utf-8') as f:
            interlock = json.load(f)
        return jsonify(interlock)
    except FileNotFoundError:
        return jsonify({'error': '互锁映射文件未找到'}), 404

@app.route('/api/interlock/check')
def api_interlock_check():
    """互锁校验API - 检查数据文件修改时间是否晚于论文生成时间"""
    import os
    changes = []
    try:
        with open('data/data_thesis_interlock.json', 'r', encoding='utf-8') as f:
            interlock = json.load(f)
    except FileNotFoundError:
        return jsonify({'status': 'error', 'message': '互锁映射文件未找到'})

    for src_id, src_info in interlock.get('data_sources', {}).items():
        for filepath in src_info.get('files', []):
            if os.path.exists(filepath):
                mtime = os.path.getmtime(filepath)
                changes.append({
                    'source': src_id,
                    'name': src_info['name'],
                    'file': filepath,
                    'modified': datetime.fromtimestamp(mtime).isoformat(),
                    'affects_chapters': src_info.get('affects_chapters', []),
                    'affects_tables': src_info.get('affects_tables', []),
                    'affects_figures': src_info.get('affects_figures', [])
                })

    return jsonify({
        'status': 'ok',
        'total_sources': len(interlock.get('data_sources', {})),
        'data_changes': changes,
        'timestamp': datetime.now().isoformat()
    })

# ========== 参考文献去重校验API ==========
@app.route('/api/literature/dedup')
def api_literature_dedup():
    """参考文献去重校验API"""
    try:
        with open('data/literature_db.json', 'r', encoding='utf-8-sig') as f:
            lit_db = json.load(f)
    except FileNotFoundError:
        return jsonify({'error': '文献库未找到'}), 404

    # 按作者+年份+标题去重检测
    seen = {}
    duplicates = []
    missing_fields = []

    for item in lit_db:
        key = (item.get('a', ''), item.get('y', ''), item.get('t', '')[:20] if item.get('t') else '')
        if key in seen:
            duplicates.append({
                'entry_1': seen[key],
                'entry_2': {'n': item.get('n'), 'a': item.get('a'), 't': item.get('t'), 'y': item.get('y')},
                'reason': 'same_author_year_title'
            })
        else:
            seen[key] = {'n': item.get('n'), 'a': item.get('a'), 't': item.get('t'), 'y': item.get('y')}

        # 缺失字段检查
        missing = []
        for field, label in [('a', '作者'), ('t', '标题'), ('j', '期刊'), ('y', '年份')]:
            if not item.get(field):
                missing.append(label)
        if missing:
            missing_fields.append({'n': item.get('n'), 't': item.get('t'), 'missing': missing})

    # 统计
    cn_count = sum(1 for i in lit_db if i.get('c') == 'cn')
    en_count = sum(1 for i in lit_db if i.get('c') == 'en')
    other = len(lit_db) - cn_count - en_count

    return jsonify({
        'total': len(lit_db),
        'cn_count': cn_count,
        'en_count': en_count,
        'other_count': other,
        'duplicate_count': len(duplicates),
        'duplicates': duplicates[:20],
        'missing_field_count': len(missing_fields),
        'missing_fields': missing_fields[:20],
        'timestamp': datetime.now().isoformat()
    })

# ========== 核心页面路由 ==========
@app.route('/collection')
def collection():
    """采集中心"""
    return render_template('v6_collection.html')

@app.route('/analysis')
def analysis():
    """分析看板"""
    return render_template('v6_analysis.html')

@app.route('/thesis')
def thesis():
    """论文成果"""
    return render_template('v6_thesis.html')

@app.route('/research')
def research():
    """研究拓展"""
    return render_template('v6_research.html')

@app.route('/external-sources')
def external_sources():
    """外部来源索引"""
    return render_template('v6_external_sources.html')

@app.route('/reproduce')
@app.route('/reproduce.html')
def reproduce():
    """数据复现"""
    return render_template('v6_reproduce.html')

@app.route('/credibility')
def credibility():
    """数据可信度中心"""
    return render_template('v6_credibility.html')

@app.route('/caliber')
def caliber():
    """数据口径声明——支撑"数据口径幻觉"概念"""
    return render_template('v6_caliber.html')

@app.route('/map')
def china_map():
    """中国省域绩效热力图"""
    return render_template('v6_map.html')

@app.route('/prisma')
def prisma():
    """文献筛选之路"""
    return render_template('v6_prisma.html')

@app.route('/literature')
def literature():
    """文献数据库"""
    return render_template('v6_literature_db.html')

@app.route('/cnki-results')
def cnki_results():
    """CNKI论文完整信息库"""
    return render_template('v6_cnki_results.html')

# API: CNKI metadata
@app.route('/api/cnki-metadata')
def api_cnki_metadata():
    try:
        with open('data/whu_export/cnki_metadata_merged.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify([])

@app.route('/methodology-paper')
def methodology_paper():
    """方法论小论文"""
    return render_template('v6_methodology_paper.html')

@app.route('/research-journey')
def research_journey():
    """文献研究之路"""
    return render_template('v6_literature_journey.html')

@app.route('/lit-extract')
def lit_extract():
    """文献摘录"""
    return render_template('v6_literature_extract.html')

@app.route('/chapter-synth')
def chapter_synth():
    """章节合成"""
    return render_template('v6_chapter_synth.html')

@app.route('/methodology')
def methodology():
    """研究方法论"""
    return render_template('v6_methodology.html')

@app.route('/references')
def references():
    """外部评估参照"""
    return render_template('v6_references.html')

@app.route('/bibliography')
def bibliography():
    """参考文献库·全文检索"""
    return render_template('v6_bibliography.html')

@app.route('/papers')
def papers():
    """小论文框架"""
    return render_template('v6_papers.html')

# ========== 导师学术思想专题 ==========
@app.route('/chen-chuanfu')
def chen_chuanfu():
    """陈传夫学术思想专题"""
    return render_template('v6_chen_chuanfu.html')

@app.route('/ran-congjing')
def ran_congjing():
    """冉从敬学术思想专题"""
    return render_template('v6_ran_congjing.html')

@app.route('/paper-collection')
def paper_collection():
    """小论文集"""
    return render_template('v6_papers_showcase.html')

# ========== PDF引用文献溯源系统 ==========
@app.route('/pdf-showcase')
def pdf_showcase():
    """PDF引用文献溯源 - 向导师展示所有引用和数据依据"""
    return render_template('v6_pdf_showcase.html')

@app.route('/data/pdf_extracted/<path:filename>')
def serve_pdf_data(filename):
    """提供PDF提取数据文件"""
    return send_from_directory('data/pdf_extracted', filename)

@app.route('/papers/<path:filename>')
def download_paper(filename):
    """下载论文docx文件"""
    return send_from_directory('papers', filename, as_attachment=True)

# 静态数据文件下载
@app.route('/static/data/<path:filename>')
def download_data_file(filename):
    """下载static/data目录下的数据文件"""
    return send_from_directory('static/data', filename, as_attachment=True)

# ========== /v3/ 旧版路径 → V6 重定向（兼容性兜底） ==========
@app.route('/v3/')
def v3_redirect_root():
    return redirect('/', code=301)

@app.route('/v3/collection')
@app.route('/v3/collection.html')
def v3_redirect_collection():
    return redirect('/collection', code=301)

@app.route('/v3/analysis')
@app.route('/v3/analysis.html')
def v3_redirect_analysis():
    return redirect('/analysis', code=301)

@app.route('/v3/thesis')
@app.route('/v3/thesis.html')
def v3_redirect_thesis():
    return redirect('/thesis', code=301)

@app.route('/v3/research')
@app.route('/v3/research.html')
def v3_redirect_research():
    return redirect('/research', code=301)

@app.route('/v3/reproduce')
@app.route('/v3/reproduce.html')
def v3_redirect_reproduce():
    return redirect('/reproduce', code=301)

@app.route('/v3/literature')
@app.route('/v3/literature.html')
def v3_redirect_literature():
    return redirect('/literature', code=301)

@app.route('/v3/papers')
@app.route('/v3/papers.html')
def v3_redirect_papers():
    return redirect('/papers', code=301)

@app.route('/v3/<path:dummy>')
def v3_redirect_catchall(dummy):
    """兜底：所有其他 /v3/* 路径重定向到首页"""
    return redirect('/', code=301)

# ========== 博士论文完整版（隐藏页面） ==========
@app.route('/thesis-full')
def thesis_full():
    """博士论文完整HTML渲染版 - 隐藏页面，用于打印导出"""
    return render_template('v6_thesis_full.html')

@app.route('/api/generate-docx')
def api_generate_docx():
    """一键生成docx"""
    import subprocess, os
    script = os.path.join(os.path.dirname(__file__), '_build_pipeline.py')
    subprocess.run(['python', script], capture_output=True, timeout=120)
    docx_path = os.path.join(os.path.dirname(__file__), 'data', 'thesis_generated.docx')
    if os.path.exists(docx_path):
        return send_from_directory(
            os.path.join(os.path.dirname(__file__), 'data'),
            'thesis_generated.docx',
            as_attachment=True,
            download_name='博士论文_武大标准格式.docx'
        )
    return jsonify({'error': '生成失败'}), 500

# ========== Web基础文件 ==========
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory('static', 'robots.txt', mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap_xml():
    return send_from_directory('static', 'sitemap.xml', mimetype='application/xml')

# ========== 404错误页 ==========
@app.errorhandler(404)
def page_not_found(e):
    return render_template('v6_404.html'), 404

# ========== 论文细读系统 ==========

# 论文MD解析器
THESIS_MD_PATH = 'docs/博士论文_最终定稿版_v23.md'

def _extract_summary(content):
    """从章节内容中提取首段摘要"""
    paragraphs = []
    current_p = []
    for line in content.split('\n'):
        s = line.strip()
        if not s or s.startswith('#') or s.startswith('![') or s.startswith('*数据') or s.startswith('*来源') or s.startswith('**图') or s.startswith('**表'):
            if current_p:
                paragraphs.append(' '.join(current_p))
                current_p = []
            continue
        current_p.append(s)
    if current_p:
        paragraphs.append(' '.join(current_p))
    if paragraphs:
        summary = re.sub(r'\[\^\d+\]', '', paragraphs[0])
        if len(summary) > 260:
            summary = summary[:257] + '...'
        return summary
    return ''

def parse_thesis_md():
    """增强版论文MD解析器：章节摘要、图表索引、引用统计、外部链接"""
    if not os.path.exists(THESIS_MD_PATH):
        return None

    with open(THESIS_MD_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    chapters = []
    current_chapter = None
    current_section = None
    current_content = []
    footnotes = {}
    in_references = False
    ref_buffer = []
    ref_id = None

    ref_counts = {}
    figures_index = []
    tables_index = []
    fig_counter = 0
    tab_counter = 0

    def _flush_chapter():
        nonlocal current_chapter
        if not current_chapter:
            return
        if current_section and current_content:
            current_chapter['sections'].append({
                'title': current_section,
                'content': ''.join(current_content)
            })
        # Build full content for summary extraction
        full = current_chapter['content'] if current_chapter.get('content') else ''
        for sec in current_chapter['sections']:
            full += sec['content']
        current_chapter['summary'] = _extract_summary(full)
        chapters.append(current_chapter)
        current_chapter = None

    for line in lines:
        # 参考文献区域
        if re.match(r'^## (中文文献|英文文献|附录)', line) or re.match(r'^# 参考文献', line):
            in_references = True
            _flush_chapter()
            continue

        if in_references:
            m = re.match(r'^\[(\d+)\]\s+(.*)', line)
            if m:
                if ref_id and ref_buffer:
                    footnotes[ref_id] = ''.join(ref_buffer).strip()
                ref_id = m.group(1)
                ref_buffer = [m.group(2)]
            elif ref_id:
                if line.strip():
                    ref_buffer.append(line)
            continue

        # 章节标题
        ch_match = re.match(r'^# (第.+章.*)', line)
        if ch_match:
            _flush_chapter()
            current_chapter = {
                'title': ch_match.group(1).strip(),
                'level': 1,
                'sections': [],
                'content': '',
                'summary': '',
                'figures': [],
                'tables': []
            }
            current_section = current_chapter['title']
            current_content = []
            continue

        # H3 节标题
        h3_match = re.match(r'^### (.+)', line)
        if h3_match and current_chapter:
            if current_section and current_content:
                current_chapter['sections'].append({
                    'title': current_section,
                    'content': ''.join(current_content)
                })
            current_section = h3_match.group(1).strip()
            current_content = [line]
            continue

        if current_chapter:
            # 统计引用
            for m in re.finditer(r'\[\^(\d+)\]', line):
                rid = m.group(1)
                ref_counts[rid] = ref_counts.get(rid, 0) + 1

            # 收集图片
            img_match = re.search(r'!\[([^\]]*)\]\(([^)]+)\)', line)
            if img_match:
                fig_counter += 1
                cap = img_match.group(1).strip()
                path = img_match.group(2).strip()
                fig_id = f'fig-{fig_counter}'
                fig_info = {'id': fig_id, 'caption': cap, 'path': path, 'global_idx': fig_counter}
                current_chapter['figures'].append(fig_info)
                figures_index.append({
                    'ch_idx': len(chapters),
                    'ch_title': current_chapter['title'],
                    'id': fig_id,
                    'caption': cap,
                    'global_idx': fig_counter
                })

            # 收集表格标题
            tbl_match = re.search(r'\*\*(表\d+-\d+[^\*]*)\*\*', line)
            if tbl_match:
                tab_counter += 1
                cap = tbl_match.group(1).strip()
                tab_id = f'tab-{tab_counter}'
                tab_info = {'id': tab_id, 'caption': cap, 'global_idx': tab_counter}
                current_chapter['tables'].append(tab_info)
                tables_index.append({
                    'ch_idx': len(chapters),
                    'ch_title': current_chapter['title'],
                    'id': tab_id,
                    'caption': cap,
                    'global_idx': tab_counter
                })

            current_content.append(line)

    _flush_chapter()

    if ref_id and ref_buffer:
        footnotes[ref_id] = ''.join(ref_buffer).strip()

    # 提取外部链接
    ref_external = {}
    for rid, text in footnotes.items():
        links = {}
        doi_match = re.search(r'10\.\d{4,}/[^\s,;]+', text)
        if doi_match:
            links['doi'] = f'https://doi.org/{doi_match.group(0)}'
        # CNKI search link for Chinese refs
        if any(k in text for k in ['《', '学报', '研究', '管理', '科学', '图书情报', '情报', '档案', '大学']):
            title_match = re.search(r'《([^》]+)》', text)
            if title_match:
                links['cnki'] = f'https://kns.cnki.net/kns8/defaultresult/index?kw={title_match.group(1)}'
        if '万方' in text:
            links['wanfang'] = 'https://www.wanfangdata.com.cn/'
        if links:
            ref_external[rid] = links

    return {
        'chapters': chapters,
        'references': footnotes,
        'ref_counts': ref_counts,
        'ref_external': ref_external,
        'figures_index': figures_index,
        'tables_index': tables_index,
        'total_chapters': len(chapters),
        'total_references': len(footnotes),
        'total_figures': len(figures_index),
        'total_tables': len(tables_index)
    }

def md_to_html(text, references=None, ctx=None):
    """将论文MD文本转为HTML，处理脚注、图片（带锚点）、表格、表格标题"""
    if references is None:
        references = {}
    if ctx is None:
        ctx = {'fig_counter': [0], 'tab_counter': [0]}

    # 处理引用 [^N] → 上标链接
    def fn_link(m):
        n = m.group(1)
        ref_text = references.get(n, '')
        short_ref = ref_text[:80] + '...' if len(ref_text) > 80 else ref_text
        return f'<sup class="fn-ref"><a href="#ref-{n}" id="fn-{n}" title="{short_ref}" onclick="showFootnote(event,\'{n}\')">[{n}]</a></sup>'
    text = re.sub(r'\[\^(\d+)\]', fn_link, text)

    # 处理图片 ![alt](path) → 带全局ID锚点
    def img_tag(m):
        ctx['fig_counter'][0] += 1
        idx = ctx['fig_counter'][0]
        alt = m.group(1)
        path = m.group(2)
        if not path.startswith('/static/'):
            path = '/static/' + path.replace('static/', '')
        return f'<figure class="thesis-figure" id="fig-{idx}"><img src="{path}" alt="{alt}" loading="lazy"><figcaption>{alt}</figcaption></figure>'
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', img_tag, text)

    # 处理表格标题 **表X-Y ...** → 带锚点
    def tab_caption(m):
        ctx['tab_counter'][0] += 1
        idx = ctx['tab_counter'][0]
        cap = m.group(1)
        return f'<div class="table-caption" id="tab-{idx}"><strong>{cap}</strong></div>'
    text = re.sub(r'\*\*(表\d+-\d+[^\*]*)\*\*', tab_caption, text)

    # 处理粗体 **text**（排除已处理的表格标题）
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

    # 处理标题
    text = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)

    # 处理表格 (简单pipe表格)
    lines = text.split('\n')
    result = []
    in_table = False
    table_lines = []

    for line in lines:
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line.strip())
        else:
            if in_table and table_lines:
                result.append(render_table(table_lines))
                table_lines = []
                in_table = False
            result.append(line)

    if in_table and table_lines:
        result.append(render_table(table_lines))

    text = '\n'.join(result)

    # 段落处理
    text = re.sub(r'\n\n+', '</p><p>', text)
    text = '<p>' + text + '</p>'
    text = text.replace('<p><h', '<h').replace('</h></p>', '</h>')
    text = text.replace('<p><figure', '<figure').replace('</figure></p>', '</figure>')
    text = text.replace('<p><table', '<table').replace('</table></p>', '</table>')
    text = text.replace('<p><div', '<div').replace('</div></p>', '</div>')

    return text

def render_table(lines):
    """渲染markdown表格为HTML"""
    if len(lines) < 2:
        return ''.join(lines)
    
    # 跳过分隔行
    data_lines = [l for l in lines if not re.match(r'^\|[\s\-:|]+\|$', l)]
    if not data_lines:
        return '<table>' + ''.join([f'<tr>{l}</tr>' for l in lines]) + '</table>'
    
    html = '<div class="data-table-wrapper"><table class="data-table">'
    for i, line in enumerate(data_lines):
        cells = [c.strip() for c in line.split('|')[1:-1]]
        tag = 'th' if i == 0 else 'td'
        html += '<tr>' + ''.join([f'<{tag}>{c}</{tag}>' for c in cells]) + '</tr>'
    html += '</table></div>'
    return html

@app.route('/reader')
def thesis_reader():
    """论文细读页——增强版：章节摘要、图表索引、引用追溯"""
    thesis = parse_thesis_md()
    if not thesis:
        return "论文文件未找到", 404

    # 预处理：转换章节内容为HTML（共享全局图/表计数器）
    ctx = {'fig_counter': [0], 'tab_counter': [0]}
    for ch in thesis['chapters']:
        ch['content_html'] = md_to_html(ch['content'], thesis['references'], ctx)
        for sec in ch['sections']:
            sec['content_html'] = md_to_html(sec['content'], thesis['references'], ctx)

    return render_template('v6_thesis_reader.html', thesis=thesis)

@app.route('/api/thesis/structure')
def api_thesis_structure():
    """返回论文结构（含摘要、图表统计）"""
    thesis = parse_thesis_md()
    if not thesis:
        return jsonify({'error': 'not found'}), 404
    structure = []
    for ch in thesis['chapters']:
        structure.append({
            'title': ch['title'],
            'summary': ch.get('summary', ''),
            'figures': len(ch.get('figures', [])),
            'tables': len(ch.get('tables', [])),
            'sections': [s['title'] for s in ch['sections']]
        })
    return jsonify({
        'chapters': structure,
        'total': len(structure),
        'total_figures': thesis.get('total_figures', 0),
        'total_tables': thesis.get('total_tables', 0)
    })

@app.route('/api/thesis/references')
def api_thesis_references():
    """返回引用列表（含被引次数、外部链接）"""
    thesis = parse_thesis_md()
    if not thesis:
        return jsonify({'error': 'not found'}), 404
    refs = []
    for rid in sorted(thesis['references'].keys(), key=int):
        refs.append({
            'id': rid,
            'text': thesis['references'][rid],
            'cited_count': thesis.get('ref_counts', {}).get(rid, 0),
            'external_links': thesis.get('ref_external', {}).get(rid, {})
        })
    return jsonify({
        'references': refs,
        'total': len(refs),
        'total_citations': sum(thesis.get('ref_counts', {}).values())
    })

@app.route('/api/thesis/figures')
def api_thesis_figures():
    """返回图表索引"""
    thesis = parse_thesis_md()
    if not thesis:
        return jsonify({'error': 'not found'}), 404
    return jsonify({
        'figures': thesis.get('figures_index', []),
        'tables': thesis.get('tables_index', [])
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
