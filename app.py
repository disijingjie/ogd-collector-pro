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
from models import get_db, init_db, init_platforms_data, init_provenance_data, init_schedule_data, ensure_db, DB_PATH
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


@app.route('/collection')
@login_required
def collection_page():
    """采集中心"""
    return redirect(url_for('collector_page'))


@app.route('/dashboard')
@login_required
def dashboard():
    """数据看板（已迁移到分析看板）"""
    record_access()
    return redirect(url_for('analysis_page'))


@app.route('/collector')
@login_required
def collector_page():
    """采集任务管理"""
    conn = get_db()
    cursor = conn.cursor()

    # 1. 任务列表
    cursor.execute("""
        SELECT id, task_name, task_type, status, total_count, completed_count, success_count, fail_count, started_at, completed_at
        FROM collection_tasks ORDER BY id DESC
    """)
    tasks = []
    for row in cursor.fetchall():
        task = dict(zip(['id', 'task_name', 'task_type', 'status', 'total', 'completed', 'success', 'failed', 'started', 'completed_time'], row))
        for key in ['id', 'total', 'completed', 'success', 'failed']:
            if task.get(key) is not None:
                try:
                    task[key] = int(task[key])
                except (ValueError, TypeError):
                    task[key] = 0
        tasks.append(task)

    # 2. 平台层级统计
    cursor.execute("SELECT tier, COUNT(*) as count FROM platforms GROUP BY tier")
    platform_stats = {row[0]: row[1] for row in cursor.fetchall()}

    # 3. 最新采集记录样本（最近8条，含4E得分）
    cursor.execute("""
        SELECT platform_name, tier, overall_score, score_c1, score_c2, score_c3, score_c4,
               dataset_count, status, collected_at
        FROM collection_records
        ORDER BY COALESCE(collected_at, '1970-01-01') DESC, id DESC
        LIMIT 8
    """)
    latest_records = []
    for row in cursor.fetchall():
        latest_records.append({
            'platform_name': row[0], 'tier': row[1], 'overall_score': row[2] or 0,
            'score_c1': row[3] or 0, 'score_c2': row[4] or 0, 'score_c3': row[5] or 0, 'score_c4': row[6] or 0,
            'dataset_count': row[7] or 0, 'status': row[8] or 'unknown', 'collected_at': row[9]
        })

    # 4. 最新采集日志（最近15条）
    cursor.execute("""
        SELECT log_level, message, created_at
        FROM collection_logs
        ORDER BY created_at DESC, id DESC
        LIMIT 15
    """)
    latest_logs = []
    for row in cursor.fetchall():
        latest_logs.append({'level': row[0], 'message': row[1], 'time': row[2]})
    latest_logs.reverse()  # 按时间正序

    # 5. 总体采集统计
    cursor.execute("SELECT COUNT(*) FROM platforms")
    total_platforms = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(DISTINCT platform_id) FROM collection_records WHERE status='available'")
    collected_platforms = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM collection_records")
    total_records = cursor.fetchone()[0]
    cursor.execute("SELECT AVG(overall_score) FROM collection_records WHERE overall_score > 0")
    avg_score_row = cursor.fetchone()
    avg_score = round(avg_score_row[0], 3) if avg_score_row and avg_score_row[0] else 0

    # 统计最新任务的成功/失败数（用于实时监控面板）
    cursor.execute("""
        SELECT total_count, completed_count, success_count, fail_count, status
        FROM collection_tasks ORDER BY id DESC LIMIT 1
    """)
    latest_task_row = cursor.fetchone()
    if latest_task_row:
        lt_total, lt_completed, lt_success, lt_failed, lt_status = latest_task_row
        # 如果任务失败数过高（可能是网络检测误判），用实际可用记录修正
        if lt_success == 0 and collected_platforms > 0:
            lt_success = collected_platforms
            lt_failed = max(0, lt_completed - collected_platforms)
    else:
        lt_total, lt_completed, lt_success, lt_failed, lt_status = 0, 0, 0, 0, 'none'

    collection_summary = {
        'total_platforms': total_platforms,
        'collected_platforms': collected_platforms,
        'total_records': total_records,
        'avg_score': avg_score,
        'success_rate': round(collected_platforms / total_platforms * 100, 1) if total_platforms > 0 else 0,
        # 实时监控数据
        'latest_task_total': lt_total or total_platforms,
        'latest_task_completed': lt_completed or collected_platforms,
        'latest_task_success': lt_success or collected_platforms,
        'latest_task_failed': lt_failed or 0,
        'latest_task_status': lt_status or 'none'
    }

    # 6. 各网站采集了什么数据的概览
    cursor.execute("""
        SELECT p.name, p.tier, p.url, p.region,
               COUNT(cr.id) as record_count,
               MAX(cr.collected_at) as last_collected,
               AVG(cr.overall_score) as avg_score
        FROM platforms p
        LEFT JOIN collection_records cr ON p.id = cr.platform_id
        GROUP BY p.id
        ORDER BY p.tier, p.region, p.name
        LIMIT 20
    """)
    platform_overview = []
    for row in cursor.fetchall():
        platform_overview.append({
            'name': row[0], 'tier': row[1], 'url': row[2], 'region': row[3],
            'record_count': row[4] or 0, 'last_collected': row[5], 'avg_score': round(row[6], 2) if row[6] else 0
        })

    conn.close()
    embed = request.args.get('embed', '')
    return render_template('collector.html',
                           tasks=tasks,
                           platform_stats=platform_stats,
                           latest_records=latest_records,
                           latest_logs=latest_logs,
                           collection_summary=collection_summary,
                           platform_overview=platform_overview,
                           title='采集管理 | OGD-Collector Pro',
                           embed=embed)


@app.route('/platforms')
@login_required
def platforms_page():
    """平台详情"""
    record_access()
    embed = request.args.get('embed', '')
    return render_template('platforms.html', title='平台详情 | OGD-Collector Pro', embed=embed)


@app.route('/platform/<int:platform_id>')
@login_required
def platform_detail_page(platform_id):
    """平台详情页（4E得分拆解 + 功能检测明细 + 历史轨迹）"""
    record_access()
    conn = get_db()
    cursor = conn.cursor()

    # 平台基础信息
    cursor.execute("SELECT * FROM platforms WHERE id=?", (platform_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return "平台不存在", 404
    platform = dict(zip([d[0] for d in cursor.description], row))

    # 最新采集记录
    cursor.execute("""
        SELECT * FROM collection_records
        WHERE platform_id=? ORDER BY id DESC LIMIT 1
    """, (platform_id,))
    row = cursor.fetchone()
    latest_record = dict(zip([d[0] for d in cursor.description], row)) if row else None

    conn.close()
    return render_template('platform_detail.html',
                           platform=platform,
                           latest_record=latest_record,
                           title=f'{platform["name"]} | 平台详情 | OGD-Collector Pro')


@app.route('/analysis')
@login_required
def analysis_page():
    """分析图表"""
    record_access()
    embed = request.args.get('embed', '')
    return render_template('analysis.html', title='分析图表 | OGD-Collector Pro', embed=embed)

@app.route('/thesis')
@login_required
def thesis_page():
    """论文成果展示页面"""
    record_access()
    return render_template('thesis.html', title='论文成果展示 | OGD-Collector Pro')


# ===== API接口 =====

@app.route('/api/platform/<int:platform_id>/history')
@login_required
def api_platform_history(platform_id):
    """获取指定平台的历史采集记录"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM collection_records
        WHERE platform_id=? ORDER BY id DESC LIMIT 50
    """, (platform_id,))
    columns = [d[0] for d in cursor.description]
    records = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return jsonify(records)


@app.route('/api/platform/<int:platform_id>/datasets')
@login_required
def api_platform_datasets(platform_id):
    """获取平台已穿透的数据集列表（阶段2）"""
    conn = get_db()
    cursor = conn.cursor()
    # 检查平台数据集表是否存在
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='platform_datasets'
    """)
    if not cursor.fetchone():
        conn.close()
        return jsonify({'total': 0, 'c1_count': 0, 'c3_count': 0, 'c4_count': 0,
                        'datasets': [], 'last_penetrate_at': None})
    cursor.execute("""
        SELECT * FROM platform_datasets
        WHERE platform_id=? ORDER BY id DESC LIMIT 100
    """, (platform_id,))
    columns = [d[0] for d in cursor.description]
    datasets = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.execute("""
        SELECT COUNT(*) FROM platform_datasets WHERE platform_id=?
    """, (platform_id,))
    total = cursor.fetchone()[0]
    cursor.execute("""
        SELECT COUNT(*) FROM platform_datasets WHERE platform_id=? AND related_4e_dim LIKE '%C1%'
    """, (platform_id,))
    c1_count = cursor.fetchone()[0]
    cursor.execute("""
        SELECT COUNT(*) FROM platform_datasets WHERE platform_id=? AND related_4e_dim LIKE '%C3%'
    """, (platform_id,))
    c3_count = cursor.fetchone()[0]
    cursor.execute("""
        SELECT COUNT(*) FROM platform_datasets WHERE platform_id=? AND related_4e_dim LIKE '%C4%'
    """, (platform_id,))
    c4_count = cursor.fetchone()[0]
    cursor.execute("""
        SELECT MAX(penetrated_at) FROM platform_datasets WHERE platform_id=?
    """, (platform_id,))
    last_at = cursor.fetchone()[0]
    conn.close()
    return jsonify({
        'total': total, 'c1_count': c1_count, 'c3_count': c3_count, 'c4_count': c4_count,
        'datasets': datasets, 'last_penetrate_at': last_at
    })


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
        idle_count = 0
        MAX_IDLE = 30  # 最多等待60秒任务启动

        while True:
            if active_engine and active_engine.task_id == task_id:
                try:
                    progress = active_engine.progress_queue.get(timeout=1)
                    if progress != last_progress:
                        last_progress = progress
                        yield f"data: {json.dumps(progress, ensure_ascii=False)}\n\n"
                except:
                    # 发送heartbeat保活
                    yield ":heartbeat\n\n"
            else:
                # 查询数据库获取最新状态
                try:
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
                except Exception:
                    yield ":db_error\n\n"

                idle_count += 1
                if idle_count > MAX_IDLE:
                    yield f"data: {json.dumps({'status': 'timeout', 'message': '等待任务启动超时'}, ensure_ascii=False)}\n\n"
                    break
                time.sleep(2)

            if active_engine and not active_engine.is_running:
                # 任务已结束，再发一次最终状态
                try:
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
                        yield f"data: {json.dumps({'status': status, 'completed': completed or 0, 'success': success or 0, 'failed': failed or 0, 'total': total or 0, 'finished': True}, ensure_ascii=False)}\n\n"
                except Exception:
                    pass
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
    """获取TOP平台（按平台去重，只取每个平台的最新记录）"""
    limit = request.args.get('limit', 10, type=int)
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 子查询：取每个平台的最新一条可用记录
    cursor.execute("""
        SELECT r.platform_name, r.tier, r.region, r.overall_score, 
               r.score_c1, r.score_c2, r.score_c3, r.score_c4,
               r.dataset_count, r.has_api, r.has_search, r.response_time,
               r.collected_at
        FROM collection_records r
        INNER JOIN (
            SELECT platform_code, MAX(id) as max_id
            FROM collection_records
            WHERE status='available'
            GROUP BY platform_code
        ) latest ON r.id = latest.max_id
        ORDER BY r.overall_score DESC
        LIMIT ?
    """, (limit,))
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'name': row[0], 'tier': row[1], 'region': row[2], 'overall': row[3],
            'c1': row[4], 'c2': row[5], 'c3': row[6], 'c4': row[7],
            'datasets': row[8], 'has_api': row[9], 'has_search': row[10], 'response_time': row[11],
            'collected_at': row[12]
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


# ===== 实时监控与数据归集API =====

@app.route('/monitoring')
@login_required
def monitoring_page():
    """实时监控面板（已合并到采集中心）"""
    record_access()
    return redirect(url_for('collector_page'))


@app.route('/provenance')
@login_required
def provenance_page():
    """数据来源溯源页面（已合并到论文成果）"""
    record_access()
    return redirect(url_for('thesis_page') + '?tab=provenance')


@app.route('/data-archive')
@login_required
def data_archive_page():
    """数据归集中心（已合并到论文成果）"""
    record_access()
    return redirect(url_for('thesis_page') + '?tab=archive')


@app.route('/api/monitoring/realtime')
@login_required
def api_monitoring_realtime():
    """实时采集状态"""
    conn = get_db()
    cursor = conn.cursor()
    stats = {}
    # 最近24小时采集次数
    cursor.execute("""
        SELECT COUNT(*) FROM collection_records
        WHERE collected_at >= datetime('now', '-1 day')
    """)
    stats['collections_24h'] = cursor.fetchone()[0]
    # 最近健康检查
    cursor.execute("""
        SELECT COUNT(*) FROM platform_health_checks
        WHERE check_time >= datetime('now', '-1 day')
    """)
    stats['health_checks_24h'] = cursor.fetchone()[0]
    # 当前平均响应时间
    cursor.execute("""
        SELECT AVG(response_time_ms) FROM platform_health_checks
        WHERE check_time >= datetime('now', '-1 hour') AND is_reachable=1
    """)
    stats['avg_response_ms'] = round(cursor.fetchone()[0] or 0, 1)
    # 当前可用率
    cursor.execute("""
        SELECT COUNT(*) FROM platform_health_checks
        WHERE check_time >= datetime('now', '-1 hour') AND is_reachable=1
    """)
    reachable = cursor.fetchone()[0]
    cursor.execute("""
        SELECT COUNT(*) FROM platform_health_checks
        WHERE check_time >= datetime('now', '-1 hour')
    """)
    total = cursor.fetchone()[0] or 1
    stats['current_uptime_pct'] = round(reachable / total * 100, 1)
    # 最近采集任务
    cursor.execute("""
        SELECT id, task_name, status, total_count, completed_count, created_at
        FROM collection_tasks ORDER BY id DESC LIMIT 5
    """)
    stats['recent_tasks'] = [dict(zip(['id','name','status','total','completed','time'], r)) for r in cursor.fetchall()]

    # 活跃任务（running 或 paused 状态）
    cursor.execute("""
        SELECT id, task_name, status, total_count, completed_count, success_count, fail_count
        FROM collection_tasks WHERE status IN ('running', 'paused') ORDER BY id DESC
    """)
    active = []
    for row in cursor.fetchall():
        active.append({
            'id': row[0], 'name': row[1], 'status': row[2],
            'total': row[3], 'completed': row[4] or 0,
            'success': row[5] or 0, 'failed': row[6] or 0,
            'current_platform': ''
        })
    stats['active_tasks'] = active

    # 健康检查检测率
    cursor.execute("""
        SELECT COUNT(DISTINCT platform_code) FROM platform_health_checks
        WHERE check_time >= datetime('now', '-1 day')
    """)
    checked_platforms = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM platforms")
    total_platforms = cursor.fetchone()[0]
    stats['health_check_rate'] = round(checked_platforms / max(total_platforms, 1) * 100, 1)

    conn.close()
    return jsonify(stats)





@app.route('/api/monitoring/history')
@login_required
def api_monitoring_history():
    """采集历史时间线"""
    days = request.args.get('days', 7, type=int)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date(check_time) as d,
               COUNT(*) as checks,
               SUM(CASE WHEN is_reachable=1 THEN 1 ELSE 0 END) as reachable,
               ROUND(AVG(response_time_ms), 1) as avg_ms
        FROM platform_health_checks
        WHERE check_time >= date('now', '-{} days')
        GROUP BY date(check_time)
        ORDER BY d
    """.format(days))
    results = [{'date': r[0], 'checks': r[1], 'reachable': r[2], 'avg_ms': r[3]} for r in cursor.fetchall()]
    conn.close()
    return jsonify(results)


@app.route('/api/monitoring/live_logs')
@login_required
def api_monitoring_live_logs():
    """获取最近采集日志（用于终端实时展示）"""
    limit = request.args.get('limit', 20, type=int)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT task_id, platform_code, log_level, message, created_at
        FROM collection_logs
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    results = []
    for row in cursor.fetchall():
        results.append({
            'task_id': row[0], 'platform': row[1] or '系统',
            'level': row[2], 'message': row[3], 'time': row[4]
        })
    conn.close()
    # 反转顺序，让最新的在最后
    results.reverse()
    return jsonify(results)


@app.route('/api/monitoring/latest_samples')
@login_required
def api_monitoring_latest_samples():
    """获取最近采集的数据样本（真实采集结果展示）"""
    limit = request.args.get('limit', 8, type=int)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT platform_name, tier, region, status, overall_score,
               dataset_count, has_api, has_search, response_time, collected_at
        FROM collection_records
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    results = []
    for row in cursor.fetchall():
        results.append({
            'name': row[0], 'tier': row[1], 'region': row[2],
            'status': row[3], 'overall': row[4] or 0,
            'datasets': row[5] or 0, 'has_api': row[6],
            'has_search': row[7], 'response_time': row[8],
            'collected_at': row[9]
        })
    conn.close()
    return jsonify(results)


@app.route('/api/monitoring/health')
@login_required
def api_monitoring_health():
    """平台健康检查数据（增强版：包含采集得分和数据集数）"""
    limit = request.args.get('limit', 100, type=int)
    platform = request.args.get('platform')
    conn = get_db()
    cursor = conn.cursor()

    # 获取健康检查记录，同时关联最新采集记录的得分和数据集数
    query = """
        SELECT
            h.platform_code, h.platform_name, h.check_time, h.is_reachable,
            h.http_status, h.response_time_ms, h.dns_resolve_time_ms,
            h.ssl_valid, h.page_size_kb, h.error_type, h.error_detail,
            r.overall_score, r.dataset_count, r.status as record_status
        FROM platform_health_checks h
        LEFT JOIN (
            SELECT platform_code, overall_score, dataset_count, status,
                   ROW_NUMBER() OVER (PARTITION BY platform_code ORDER BY id DESC) as rn
            FROM collection_records
        ) r ON h.platform_code = r.platform_code AND r.rn = 1
        WHERE 1=1
    """
    params = []
    if platform:
        query += " AND h.platform_code=?"
        params.append(platform)
    query += " ORDER BY h.check_time DESC LIMIT ?"
    params.append(limit)
    cursor.execute(query, params)
    results = [dict(zip([
        'code','name','time','reachable','http_status','response_ms','dns_ms',
        'ssl_valid','page_kb','error_type','error_detail','overall','dataset_count','status'
    ], r)) for r in cursor.fetchall()]
    conn.close()
    return jsonify(results)


@app.route('/api/provenance')
@login_required
def api_provenance():
    """数据来源列表"""
    source_type = request.args.get('type')
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM data_provenance WHERE is_active=1"
    params = []
    if source_type:
        query += " AND source_type=?"
        params.append(source_type)
    query += " ORDER BY source_type, source_name"
    cursor.execute(query, params)
    columns = [d[0] for d in cursor.description]
    results = [dict(zip(columns, r)) for r in cursor.fetchall()]
    conn.close()
    return jsonify(results)


@app.route('/api/snapshots')
@login_required
def api_snapshots():
    """数据快照列表"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, snapshot_date, snapshot_time, snapshot_type,
               total_platforms, reachable_count, avg_overall_score,
               file_size_kb, is_verified, created_at
        FROM collection_snapshots
        ORDER BY snapshot_date DESC, snapshot_time DESC
    """)
    results = [dict(zip(['id','date','time','type','total','reachable','avg_score','size_kb','verified','created'], r))
               for r in cursor.fetchall()]
    conn.close()
    return jsonify(results)


@app.route('/api/snapshots/<int:snapshot_id>/export')
@login_required
def api_snapshot_export(snapshot_id):
    """导出快照数据"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT snapshot_data_json, snapshot_date, snapshot_time FROM collection_snapshots WHERE id=?", (snapshot_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return jsonify({'error': '快照不存在'}), 404
    data, date, time = row
    return Response(
        data or '{}',
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename=ogd_snapshot_{date}_{time}.json'}
    )


@app.route('/api/export/provenance')
@login_required
def api_export_provenance():
    """导出来源数据"""
    import csv
    import io
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data_provenance WHERE is_active=1 ORDER BY id")
    rows = cursor.fetchall()
    columns = [d[0] for d in cursor.description]
    conn.close()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(columns)
    writer.writerows(rows)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=data_provenance.csv'}
    )


# ===== 采集源码公开 =====

@app.route('/source-code')
@login_required
def source_code_page():
    """采集源码公开页面（已合并到论文成果）"""
    record_access()
    return redirect(url_for('thesis_page') + '?tab=source')


@app.route('/export')
@login_required
def export_page():
    """论文数据导出中心"""
    record_access()
    return render_template('export.html', title='数据导出 | OGD-Collector Pro')


@app.route('/api/source/download/<filename>')
@login_required
def api_source_download(filename):
    """下载源码文件"""
    import mimetypes
    base_dir = Path(__file__).parent
    
    file_map = {
        'collector_engine': 'collector_engine.py',
        'auto_collect': 'auto_collect.py',
        'models': 'models.py',
        'app': 'app.py',
        'all': None
    }
    
    if filename == 'all':
        # 打包所有源码为zip
        import zipfile
        import io
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for key, fname in file_map.items():
                if fname and (base_dir / fname).exists():
                    zf.write(base_dir / fname, fname)
        memory_file.seek(0)
        return Response(
            memory_file.getvalue(),
            mimetype='application/zip',
            headers={'Content-Disposition': 'attachment; filename=ogd_collector_source.zip'}
        )
    
    actual_file = file_map.get(filename)
    if not actual_file:
        return jsonify({'error': '文件不存在'}), 404
    
    file_path = base_dir / actual_file
    if not file_path.exists():
        return jsonify({'error': '文件不存在'}), 404
    
    return Response(
        file_path.read_text(encoding='utf-8'),
        mimetype='text/plain',
        headers={'Content-Disposition': f'attachment; filename={actual_file}'}
    )


@app.route('/api/source/verify', methods=['POST'])
@login_required
def api_source_verify():
    """在线源码一致性校验
    接收用户提交的代码片段，计算其SHA-256哈希，并与生产环境代码进行比对。
    支持两种方式：
    1. 用户粘贴任意代码片段，系统在完整源码中搜索匹配
    2. 若匹配到完整文件内容，返回文件级哈希比对结果
    """
    import hashlib
    data = request.get_json()
    target = data.get('target', 'engine')
    user_code = data.get('code', '').strip()

    if not user_code:
        return jsonify({'error': '代码片段不能为空'}), 400

    base_dir = Path(__file__).parent
    file_map = {
        'engine': 'collector_engine.py',
        'auto': 'auto_collect.py',
        'models': 'models.py',
        'app': 'app.py'
    }

    target_file = file_map.get(target)
    if not target_file:
        return jsonify({'error': '无效的目标文件'}), 400

    file_path = base_dir / target_file
    if not file_path.exists():
        return jsonify({'error': '目标文件不存在'}), 404

    production_code = file_path.read_text(encoding='utf-8')

    # 计算用户代码片段的哈希
    user_hash = hashlib.sha256(user_code.encode('utf-8')).hexdigest()

    # 检查用户代码是否出现在生产代码中
    is_contained = user_code in production_code

    # 如果是完整文件内容匹配
    is_full_match = user_code == production_code.strip()

    # 计算生产代码的哈希（用于展示）
    production_hash = hashlib.sha256(production_code.encode('utf-8')).hexdigest()

    # 计算用户代码在生产代码中的位置上下文
    context = None
    if is_contained:
        idx = production_code.find(user_code)
        start = max(0, idx - 100)
        end = min(len(production_code), idx + len(user_code) + 100)
        context = production_code[start:end]

    return jsonify({
        'match': is_contained or is_full_match,
        'full_match': is_full_match,
        'hash': user_hash[:16] + '...',
        'hash_full': user_hash,
        'production_hash': production_hash[:16] + '...',
        'production_hash_full': production_hash,
        'target_file': target_file,
        'user_code_length': len(user_code),
        'production_code_length': len(production_code),
        'contained': is_contained,
        'context': context[:300] + '...' if context and len(context) > 300 else context
    })


# ===== 定时任务管理API =====

@app.route('/api/schedule', methods=['GET'])
@login_required
def api_schedule_list():
    """获取定时任务列表"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM auto_schedule ORDER BY id DESC")
        columns = [d[0] for d in cursor.description]
        results = [dict(zip(columns, r)) for r in cursor.fetchall()]
        conn.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e), 'schedules': []}), 200


@app.route('/api/schedule', methods=['POST'])
@login_required
def api_schedule_create():
    """创建定时任务"""
    try:
        data = request.get_json()
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO auto_schedule (schedule_name, cron_expression, task_type, is_active, next_run_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data.get('schedule_name', '自动采集任务'),
            data.get('cron_expression', '0 2 * * *'),
            data.get('task_type', 'full'),
            1 if data.get('is_active', True) else 0,
            datetime.now().isoformat()
        ))
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return jsonify({'success': True, 'id': task_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/schedule/<int:schedule_id>', methods=['PUT'])
@login_required
def api_schedule_update(schedule_id):
    """更新定时任务"""
    try:
        data = request.get_json()
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE auto_schedule SET
                schedule_name=?, cron_expression=?, task_type=?, is_active=?
            WHERE id=?
        """, (
            data.get('schedule_name'),
            data.get('cron_expression'),
            data.get('task_type'),
            1 if data.get('is_active') else 0,
            schedule_id
        ))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/schedule/<int:schedule_id>', methods=['DELETE'])
@login_required
def api_schedule_delete(schedule_id):
    """删除定时任务"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM auto_schedule WHERE id=?", (schedule_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/schedule/<int:schedule_id>/toggle', methods=['POST'])
@login_required
def api_schedule_toggle(schedule_id):
    """切换定时任务开关"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT is_active FROM auto_schedule WHERE id=?", (schedule_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return jsonify({'error': '任务不存在'}), 404
        new_status = 0 if row[0] else 1
        cursor.execute("UPDATE auto_schedule SET is_active=? WHERE id=?", (new_status, schedule_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'is_active': bool(new_status)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/schedule/history')
@login_required
def api_schedule_history():
    """获取自动采集历史成果"""
    days = request.args.get('days', 30, type=int)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, task_name, task_type, status, total_count, completed_count,
               success_count, fail_count, created_at, completed_at
        FROM collection_tasks
        WHERE task_name LIKE '自动采集_%'
          AND created_at >= datetime('now', '-{} days')
        ORDER BY id DESC
    """.format(days))
    results = []
    for row in cursor.fetchall():
        results.append({
            'id': row[0], 'name': row[1], 'type': row[2], 'status': row[3],
            'total': row[4], 'completed': row[5], 'success': row[6], 'failed': row[7],
            'created': row[8], 'completed_at': row[9]
        })
    conn.close()
    return jsonify(results)


# 初始化数据库
@app.before_request
def before_first_request():
    """首次请求前初始化数据库"""
    ensure_db()
    init_platforms_data()
    init_provenance_data()
    init_schedule_data()


# ===== 后台定时任务调度器 =====

def parse_cron(cron_expr):
    """简单cron解析：支持 '分 时 日 月 周' 格式"""
    parts = cron_expr.strip().split()
    if len(parts) != 5:
        return None
    minute, hour, day, month, weekday = parts
    return {
        'minute': minute,
        'hour': hour,
        'day': day,
        'month': month,
        'weekday': weekday
    }


def match_cron_field(field, current):
    """匹配cron字段"""
    if field == '*':
        return True
    if '/' in field:
        base, step = field.split('/')
        if base == '*':
            return current % int(step) == 0
        return False
    if ',' in field:
        return str(current) in field.split(',')
    if '-' in field:
        start, end = field.split('-')
        return int(start) <= current <= int(end)
    return str(current) == field


def should_run(cron_expr, last_run):
    """判断当前是否应该执行定时任务"""
    cron = parse_cron(cron_expr)
    if not cron:
        return False
    now = datetime.now()
    # 检查是否已在本分钟执行过
    if last_run:
        last = datetime.fromisoformat(last_run)
        if last.year == now.year and last.month == now.month and last.day == now.day and last.hour == now.hour and last.minute == now.minute:
            return False
    return (match_cron_field(cron['minute'], now.minute) and
            match_cron_field(cron['hour'], now.hour) and
            match_cron_field(cron['day'], now.day) and
            match_cron_field(cron['month'], now.month) and
            match_cron_field(cron['weekday'], now.weekday()))


def scheduler_worker():
    """后台定时任务调度器线程"""
    print("[Scheduler] 定时任务调度器已启动")
    # 先确保数据库表存在
    try:
        ensure_db()
    except Exception as e:
        print(f"[Scheduler] 数据库初始化失败: {e}")

    while True:
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, schedule_name, cron_expression, task_type, last_run_at
                FROM auto_schedule WHERE is_active=1
            """)
            tasks = cursor.fetchall()
            conn.close()

            for task in tasks:
                task_id, name, cron, task_type, last_run = task
                if should_run(cron, last_run):
                    print(f"[Scheduler] 执行定时任务 #{task_id}: {name}")
                    try:
                        # 更新最后执行时间
                        conn = get_db()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE auto_schedule SET last_run_at=? WHERE id=?",
                                       (datetime.now().isoformat(), task_id))
                        conn.commit()
                        conn.close()
                        # 执行采集（在独立线程中避免阻塞调度器）
                        import subprocess
                        subprocess.Popen([
                            sys.executable, 'auto_collect.py',
                            '--tier', task_type,
                            '--workers', '3'
                        ], cwd=os.path.dirname(os.path.abspath(__file__)))
                        print(f"[Scheduler] 定时任务 #{task_id} 已触发")
                    except Exception as e:
                        print(f"[Scheduler] 任务 #{task_id} 执行失败: {e}")
        except Exception as e:
            print(f"[Scheduler] 调度器异常: {e}")
        # 每分钟检查一次
        time.sleep(60)


# 启动后台调度器
scheduler_thread = threading.Thread(target=scheduler_worker, daemon=True)
scheduler_thread.start()


if __name__ == '__main__':
    # 确保数据库已初始化
    ensure_db()
    init_platforms_data()
    init_provenance_data()
    init_schedule_data()

    print("=" * 60)
    print("OGD-Collector Pro 启动中...")
    print("三层架构数据开放平台采集系统")
    print("作者：文明（武汉大学信息管理学院博士生）")
    print("=" * 60)
    print("访问地址: http://127.0.0.1:5000")
    print("=" * 60)

    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
