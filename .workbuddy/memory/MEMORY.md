# OGD-Collector Pro 项目记忆

## 用户
- 文明，武大信管院博士生 | 导师：陈传夫+冉从敬 | 邮箱：ambit@qq.com | 基金：21&ZD169
- 研究方向：OGD平台数据利用绩效评估 | 方法：TOPSIS/DEA/DEMATEL/fsQCA/多期DID

## 项目架构
- **系统代码**：`C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system\`（Git仓库，已部署）
- **论文文件**：`C:\Users\MI\WorkBuddy\newbbbb\` 根目录及子文件夹
- 系统数据反哺论文，23平台采集数据→4E评估→论文实证

## 服务器
- **IP**: 106.53.188.187 | Ubuntu 22.04 | 部署路径: /opt/ogd-collector-pro
- **SSH**: ubuntu@IP | 私钥: `C:\Users\MI\.ssh\id_ed25519` | 已免密
- **服务**: systemd ogd-collector | gunicorn@5000 | nginx反代80→5000
- **GitHub**: https://github.com/disijingjie/ogd-collector-pro
- **Cron**: 每日02:00省级采集 + 每周日06:00全量采集

## 部署方式
```powershell
# 推荐：Python一键部署
& "C:\Users\MI\AppData\Local\Programs\Python\Python315\python.exe" "_one_click_deploy.py"
# 单文件上传
& "...python.exe" "_one_click_deploy.py" "templates\v6_xxx.html"
```
- **⚠️ Windows坑**：SCP有bug→用SSH stdin; Git Bash有MSYS2 fork bug→用`C:\Program Files\Git\cmd\git.exe`或Python脚本
- **部署后必做**：gunicorn重启 + Ctrl+F5强制刷新 + 模板数校验

## V6架构（单实例）
| 应用 | 端口 | 管理 |
|:---|:---|:---|
| V6 | 5000 | systemd |

### 页面路由（34模板）
`/`首页 | `/collection`采集 | `/platform/<code>`详情 | `/analysis`分析 | `/thesis`论文 | `/research`研究 | `/literature`文献 | `/papers`小论文 | `/paper-collection`论文集 | `/credibility`可信度 | `/provenance`溯源 | `/rules`规则 | `/caliber`口径 | `/map`地图 | `/chen-chuanfu`陈传夫 | `/ran-congjing`冉从敬 | `/charts/{topsis,dematel,fsqa}`图表 | `/v3/*`→301重定向

### API路由（9个）
`/api/collection/{status,health,timeline}` | `/api/interlock/{map,check}` | `/api/literature/dedup` | `/api/platforms` | `/api/stats` | `/api/csv`

### Nginx优化
- Gzip: level 6, 7种类型, gzip_vary on
- 缓存: thesis_charts 30天 / fulltext 7天 / 其他 7天
- static权限: 755 (www-data可读)

## 23平台采集数据
| 平台 | 数量 | 方法 | 平台 | 数量 | 方法 |
|:---|---:|:---|:---|---:|:---|
| 广东 | 97,528 | 正则 | 四川 | 9,115 | 正则 |
| 山东 | 63,656 | 正则 | 贵州 | 9,042 | 计数器 |
| 浙江 | 38,000 | 发布会 | 福建 | 6,722 | CSS |
| 海南 | 35,835 | 正则 | 北京 | 4,454 | 正则 |
| 安徽 | 36,300 | Playwright | 辽宁 | 4,120 | 正则 |
| 湖北 | 24,119 | 正则 | 天津 | 3,344 | 报告 |
| 重庆 | 22,550 | 正则 | 湖南 | 634 | 正则 |
| 广西 | 10,162 | CSS | 江苏 | 644 | 新URL |
| 上海 | 10,753 | 官方 | 江西 | 534 | 正则 |
| | | | 山西 | 534 | 正则 |
| | | | 河南 | 931 | 产品页 |
| | | | 云南 | 428 | 登记页 |
| | | | 吉林 | 303 | 正则 |
| | | | 内蒙古 | 219 | 正则 |

## 论文关键经验
1. pandoc图片：必须`--embed-resources` + 相对路径
2. 引用优化：中英比67.6%:32.4%，删除低质量英文文献
3. 术语统一："数据利用绩效"

## 更新记录
- 2026-05-16: 6项优化部署+Nginx gzip_vary修复+静态文件403修复+Cron定时采集部署+服务器V3模板清理+gitignore大更新(80+规则)+git commit 7d5522c
- 2026-05-15: 口径声明页/D3地图/代码瘦身/DID图/Git快照(tag: v6-pre-optimization-20260515)
- 2026-05-09: V14论文全面审读修复
- 2026-05-03: 全面改版16页面+文献五件套
- 2026-05-02: V6单实例架构确立
- 2026-04-28: 23平台数据全完成(安徽Playwright突破)
- 2026-04-27: V25盲审版完成(258,844字符)
