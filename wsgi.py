"""
WSGI入口文件
用于Render/Vercel等PaaS平台部署
"""
from app import app

if __name__ == "__main__":
    app.run()
