# OGD-Collector Pro 项目记忆

## 用户基本信息
- **用户**：文明，武汉大学信息管理学院博士生
- **研究方向**：政府数据开放平台数据资源利用的评价与优化
- **研究方法**：fsQCA、多期DID、政策评估、混合方法
- **目标期刊**：公共行政评论、管理世界、公共管理学报、图书情报工作、中国行政管理
- **邮箱**：ambit@qq.com
- **基金编号占位符**：21&ZDXXX（待替换）

## 项目整体架构（2026-04-30整理）
本项目包含论文和系统两大部分，**保持联动，系统数据反哺论文**：
- **论文文件**：位于 `C:\Users\MI\WorkBuddy\newbbbb\` 根目录（532个文件，260.py+141.md+75.docx）
- **系统代码**：位于 `C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system\`（Git仓库，已部署）
- **论文子文件夹**：gen_thesis/ whu-thesis/ 博士论文图表/ 武大博士论文格式材料/ 盲审意见/ 等
- **系统论文联动**：系统采集的23平台数据直接用于论文实证分析，4E评估结果写入论文

### 关键论文经验（从旧空间迁移）
1. **论文整合决策**：以V9为绝对主导，V31选择性补充；术语统一"数据利用绩效"
2. **图片嵌入**：pandoc必须用`--embed-resources`，图片路径必须是相对路径
3. **引用优化**：删除低质量英文文献+补充高质量中文文献，中英比67.6%:32.4%
4. **精修版章节**：7个精修版章节md文件在newbbbb根目录
5. **层级分化整改**：研究样本扩展为"三层架构31省"，新增四种"传导断裂"分析

## 服务器信息
- **IP**: 106.53.188.187
- **实例ID**: lhins-kyp9be3t
- **区域**: ap-guangzhou
- **系统**: Ubuntu 22.04
- **部署路径**: /opt/ogd-collector-pro
- **GitHub**: https://github.com/disijingjie/ogd-collector-pro

## SSH 配置
- **用户名**: ubuntu
- **密码**: wenming.890503（已配置免密登录）
- **公钥**: 已添加到服务器 ~/.ssh/authorized_keys
- **本地私钥**: C:\Users\MI\.ssh\id_ed25519

## 一键部署流程（2026-05-02 更新：已验证可行）

### 方法A：Python一键部署脚本（推荐）
```powershell
# 完整部署（git push + 服务器pull）
& "C:\Users\MI\AppData\Local\Programs\Python\Python315\python.exe" "_one_click_deploy.py"

# 只上传单个文件（绕过GitHub）
& "C:\Users\MI\AppData\Local\Programs\Python\Python315\python.exe" "_one_click_deploy.py" "templates\v6_xxx.html"
```

**脚本路径**：`_one_click_deploy.py`（项目根目录）

### 方法B：PowerShell直接上传（适合大文件）
```powershell
# 用Python + SSH stdin方式上传（绕过MSYS2 fork bug）
& "C:\Users\MI\AppData\Local\Programs\Python\Python315\python.exe" -c "
import subprocess, sys
content = open(r'模板路径','rb').read()
cmd = ['C:\\Program Files\\Git\\usr\\bin\\ssh.exe', 
     '-o','StrictHostKeyChecking=no','-i','C:\\Users\\MI\\.ssh\\id_ed25519',
     'ubuntu@106.53.188.187','cat > /opt/ogd-collector-pro/模板路径']
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
proc.communicate(input=content)
print('上传完成' if proc.returncode==0 else '失败')
"
```

### 方法C：旧桌面脚本（需要更新）
- `C:\Users\MI\Desktop\ogd-update.bat` 需要更新为V6专用版本

### 关键教训（已验证）
1. **Windows OpenSSH SCP有bug** → 改用 Python + SSH stdin
2. **Git Bash MSYS2 fork bug** → 用 `C:\Program Files\Git\cmd\git.exe` 或Python脚本
3. **PowerShell外部命令无输出** → 用 `Start-Process -RedirectStandardOutput`
4. **GitHub push失败** → 用Python脚本直接SSH上传文件



## 服务管理命令
```bash
# 查看状态
sudo systemctl status ogd-collector --no-pager

# 重启服务
sudo systemctl restart ogd-collector

# 查看日志
sudo journalctl -u ogd-collector --no-pager -n 50

# 测试访问
curl -s http://127.0.0.1:5000 | head -5
```

## 已知问题
- 腾讯云API密钥已失效（SecretId不存在），无法使用TAT自动化助手
- SSH免密登录已配置成功，是主要连接方式

## 论文版本记录
- 2026-04-27: 博士论文v25（顶级盲审专家点睛版）
  - 摘要重构：注入"数据口径幻觉"、"制度同形理论"、"fsQCA路径管理学内涵"
  - 方法论递进逻辑：第3章新增3.0节，解释TOPSIS→DEA→DEMATEL→fsQCA→DID的"破案"逻辑链条
  - 数据局限性讨论：第8.4节新增"下载量≠经济价值"的代理变量偏差讨论
  - 理论贡献强化：第8.2节新增第五项贡献（制度同形理论拓展到中国数据要素市场化语境）
  - 对策建议重构：第8.3节新增"政策内参摘要"板块，面向国家数据局的三条行动建议
  - 总字符：258,844 | Word文件：docs/博士论文_最终完整版_v25.docx（10.2MB）

- 2026-04-27: 博士论文v24（北大清华教授深度审稿版）
  - 第1-4章深度补充：新增20个章节/表格/图表，约+17,575字符
  - 新增理论：学科定位（IRM三次范式）、NPG新公共治理、制度同形三机制
  - 新增国际比较：美/英/爱沙尼亚/韩国四国深度案例 + 表2-4
  - 新增文献计量：WOS 2847篇+CNKI 3156篇三阶段演化
  - 新增6张图：图1-4政策时间轴、图2-7关键词共现、图2-8制度同形、图3-3整合框架、图4-5 DID设计、图4-6预处理流程
  - 总字符：255,156 | 图36张 | 表24张 | 参考文献56篇
  - 结构验证：21/21项ALL PASS
  - Word文件：docs/博士论文_最终完整版_v24.docx（10.2MB）
  - Markdown源文件：docs/博士论文_最终定稿版_v24.md（255,156字符）

- 2026-04-26: 博士论文v13（博导意见落实版）
  - 35条博导意见落实32条（91.4%）
  - 核心数据：23平台、山东0.955、DEA有效1个、DEMATEL网络化、fsQCA 2条路径
  - 新增理论内容：理论整合小节、制度同形分析、府际关系分析、DEA模型论证
  - 四向交叉核对通过
  - Word文件：docs/博士论文_最终完整版_v13.docx（1,399KB）
  - Markdown源文件：docs/博士论文_最终定稿版_v10.md（207,089字符）

## 论文图表工作流（2026-04-27确立）
- 图表制作采用"Claude出设计方案 → Kimi代码实现 → 用户确认"的分工模式
- Claude负责：布局设计、配色方案、工具选型建议
- Kimi负责：Python matplotlib代码生成、批量出图、Word嵌入
- 复杂图（流程图/网络图/SWOT）用draw.io/ProcessOn手工精做
- 全篇规划43张图，目标保留25-28张核心图
- 规划文档：`docs/_视觉叙事规划_图表清单_v1.md`
- Claude提示词：`docs/_Claude提示词_图表设计方案.md`

## 部署架构（2026-05-02最终确定：单实例V6）

### 架构变更历史
- **2026-04-28前**：三个独立Flask应用（旧版@5000、V3@5001、V4@5002），多端口混乱
- **2026-05-02**：**只保留单实例V6 @ 5000端口**，清理所有残留（V3/V4/V8进程全部杀死）

### 当前架构
| 应用 | 端口 | 路由 | 管理方式 |
|:---|:---|:---|:---|
| **V6** | **5000** | `/` | **systemd (ogd-collector)** |

- nginx：`location /` → `proxy_pass http://127.0.0.1:5000`
- static文件：`/opt/ogd-collector-pro/static`（nginx直接服务，30天缓存）

### V6完整路由表（2026-05-03更新）
| 路径 | 模板 | 说明 |
|:---|:---|:---|
| `/` | v6_index.html | 首页·采集状态总览 |
| `/collection`, `/dashboard` | v6_collection.html | 采集中心/数据看板 |
| `/platform/<code>` | v6_platform_detail.html | 平台详情 |
| `/analysis` | v6_analysis.html | 分析看板 |
| `/thesis` | v6_thesis.html | 论文成果 |
| `/research` | v6_research.html | 研究拓展 |
| `/literature` | v6_literature.html | 文献检索专题 |
| `/papers` | v6_papers.html | 小论文框架 |
| `/paper-collection` | v6_papers_showcase.html | 小论文集 |
| `/reproduce` | v6_reproduce.html | 数据复现 |
| `/provenance` | v6_provenance.html | 数据溯源 |
| `/rules` | v6_rules.html | 规则映射表 |
| `/charts/topsis` | v6_topsis_chart.html | TOPSIS图表 |
| `/charts/dematel` | v6_dematel_chart.html | DEMATEL图表 |
| `/charts/fsqa` | v6_fsqa_chart.html | fsQCA图表 |
| `/chen-chuanfu` | v6_chen_chuanfu.html | 陈传夫专题 |
| `/ran-congjing` | v6_ran_congjing.html | 冉从敬专题 |
| `/v3/*` | 301重定向 | 旧版路径自动跳转V6 |

### /v3/ 旧路径兼容方案（2026-05-03实现）
- 在 `v6_app.py` 中添加 9 条 301 重定向路由（`/v3/` → `/`, `/v3/research` → `/research` 等）
- 外加通配符 `@app.route('/v3/<path:dummy>')` 兜底所有未知路径 → 重定向到首页
- 所有模板内部链接已修正为 V6 格式（无 `/v3/` 残留）

### 关键教训
1. **只保留一套程序**：多端口/多版本是灾难，维护成本指数级增长
2. **v3_app.py和app.py完全独立**：修改V3页面必须改v3_app.py，不是app.py（历史教训）
3. **gunicorn命令语法**：`PYTHONPATH=... timeout 5 cmd` 错误！必须用 `bash -c "export PYTHONPATH=... && cmd"`
4. **文件部署≠页面生效**：需确保路由正确 + gunicorn重启 + **浏览器Ctrl+F5强制刷新**
5. **浏览器缓存**：static文件缓存30天，修改后必须按Ctrl+F5
6. **模板同步检查**：每次部署后确认服务器模板数 = 本地模板数（当前 17/17）

### 部署文档
- 运维手册：`V6运维手册.md`（2026-05-02新增，解决"AI失忆"痛点）
- 历史手册：`DEPLOYMENT_GUIDE.md`
- 桌面速查：`C:\Users\MI\Desktop\OGD-部署速查.txt`
- 同步脚本：`C:\Users\MI\Desktop\ogd-sync.py`

## 数据采集技术栈
- **静态爬取**：Requests + BeautifulSoup（适用于传统服务端渲染页面）
- **动态渲染**：Playwright + Chromium（适用于Vue.js/React等单页应用）
- **安徽平台案例**：首次使用Playwright成功采集Vue.js单页应用数据，证明系统可处理JavaScript动态渲染平台

## 23个平台数据采集状态（2026-04-28最终确认）

| 序号 | 平台 | 数据集/目录数 | 采集方法 | 置信度 |
|:---:|:---|:---:|:---|:---:|
| 1 | 广东 | 97,528 | 首页正则匹配 | 高 |
| 2 | 山东 | 63,656 | 首页正则匹配 | 高 |
| 3 | 浙江 | 38,000 | 政府发布会 | 高 |
| 4 | 海南 | 35,835 | 首页正则匹配 | 高 |
| 5 | 安徽 | **36,300** | **Playwright动态渲染** | **高** |
| 6 | 湖北 | 24,119 | 首页正则匹配 | 高 |
| 7 | 重庆 | 22,550 | 首页正则匹配 | 高 |
| 8 | 广西 | 10,162 | 数据目录页CSS | 高 |
| 9 | 上海 | 10,753 | 官方统计 | 高 |
| 10 | 四川 | 9,115 | 数据目录页正则 | 高 |
| 11 | 贵州 | 9,042 | 首页数字计数器 | 高 |
| 12 | 福建 | 6,722 | 首页CSS选择器 | 中 |
| 13 | 北京 | 4,454 | 首页正则匹配 | 高 |
| 14 | 辽宁 | 4,120 | 首页正则匹配 | 高 |
| 15 | 天津 | 3,344 | 官方报告 | 高 |
| 16 | 湖南 | 634 | 数据目录页正则 | 高 |
| 17 | 江苏 | 644 | 新URL访问 | 高 |
| 18 | 江西 | 534 | 首页正则匹配 | 高 |
| 19 | 山西 | 534 | 首页正则匹配 | 中 |
| 20 | 河南 | 931 | 产品中心页面 | 中 |
| 21 | 云南 | 428 | 登记中心页面 | 中 |
| 22 | 吉林 | 303 | 首页正则匹配 | 高 |
| 23 | 内蒙古 | 219 | 首页正则匹配 | 高 |

**注：安徽平台于2026-04-28首次使用Playwright动态渲染技术成功采集，解决了Vue.js单页应用的数据获取难题。**

## 更新记录
- 2026-05-09: **V14论文全面审读与修复**：完成P0/P1/P2三级问题修复（数据一致性、4E命名统一、数据溯源声明、脚注注入），构建最终版DOCX；建立论文与采集系统数据交叉验证机制
- 2026-05-08: V14论文生成（64篇PDF文献注入9处），审读报告识别14项问题，V14完整版+脚注版DOCX产出
- 2026-05-03: 全面改版（16页面200OK），文献五件套上线，方法论论文框架
- 2026-05-02: V6单实例架构确立，清理多版本残留
- 2026-04-28: 安徽平台Playwright采集成功(36,300)，23平台数据全完成，部署架构理清
- 2026-04-27: 视觉叙事规划，V24/V25论文版本迭代
- 2026-04-26: V13论文完成，博导意见落实91.4%
