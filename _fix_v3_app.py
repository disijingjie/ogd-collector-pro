import sys

with open('/opt/ogd-collector-pro/v3_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 把/路由的v3_index.html改成v3_dashboard.html
old = "return render_template('v3_index.html',"
new = "return render_template('v3_dashboard.html',"

if old in content:
    content = content.replace(old, new, 1)  # 只替换第一个出现
    with open('/opt/ogd-collector-pro/v3_app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK')
else:
    print('NOT_FOUND')
    sys.exit(1)
