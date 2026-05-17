"""
OGD-Collector Pro V6 - 统一版本Flask应用
整合服务器V3内容和本地修改，单一路径部署
"""

import json
import sqlite3
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
    """数据复现 → 重定向到数据可信度中心"""
    return redirect('/credibility', code=301)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
