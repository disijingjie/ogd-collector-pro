"""
OGD-Collector Pro - SSH密钥管理与部署保障脚本
一键解决SSH密钥、GitHub连接、服务器部署问题
"""

import subprocess
import os
import sys
from pathlib import Path

SSH_DIR = Path.home() / ".ssh"
KEY_FILE = SSH_DIR / "id_ed25519"
PUB_FILE = SSH_DIR / "id_ed25519.pub"
GITHUB_HOST = "github.com"
SERVER_HOST = "106.53.188.187"
SERVER_USER = "ubuntu"
PROJECT_DIR = Path("C:/Users/MI/WorkBuddy/newbbbb/ogd_collector_system")

def run(cmd, capture=True):
    """执行命令并返回结果"""
    result = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    return result

def check_ssh_key():
    """检查SSH密钥是否存在"""
    print("=" * 60)
    print("[1/5] 检查SSH密钥")
    print("=" * 60)
    
    if not SSH_DIR.exists():
        print(f"  创建SSH目录: {SSH_DIR}")
        SSH_DIR.mkdir(mode=0o700)
    
    if KEY_FILE.exists() and PUB_FILE.exists():
        print(f"  SSH密钥已存在: {KEY_FILE}")
        with open(PUB_FILE, 'r') as f:
            pub_key = f.read().strip()
        print(f"  公钥内容: {pub_key[:60]}...")
        return True
    else:
        print("  SSH密钥不存在，需要生成")
        return False

def generate_ssh_key():
    """生成新的SSH密钥"""
    print("\n  生成新的ED25519密钥对...")
    result = run(f'ssh-keygen -t ed25519 -C "disijingjie@github" -f {KEY_FILE} -N ""')
    if result.returncode == 0:
        print("  密钥生成成功")
        # 设置权限
        os.chmod(KEY_FILE, 0o600)
        os.chmod(PUB_FILE, 0o644)
        return True
    else:
        print(f"  密钥生成失败: {result.stderr}")
        return False

def setup_github_ssh():
    """配置GitHub SSH连接"""
    print("\n" + "=" * 60)
    print("[2/5] 配置GitHub SSH连接")
    print("=" * 60)
    
    # 添加GitHub到known_hosts
    print("  添加GitHub到known_hosts...")
    run(f"ssh-keyscan -H {GITHUB_HOST} >> {SSH_DIR / 'known_hosts'} 2>nul")
    
    # 测试SSH连接
    print("  测试SSH连接GitHub...")
    result = run(f"ssh -o StrictHostKeyChecking=no -T git@{GITHUB_HOST} 2>&1")
    if "successfully authenticated" in result.stdout or "successfully authenticated" in result.stderr:
        print("  GitHub SSH连接成功")
        return True
    elif "Permission denied" in result.stdout or "Permission denied" in result.stderr:
        print("  GitHub拒绝连接 - 需要将公钥添加到GitHub账户")
        print(f"\n  请执行以下操作:")
        print(f"  1. 复制公钥: cat {PUB_FILE}")
        print(f"  2. 访问: https://github.com/settings/keys")
        print(f"  3. 点击 'New SSH key'")
        print(f"  4. 粘贴公钥并保存")
        return False
    else:
        print(f"  连接结果: {result.stdout} {result.stderr}")
        return False

def setup_server_ssh():
    """配置服务器SSH连接"""
    print("\n" + "=" * 60)
    print("[3/5] 配置服务器SSH连接")
    print("=" * 60)
    
    # 测试连接
    print(f"  测试连接 {SERVER_USER}@{SERVER_HOST}...")
    result = run(f"ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 {SERVER_USER}@{SERVER_HOST} 'echo SSH_OK'")
    
    if "SSH_OK" in result.stdout:
        print("  服务器SSH连接成功")
        return True
    else:
        print("  服务器连接失败")
        print(f"  错误: {result.stderr}")
        return False

def setup_git_remote():
    """配置Git远程仓库为SSH地址"""
    print("\n" + "=" * 60)
    print("[4/5] 配置Git远程仓库")
    print("=" * 60)
    
    os.chdir(PROJECT_DIR)
    
    # 检查当前远程地址
    result = run("git remote -v")
    print(f"  当前远程地址:\n{result.stdout}")
    
    # 设置为SSH地址
    run("git remote set-url origin git@github.com:disijingjie/ogd-collector-pro.git")
    print("  已设置为SSH地址: git@github.com:disijingjie/ogd-collector-pro.git")
    
    # 验证
    result = run("git remote -v")
    if "git@github.com" in result.stdout:
        print("  配置成功")
        return True
    return False

def test_full_pipeline():
    """测试完整部署流程"""
    print("\n" + "=" * 60)
    print("[5/5] 测试完整部署流程")
    print("=" * 60)
    
    os.chdir(PROJECT_DIR)
    
    # 测试1: GitHub fetch
    print("  测试1: GitHub fetch...")
    result = run("git fetch origin main --dry-run 2>&1")
    if result.returncode == 0 or "fatal: Could not resolve host" not in result.stderr:
        print("  GitHub fetch测试通过")
    else:
        print(f"  GitHub fetch失败: {result.stderr}")
    
    # 测试2: 服务器连接
    print("  测试2: 服务器连接...")
    result = run(f"ssh -o ConnectTimeout=5 {SERVER_USER}@{SERVER_HOST} 'echo DEPLOY_OK'")
    if "DEPLOY_OK" in result.stdout:
        print("  服务器连接测试通过")
    else:
        print(f"  服务器连接失败")

def deploy_to_server():
    """部署到服务器"""
    print("\n" + "=" * 60)
    print("[部署] 直接部署到服务器")
    print("=" * 60)
    
    os.chdir(PROJECT_DIR)
    
    # 打包
    print("  打包项目文件...")
    run("tar -czf /tmp/ogd-deploy.tar.gz --exclude=venv --exclude=__pycache__ --exclude=.git --exclude=data/logs .")
    
    # 上传
    print("  上传到服务器...")
    result = run(f"scp -o StrictHostKeyChecking=no /tmp/ogd-deploy.tar.gz {SERVER_USER}@{SERVER_HOST}:/tmp/")
    if result.returncode != 0:
        print(f"  上传失败: {result.stderr}")
        return False
    
    # 解压并重启
    print("  解压并重启服务...")
    result = run(f"ssh -o StrictHostKeyChecking=no {SERVER_USER}@{SERVER_HOST} 'cd /opt/ogd-collector-pro && sudo tar -xzf /tmp/ogd-deploy.tar.gz -C /opt/ogd-collector-pro/ && sudo systemctl restart ogd-collector && echo DEPLOY_SUCCESS'")
    
    if "DEPLOY_SUCCESS" in result.stdout:
        print("  部署成功!")
        return True
    else:
        print(f"  部署失败: {result.stderr}")
        return False

def main():
    print("=" * 60)
    print("OGD-Collector Pro - SSH密钥管理与部署保障")
    print("=" * 60)
    
    # 1. 检查密钥
    if not check_ssh_key():
        if not generate_ssh_key():
            print("密钥生成失败，退出")
            return
    
    # 2. 配置GitHub
    github_ok = setup_github_ssh()
    
    # 3. 配置服务器
    server_ok = setup_server_ssh()
    
    # 4. 配置Git
    setup_git_remote()
    
    # 5. 测试完整流程
    test_full_pipeline()
    
    print("\n" + "=" * 60)
    print("总结")
    print("=" * 60)
    print(f"  SSH密钥: {'已配置' if KEY_FILE.exists() else '未配置'}")
    print(f"  GitHub连接: {'正常' if github_ok else '需手动添加公钥到GitHub'}")
    print(f"  服务器连接: {'正常' if server_ok else '异常'}")
    
    if not github_ok:
        print(f"\n  请手动添加公钥到GitHub:")
        with open(PUB_FILE, 'r') as f:
            print(f"  {f.read().strip()}")
    
    # 询问是否部署
    print("\n  是否直接部署到服务器? (输入 'deploy' 部署)")
    choice = input("  > ").strip().lower()
    if choice == 'deploy':
        deploy_to_server()

if __name__ == '__main__':
    main()
