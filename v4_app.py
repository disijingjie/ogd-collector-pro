"""
OGD-Collector Pro V4 - 论文全场景展示系统
Author: OGD-Collector Team
Version: 4.0.0
Date: 2026-04-25
Description: 博士论文全场景采集与展示系统
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import os

app = Flask(__name__)

# ============== 数据加载 ==============

def load_json(filepath):
    """安全加载JSON文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}

def load_csv(filepath):
    """安全加载CSV文件"""
    try:
        import pandas as pd
        return pd.read_csv(filepath).to_dict('records')
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return []

# ============== 全局数据 ==============

COLLECTION_RESULTS = load_json('data/v3_collection_results.json')
PLATFORM_RULES = load_json('v3_platform_rules.json')
TOPSIS_RESULTS = load_csv('data/v3_topsis_results_v2.csv')
DEA_RESULTS = load_csv('data/v3_dea_results.csv')
DEMATEL_RESULTS = load_csv('data/v3_dematel_results.csv')
FSQCA_RESULTS = load_csv('data/v3_fsqca_results.csv')

# ============== V4 路由 - 论文全场景展示 ==============

@app.route('/thesis/')
def thesis_index():
    """论文展示首页"""
    return render_template('v4_thesis_index.html')

@app.route('/thesis/ch1')
def thesis_ch1():
    """第一章 绪论"""
    return render_template('v4_thesis_ch1.html')

@app.route('/thesis/ch2')
def thesis_ch2():
    """第二章 文献综述"""
    return render_template('v4_thesis_ch2.html')

@app.route('/thesis/ch3')
def thesis_ch3():
    """第三章 4E框架"""
    return render_template('v4_thesis_ch3.html')

@app.route('/thesis/ch4')
def thesis_ch4():
    """第四章 研究设计 - 一平台一议策略库"""
    platforms = PLATFORM_RULES.get('platforms', {})
    return render_template('v4_thesis_ch4.html', platforms=platforms)

@app.route('/thesis/ch5')
def thesis_ch5():
    """第五章 绩效评估 - TOPSIS/DEA/区域对比"""
    return render_template('v4_thesis_ch5.html', 
                         topsis=TOPSIS_RESULTS,
                         dea=DEA_RESULTS)

@app.route('/thesis/ch6')
def thesis_ch6():
    """第六章 影响因素 - DEMATEL/fsQCA"""
    return render_template('v4_thesis_ch6.html',
                         dematel=DEMATEL_RESULTS,
                         fsqca=FSQCA_RESULTS)

@app.route('/thesis/ch7')
def thesis_ch7():
    """第七章 对策建议 - 转型追踪"""
    return render_template('v4_thesis_ch7.html')

@app.route('/thesis/ch8')
def thesis_ch8():
    """第八章 结论"""
    return render_template('v4_thesis_ch8.html')

# ============== API 接口 ==============

@app.route('/api/v4/stats')
def api_v4_stats():
    """V4统计信息"""
    return jsonify({
        'version': '4.0.0',
        'total_platforms': 31,
        'valid_samples': 22,
        'high_performance': 11,
        'low_performance': 11,
        'transformed': 3,
        'no_platform': 8,
        'total_datasets': 343217,
        'avg_datasets': 15601,
        'data_source': 'OGD-Collector Pro V3.5',
        'server': '腾讯云 106.53.188.187'
    })

@app.route('/api/v4/topsis')
def api_v4_topsis():
    """TOPSIS结果API"""
    return jsonify(TOPSIS_RESULTS)

@app.route('/api/v4/dea')
def api_v4_dea():
    """DEA结果API"""
    return jsonify(DEA_RESULTS)

@app.route('/api/v4/dematel')
def api_v4_dematel():
    """DEMATEL结果API"""
    return jsonify(DEMATEL_RESULTS)

@app.route('/api/v4/fsqca')
def api_v4_fsqca():
    """fsQCA结果API"""
    return jsonify(FSQCA_RESULTS)

@app.route('/api/v4/platforms')
def api_v4_platforms():
    """平台详细信息API"""
    return jsonify(PLATFORM_RULES)

# ============== 静态文件 ==============

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# ============== 主入口 ==============

@app.route('/')
def index():
    """V4主入口 - 论文展示系统"""
    return render_template('v4_thesis_index.html')

# ============== 错误处理 ==============

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)
