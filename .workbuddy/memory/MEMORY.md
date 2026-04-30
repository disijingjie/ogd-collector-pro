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

## 一键更新流程
当本地代码有变更时，执行以下步骤：

### 方式1：桌面脚本（推荐）
双击运行 `C:\Users\MI\Desktop\ogd-update.bat`

### 方式2：手动命令
```powershell
cd C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system
git add .
git commit -m "自动更新 $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push origin main
ssh ubuntu@106.53.188.187 "cd /opt/ogd-collector-pro && git pull origin main && sudo systemctl restart ogd-collector"
```

### 方式3：腾讯云控制台（备用）
1. 登录 https://console.cloud.tencent.com/lighthouse/instance
2. 找到实例 lhins-kyp9be3t → 一键登录
3. 执行：
```bash
cd /opt/ogd-collector-pro
git pull origin main
sudo systemctl restart ogd-collector
systemctl status ogd-collector --no-pager
```

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

## 部署架构（2026-04-28最终确定）

### 三个独立Flask应用
| 应用 | 端口 | WSGI | Nginx路由 | 管理方式 |
|:---|:---|:---|:---|:---|
| 旧版 | 5000 | wsgi.py | `/` | systemd (ogd-collector) |
| V3 | 5001 | v3_wsgi.py | `/v3/` | 手动gunicorn |
| V4 | 5002 | v4_wsgi.py | `/` | 手动gunicorn |

### 关键教训
1. **v3_app.py和app.py完全独立**：修改V3页面必须改v3_app.py，不是app.py
2. **gunicorn命令语法**：`PYTHONPATH=... timeout 5 cmd` 错误！必须用 `bash -c "export PYTHONPATH=... && cmd"`
3. **文件部署≠页面生效**：需确保路由正确 + gunicorn重启
4. **浏览器缓存**：static文件缓存30天，修改后按Ctrl+F5

### 部署文档
- 完整手册：`DEPLOYMENT_GUIDE.md`
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
- 2026-04-28: 用Playwright动态渲染成功采集安徽平台数据（36,300个开放目录），23个平台数据采集全部完成
- 2026-04-28: 部署架构彻底理清，编写DEPLOYMENT_GUIDE.md和桌面速查卡
- 2026-04-27: 视觉叙事规划完成，编制43张图清单，确立"Claude设计+Kimi执行"分工
- 2026-04-26: 博士论文v13完成，博导意见全面落实
- 2026-04-23: 配置SSH免密登录，创建一键更新脚本
