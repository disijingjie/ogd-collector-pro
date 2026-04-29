"""
OGD-Collector Pro V8 - 完整版
博士论文支撑系统
"""
from flask import Flask, render_template, send_from_directory, jsonify
import os
import json

app = Flask(__name__,
    template_folder='templates',
    static_folder='static')

# ========== 核心页面 ==========

@app.route('/')
def index():
    """首页 - 系统概览"""
    return render_template('v3_dashboard.html')

@app.route('/collection')
def collection():
    """采集中心"""
    return render_template('v3_collection.html')

@app.route('/collection/dashboard')
def collection_dashboard():
    """采集看板"""
    return render_template('v3_collection_dashboard.html')

@app.route('/collection/mechanism')
def collection_mechanism():
    """采集机制"""
    return render_template('v3_collection_mechanism.html')

@app.route('/analysis')
def analysis():
    """分析看板"""
    return render_template('v3_analysis.html')

@app.route('/thesis')
def thesis():
    """论文成果"""
    return render_template('v3_thesis.html')

@app.route('/research')
def research():
    """研究拓展"""
    return render_template('v3_research.html')

@app.route('/reproduce')
def reproduce():
    """数据复现"""
    return render_template('v3_reproduce.html')

@app.route('/provenance')
def provenance():
    """数据溯源"""
    return render_template('v3_provenance.html')

@app.route('/preview')
def preview():
    """预览"""
    return render_template('v3_preview.html')

@app.route('/platforms')
def platforms():
    """平台列表"""
    return render_template('v3_platforms.html')

@app.route('/rules')
def rules():
    """规则映射表"""
    return render_template('v3_rules.html')

# ========== 图表页面 ==========

@app.route('/charts/topsis')
def chart_topsis():
    return render_template('v3_topsis_chart.html')

@app.route('/charts/dematel')
def chart_dematel():
    return render_template('v3_dematel_chart.html')

@app.route('/charts/fsqa')
def chart_fsqa():
    return render_template('v3_fsqa_chart.html')

# ========== 论文章节 (v4) ==========

@app.route('/thesis/ch1')
def thesis_ch1():
    return render_template('v4_thesis_ch1.html')

@app.route('/thesis/ch2')
def thesis_ch2():
    return render_template('v4_thesis_ch2.html')

@app.route('/thesis/ch3')
def thesis_ch3():
    return render_template('v4_thesis_ch3.html')

@app.route('/thesis/ch4')
def thesis_ch4():
    return render_template('v4_thesis_ch4.html')

@app.route('/thesis/ch5')
def thesis_ch5():
    return render_template('v4_thesis_ch5.html')

@app.route('/thesis/ch6')
def thesis_ch6():
    return render_template('v4_thesis_ch6.html')

@app.route('/thesis/ch7')
def thesis_ch7():
    return render_template('v4_thesis_ch7.html')

@app.route('/thesis/ch8')
def thesis_ch8():
    return render_template('v4_thesis_ch8.html')

@app.route('/thesis/index')
def thesis_index():
    return render_template('v4_thesis_index_v3.html')

# ========== API ==========

@app.route('/api/stats')
def api_stats():
    return jsonify({"status": "ok", "version": "v8"})

# ========== 静态文件 ==========

@app.route('/static/data/<path:filename>')
def download_data(filename):
    return send_from_directory('static/data', filename)

# ========== 运行 ==========

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)
