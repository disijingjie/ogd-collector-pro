import sys

# 1. 修改v3_dashboard.html
with open('/opt/ogd-collector-pro/templates/v3_dashboard.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('<div class="stat-value">23/23</div><div class="stat-label">省级数据采集覆盖</div>', 
              '<div class="stat-value">23</div><div class="stat-label">省级数据采集覆盖</div>')

with open('/opt/ogd-collector-pro/templates/v3_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('v3_dashboard.html OK')

# 2. 修改v3_app.py - 添加/collection路由
with open('/opt/ogd-collector-pro/v3_app.py', 'r', encoding='utf-8') as f:
    c = f.read()

if "@app.route('/collection')" not in c:
    # 在第一个路由后面添加/collection路由
    insert_after = "def index():"
    new_route = '''\n@app.route('/collection')\ndef collection():\n    return render_template('v3_collection.html')\n'''
    
    # 找到index函数定义的位置，在其前面添加新路由
    idx = c.find('@app.route(\'/\')')
    if idx != -1:
        c = c[:idx] + "@app.route('/collection')\ndef collection():\n    return render_template('v3_collection.html')\n\n" + c[idx:]
        with open('/opt/ogd-collector-pro/v3_app.py', 'w', encoding='utf-8') as f:
            f.write(c)
        print('v3_app.py OK')
    else:
        print('v3_app.py ROUTE_NOT_FOUND')
        sys.exit(1)
else:
    print('v3_app.py ALREADY_HAS_COLLECTION')
