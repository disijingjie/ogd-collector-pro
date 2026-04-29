"""
OGD-Collector Pro V8 - 简化版
博士论文支撑系统
"""
from flask import Flask, render_template, send_from_directory
import os

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

# ========== 静态文件 ==========

@app.route('/static/data/<path:filename>')
def download_data(filename):
    return send_from_directory('static/data', filename)

# ========== 运行 ==========

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)
