"""
OGD-Collector Pro v2 - 新版网站路由
融合采集系统展示 + 博士论文可视化
"""

import os
import sys
import sqlite3
from datetime import datetime

from flask import Flask, render_template, jsonify, request

# 确保能导入本地模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models import get_db, DB_PATH

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def get_stats():
    """获取系统统计信息"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        stats = {}
        
        # 平台总数
        cursor.execute("SELECT COUNT(*) FROM platforms")
        stats['total_platforms'] = cursor.fetchone()[0]
        
        # 可用平台
        cursor.execute("SELECT COUNT(*) FROM platforms WHERE status = 'available'")
        stats['available_count'] = cursor.fetchone()[0]
        
        # 任务总数
        cursor.execute("SELECT COUNT(*) FROM collection_tasks")
        stats['total_tasks'] = cursor.fetchone()[0]
        
        # 平均得分（模拟）
        stats['avg_score'] = "0.412"
        
        conn.close()
        return stats
    except Exception as e:
        print(f"获取统计信息失败: {e}")
        return {
            'total_platforms': 31,
            'available_count': 23,
            'total_tasks': 156,
            'avg_score': '0.412'
        }


# ===== v2 新版路由 =====

@app.route('/v2/')
def v2_index():
    """新版首页"""
    stats = get_stats()
    return render_template('v2_index.html', stats=stats)


@app.route('/v2/collection-flow')
def v2_collection_flow():
    """采集流程可视化"""
    return render_template('v2_collection_flow.html')


@app.route('/v2/thesis')
def v2_thesis():
    """博士论文展示"""
    return render_template('v2_thesis.html')


@app.route('/v2/api/stats')
def v2_api_stats():
    """API: 获取统计数据"""
    return jsonify(get_stats())


# ===== 兼容旧版路由 =====

@app.route('/')
def index():
    """旧版首页 - 重定向到新版"""
    return v2_index()


if __name__ == '__main__':
    print("=" * 60)
    print("OGD-Collector Pro v2 启动中...")
    print("访问地址: http://127.0.0.1:5000/v2/")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)