"""
OGD-Collector Pro Web应用
三层架构数据开放平台采集系统 - Web服务层
作者：文明（武汉大学信息管理学院博士生）
日期：2026-04-22
"""

import os
import sys
import json
import sqlite3
import threading
import time
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, jsonify, request, Response, redirect, url_for, session
from functools import wraps

# 确保能导入本地模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models import get_db, init_db, init_platforms_data, DB_PATH
from collector_engine import CollectorEngine, create_collection_task

app = Flask(__name__)
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ogd-collector-pro-dev-key-change-in-production')
app.config['JSON_AS_ASCII'] = False

# ===== 隐私保护：登录认证 =====
AUTH_PASSWORD = os.environ.get('AUTH_PASSWORD', '123')


def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': '未授权，请先登录'}), 401
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function


def record_access():
    """记录访问日志"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO access_logs (ip, path, method, user_agent, accessed_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            request.remote_addr,
            request.path,
            request.method,
            request.headers.get('User-Agent', '')[:200],
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
    except Exception:
        pass


# 全局采集引擎实例
active_engine = None


def get_stats():
    """获取系统统计信息"""
    conn = get_db()
    cursor = conn.cursor()
    
    stats = {}
    
    # 平台总数
    cursor.execute("SELECT COUNT(*) FROM platforms")
    stats['total_platforms'] = cursor.fetchone()[0]
    
    # 按层级统计
    cursor.execute("SELECT tier, COUNT(*) FROM platforms GROUP BY tier")
    stats['tier_distribution'] = {row[0]: row[1] for row in cursor.fetchall()}
    
    # 任务总数
    cursor.execute("SELECT COUNT(*) FROM collection_tasks")
    stats['total_tasks'] = cursor.fetchone()[0]
    
    # 最新任务
    cursor.execute("""
        SELECT id, task_name, status, total_count, completed_count, success_count, fail_count, created_at
        FROM collection_tasks ORDER BY id DESC LIMIT 5
    """)
    stats['recent_tasks'] = [dict(zip(['id', 'task_name', 'status', 'total', 'completed', 'success', 'failed', 'created_at'], row)) 
                             for row in cursor.fetchall()]
    
    # 采集记录总数
    cursor.execute("SELECT COUNT(*) FROM collection_records")
    stats['total_records'] = cursor.fetchone()[0]
    
    # 可用平台数
    cursor.execute("SELECT COUNT(*) FROM collection_records WHERE status='available'")
    stats['available_count'] = cursor.fetchone()[0]
    
    conn.close()
    return stats


@app.route('/robots.txt')
def robots():
    """禁止搜索引擎抓取"""
    return Response("User-agent: *\nDisallow: /\n", mimetype='text/plain')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """登录页面"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == AUTH_PASSWORD:
            session['logged_in'] = True
            session.permanent = True
            return redirect(url_for('index'))
        return render_template('login.html', title='登录 | OGD-Collector Pro', error='密码错误')
    return render_template('login.html', title='登录 | OGD-Collector Pro')


@app.route('/logout')
def logout():
    """退出登录"""
    session.pop('logged_in', None)
    return redirect(url_for('login_page'))


@app.route('/')
@login_required
def index():
    """主控台首页"""
    record_access()
    stats = get_stats()
    return render_template('index.html', stats=stats, title='OGD-Collector Pro | 主控台')


@app.route('/dashboard')
@login_required
def dashboard():
    """数据看板"""
    record_access()
    return render_template('dashboard.html', title='数据看板 | OGD-Collector Pro')


@app.route('/collector')
@login_required
def collector_page():
    """采集任务管理"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, task_name, task_type, status, total_count, completed_count, success_count, fail_count, started_at, completed_at
        FROM collection_tasks ORDER BY id DESC
    """)
    tasks = []
    for row in cursor.fetchall():
        task = dict(zip(['id', 'task_name', 'task_type', 'status', 'total', 'completed', 'success', 'failed', 'started', 'completed_time'], row))
        # 确保数值字段为整数
        for key in ['id', 'total', 'completed', 'success', 'failed']:
            if task.get(key) is not None:
                try:
                    task[key] = int(task[key])
                except (ValueError, TypeError):
                    task[key] = 0
        tasks.append(task)
    conn.close()
    return render_template('collector.html', tasks=tasks, title='采集管理 | OGD-Collector Pro')


@app.route('/platforms')
@login_required
def platforms_page():
    """平台详情"""
    record_access()
    return render_template('platforms.html', title='平台详情 | OGD-Collector Pro')


@app.route('/analysis')
@login_required
def analysis_page():
    """分析图表"""
    record_access()
    return render_template('analysis.html', title='分析图表 | OGD-Collector Pro')

@app.route('/thesis')
@login_required
def thesis_page():
    """论文成果展示页面"""
    record_access()
    return render_template('thesis.html', title='论文成果展示 | OGD-Collector Pro')


# ===== API接口 =====

@app.route('/api/stats')
@login_required
def api_stats():
    """获取系统统计"""
    return jsonify(get_stats())


@app.route('/api/tasks', methods=['GET', 'POST'])
@login_required
def api_tasks():
    """任务管理API"""
    if request.method == 'POST':
        data = request.json
        task_name = data.get('task_name', f'采集任务_{datetime.now().strftime("%m%d%H%M")}')
        task_type = data.get('task_type', 'full')
        
        task_id = create_collection_task(task_name, task_type)
        return jsonify({'success': True, 'task_id': task_id, 'message': '任务创建成功'})
    
    # GET
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, task_name, task_type, status, total_count, completed_count, success_count, fail_count, 
               started_at, completed_at, created_at
        FROM collection_tasks ORDER BY id DESC
    """)
    tasks = []
    for row in cursor.fetchall():
        tasks.append({
            'id': row[0], 'task_name': row[1], 'task_type': row[2], 'status': row[3],
            'total': row[4], 'completed': row[5], 'success': row[6], 'failed': row[7],
            'started': row[8], 'completed_time': row[9], 'created': row[10]
        })
    conn.close()
    return jsonify(tasks)


@app.route('/api/tasks/<int:task_id>/start', methods=['POST'])
@login_required
def api_start_task(task_id):
    """启动采集任务"""
    global active_engine
    
    if active_engine and active_engine.is_running:
        return jsonify({'success': False, 'message': '已有采集任务正在运行'})
    
    # 获取任务配置
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT task_type, config_json FROM collection_tasks WHERE id=?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return jsonify({'success': False, 'message': '任务不存在'})
    
    task_type, config_json = row
    config = json.loads(config_json) if config_json else {}
    
    # 创建引擎并启动（在后台线程中运行）
    active_engine = CollectorEngine(
        task_id=task_id,
        max_workers=config.get('max_workers', 3),
        delay=config.get('delay', 2)
    )
    
    filter_map = {
        'full': None,
        'provincial': {'tier': '省级'},
        'subprovincial': {'tier': '副省级/计划单列市'},
        'prefectural': {'tier': '地级市'}
    }
    platform_filter = filter_map.get(task_type)
    
    def run_in_thread():
        active_engine.run_collection(platform_filter)
    
    thread = threading.Thread(target=run_in_thread)
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'message': '任务已启动', 'task_id': task_id})


@app.route('/api/tasks/<int:task_id>/stop', methods=['POST'])
@login_required
def api_stop_task(task_id):
    """停止采集任务"""
    global active_engine
    if active_engine:
        active_engine.stop()
        active_engine = None
    return jsonify({'success': True, 'message': '任务已停止'})


@app.route('/api/tasks/<int:task_id>/progress')
@login_required
def api_task_progress(task_id):
    """获取任务实时进度（SSE流）"""
    def event_stream():
        global active_engine
        last_progress = None
        
        while True:
            if active_engine and active_engine.task_id == task_id:
                try:
                    progress = active_engine.progress_queue.get(timeout=1)
                    if progress != last_progress:
                        last_progress = progress
                        yield f"data: {json.dumps(progress, ensure_ascii=False)}\n\n"
                except:
                    pass
            else:
                # 查询数据库获取最新状态
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT status, completed_count, success_count, fail_count, total_count
                    FROM collection_tasks WHERE id=?
                """, (task_id,))
                row = cursor.fetchone()
                conn.close()
                
                if row:
                    status, completed, success, failed, total = row
                    yield f"data: {json.dumps({'status': status, 'completed': completed or 0, 'success': success or 0, 'failed': failed or 0, 'total': total or 0}, ensure_ascii=False)}\n\n"
                
                time.sleep(2)
                
            if not (active_engine and active_engine.is_running):
                break
    
    return Response(event_stream(), mimetype='text/event-stream')


@app.route('/api/records')
@login_required
def api_records():
    """获取采集记录"""
    task_id = request.args.get('task_id', type=int)
    tier = request.args.get('tier')
    status = request.args.get('status')
    limit = request.args.get('limit', 100, type=int)
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = """
        SELECT r.*, p.url, p.url_pattern 
        FROM collection_records r
        JOIN platforms p ON r.platform_id = p.id
        WHERE 1=1
    """
    params = []
    
    if task_id:
        query += " AND r.task_id=?"
        params.append(task_id)
    if tier:
        query += " AND r.tier=?"
        params.append(tier)
    if status:
        query += " AND r.status=?"
        params.append(status)
    
    query += " ORDER BY r.id DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    records = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(records)


@app.route('/api/platforms')
@login_required
def api_platforms():
    """获取平台列表"""
    tier = request.args.get('tier')
    region = request.args.get('region')
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM platforms WHERE 1=1"
    params = []
    
    if tier:
        query += " AND tier=?"
        params.append(tier)
    if region:
        query += " AND region=?"
        params.append(region)
    
    query += " ORDER BY tier, region, name"
    
    cursor.execute(query, params)
    platforms = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(platforms)


@app.route('/api/analysis/tier_comparison')
@login_required
def api_tier_comparison():
    """获取层级比较分析数据"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 按层级统计
    cursor.execute("""
        SELECT tier, 
               COUNT(*) as total,
               SUM(CASE WHEN status='available' THEN 1 ELSE 0 END) as available,
               ROUND(AVG(CASE WHEN status='available' THEN overall_score ELSE NULL END), 3) as avg_score,
               ROUND(AVG(CASE WHEN status='available' THEN score_c1 ELSE NULL END), 3) as avg_c1,
               ROUND(AVG(CASE WHEN status='available' THEN score_c2 ELSE NULL END), 3) as avg_c2,
               ROUND(AVG(CASE WHEN status='available' THEN score_c3 ELSE NULL END), 3) as avg_c3,
               ROUND(AVG(CASE WHEN status='available' THEN score_c4 ELSE NULL END), 3) as avg_c4
        FROM collection_records
        GROUP BY tier
    """)
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'tier': row[0], 'total': row[1], 'available': row[2] or 0,
            'avg_score': row[3] or 0, 'avg_c1': row[4] or 0,
            'avg_c2': row[5] or 0, 'avg_c3': row[6] or 0, 'avg_c4': row[7] or 0
        })
    
    conn.close()
    return jsonify(results)


@app.route('/api/analysis/region_distribution')
@login_required
def api_region_distribution():
    """获取区域分布分析数据"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT region,
               COUNT(*) as total,
               SUM(CASE WHEN status='available' THEN 1 ELSE 0 END) as available,
               ROUND(AVG(CASE WHEN status='available' THEN overall_score ELSE NULL END), 3) as avg_score
        FROM collection_records
        GROUP BY region
        ORDER BY avg_score DESC
    """)
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'region': row[0], 'total': row[1], 'available': row[2] or 0, 'avg_score': row[3] or 0
        })
    
    conn.close()
    return jsonify(results)


@app.route('/api/analysis/top_platforms')
@login_required
def api_top_platforms():
    """获取TOP平台"""
    limit = request.args.get('limit', 10, type=int)
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT r.platform_name, r.tier, r.region, r.overall_score, 
               r.score_c1, r.score_c2, r.score_c3, r.score_c4,
               r.dataset_count, r.has_api, r.has_search, r.response_time
        FROM collection_records r
        WHERE r.status='available'
        ORDER BY r.overall_score DESC
        LIMIT ?
    """, (limit,))
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'name': row[0], 'tier': row[1], 'region': row[2], 'overall': row[3],
            'c1': row[4], 'c2': row[5], 'c3': row[6], 'c4': row[7],
            'datasets': row[8], 'has_api': row[9], 'has_search': row[10], 'response_time': row[11]
        })
    
    conn.close()
    return jsonify(results)


@app.route('/api/export/csv')
@login_required
def api_export_csv():
    """导出CSV数据"""
    import csv
    import io
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM collection_records ORDER BY id")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(columns)
    writer.writerows(rows)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=ogd_collection_{datetime.now().strftime("%Y%m%d")}.csv'}
    )


# ===== 丰富数据维度API =====

@app.route('/api/analysis/trend')
@login_required
def api_trend():
    """获取采集趋势数据（按日统计）"""
    days = request.args.get('days', 30, type=int)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT stat_date, total_platforms, available_count, avg_score,
               avg_c1, avg_c2, avg_c3, avg_c4
        FROM collection_stats
        WHERE stat_date >= date('now', '-{} days')
        ORDER BY stat_date
    """.format(days))
    results = []
    for row in cursor.fetchall():
        results.append({
            'date': row[0], 'total': row[1], 'available': row[2],
            'avg_score': row[3], 'c1': row[4], 'c2': row[5], 'c3': row[6], 'c4': row[7]
        })
    conn.close()
    return jsonify(results)


@app.route('/api/analysis/platform_features')
@login_required
def api_platform_features():
    """获取平台架构与特征分析"""
    conn = get_db()
    cursor = conn.cursor()
    # CMS类型分布
    cursor.execute("""
        SELECT cms_type, COUNT(*) FROM platform_features
        WHERE cms_type IS NOT NULL GROUP BY cms_type
    """)
    cms_dist = {row[0]: row[1] for row in cursor.fetchall()}
    # 功能特征统计
    cursor.execute("""
        SELECT 
            SUM(has_mobile_version) as mobile,
            SUM(has_feedback) as feedback,
            SUM(has_data_request) as request,
            SUM(has_app_showcase) as showcase
        FROM platform_features
    """)
    row = cursor.fetchone()
    feature_stats = {
        'mobile': row[0] or 0, 'feedback': row[1] or 0,
        'data_request': row[2] or 0, 'app_showcase': row[3] or 0
    }
    conn.close()
    return jsonify({'cms_distribution': cms_dist, 'feature_stats': feature_stats})


@app.route('/api/analysis/data_quality')
@login_required
def api_data_quality():
    """数据质量深度分析"""
    conn = get_db()
    cursor = conn.cursor()
    # 按层级数据质量分布
    cursor.execute("""
        SELECT tier,
               ROUND(AVG(dataset_count), 1) as avg_datasets,
               ROUND(AVG(CASE WHEN has_api=1 THEN 1 ELSE 0 END)*100, 1) as api_rate,
               ROUND(AVG(CASE WHEN has_bulk_download=1 THEN 1 ELSE 0 END)*100, 1) as bulk_rate,
               ROUND(AVG(CASE WHEN has_update_info=1 THEN 1 ELSE 0 END)*100, 1) as update_rate,
               ROUND(AVG(CASE WHEN has_metadata=1 THEN 1 ELSE 0 END)*100, 1) as meta_rate
        FROM collection_records WHERE status='available' GROUP BY tier
    """)
    results = []
    for row in cursor.fetchall():
        results.append({
            'tier': row[0], 'avg_datasets': row[1],
            'api_rate': row[2], 'bulk_rate': row[3],
            'update_rate': row[4], 'meta_rate': row[5]
        })
    conn.close()
    return jsonify(results)


@app.route('/api/stats/overview')
@login_required
def api_stats_overview():
    """系统总览统计（丰富版）"""
    conn = get_db()
    cursor = conn.cursor()
    stats = {}
    # 基础统计
    cursor.execute("SELECT COUNT(*) FROM platforms")
    stats['total_platforms'] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM collection_records")
    stats['total_records'] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM collection_tasks")
    stats['total_tasks'] = cursor.fetchone()[0]
    # 层级分布
    cursor.execute("SELECT tier, COUNT(*) FROM platforms GROUP BY tier")
    stats['tier_distribution'] = {row[0]: row[1] for row in cursor.fetchall()}
    # 可用率
    cursor.execute("""
        SELECT COUNT(*) FROM collection_records WHERE status='available'
    """)
    avail = cursor.fetchone()[0]
    total_rec = stats['total_records'] or 1
    stats['availability_rate'] = round(avail / total_rec * 100, 1)
    # 平均得分
    cursor.execute("""
        SELECT ROUND(AVG(overall_score), 3) FROM collection_records WHERE status='available'
    """)
    stats['avg_score'] = cursor.fetchone()[0] or 0
    # 数据集总量
    cursor.execute("SELECT SUM(dataset_count) FROM collection_records")
    stats['total_datasets'] = cursor.fetchone()[0] or 0
    # API支持率
    cursor.execute("""
        SELECT ROUND(AVG(CASE WHEN has_api=1 THEN 1 ELSE 0 END)*100, 1)
        FROM collection_records WHERE status='available'
    """)
    stats['api_support_rate'] = cursor.fetchone()[0] or 0
    conn.close()
    return jsonify(stats)


@app.route('/api/thesis/charts')
@login_required
def api_thesis_charts():
    """获取论文图表列表"""
    import glob
    chart_dir = Path(__file__).parent / 'static' / 'thesis_charts'
    charts = []
    if chart_dir.exists():
        for f in sorted(chart_dir.glob('图*.png')):
            name = f.stem
            charts.append({'name': name, 'url': f'/static/thesis_charts/{f.name}'})
    return jsonify(charts)


@app.route('/api/access/logs')
@login_required
def api_access_logs():
    """获取访问日志（管理员）"""
    limit = request.args.get('limit', 50, type=int)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ip, path, method, accessed_at FROM access_logs
        ORDER BY id DESC LIMIT ?
    """, (limit,))
    logs = [{'ip': row[0], 'path': row[1], 'method': row[2], 'time': row[3]}
            for row in cursor.fetchall()]
    conn.close()
    return jsonify(logs)


# 初始化数据库
@app.before_request
def before_first_request():
    """首次请求前初始化数据库"""
    if not DB_PATH.exists():
        init_db()
        init_platforms_data()


if __name__ == '__main__':
    # 确保数据库已初始化
    if not DB_PATH.exists():
        init_db()
        init_platforms_data()
    
    print("=" * 60)
    print("OGD-Collector Pro 启动中...")
    print("三层架构数据开放平台采集系统")
    print("作者：文明（武汉大学信息管理学院博士生）")
    print("=" * 60)
    print("访问地址: http://127.0.0.1:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
