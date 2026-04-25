"""
V3 WSGI入口文件
用于Gunicorn部署
"""
from v3_app import app

if __name__ == "__main__":
    app.run()
