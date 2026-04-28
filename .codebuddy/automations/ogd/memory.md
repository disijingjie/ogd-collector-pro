# OGD 自动更新执行记录

## 2026-04-29 01:48
- **状态**: GitHub推送成功，服务器git pull失败（GitHub 443连接超时），服务运行正常
- **本地提交**: 成功（commit 3bbf338，1个文件变更，+77行）
  - .workbuddy/memory/2026-04-29.md（每日工作记忆文件）
- **GitHub推送**: 第1次尝试成功（9af0d88..3bbf338）
- **服务器SSH**: 正常连接
- **服务器git pull**: 失败
  - GitHub 443端口连接超时（130秒），与2026-04-26以来持续存在的网络问题一致
- **服务状态**: 运行中（自2026-04-29 01:51:55 CST起，HTTP 302正常，内存120.9M）
- **服务器当前版本**: 9af0d88（2026-04-28 23:56），与本地最新（3bbf338）存在差异
- **本次变更影响评估**: 仅涉及工作记忆文件（.workbuddy/memory/2026-04-29.md），不涉及核心服务代码
- **结论**: GitHub推送成功，但服务器端GitHub持续不可达。本次变更仅为工作记忆文件，不影响OGD采集服务运行。服务器代码与GitHub远程仍存在差异，建议网络恢复后手动同步。

## 2026-04-28 18:58
- **状态**: GitHub推送失败（网络问题），本地已提交，服务器运行正常
- **本地提交**: 成功（commit 77085b6，30个文件变更，+1981行/-246行）
  - 新增：论文投稿包（CoverLetter×5 + 投稿版docx×6）、投稿指南、操作手册
  - 新增：采集脚本（_check_actions.py, _generate_cover_letter.py, collect_anhui_playwright.py）
  - 新增：数据文件（_actions.json, _jobs.json, _logs.zip等）
  - 修改：6篇论文初稿（A-F）、md转docx脚本、内存文件
- **GitHub推送**: 3次重试均失败
  - 第1次：SSH权限拒绝（publickey），已切换为HTTPS
  - 第2次：Recv failure: Connection was reset
  - 第3次：Couldn't connect to server（连接超时21秒）
- **服务器SSH**: 正常连接
- **服务器git pull**: 失败，服务器端GitHub同样不可达（GnuTLS recv error -110）
- **服务器当前版本**: 88bed356（2026-04-28 16:56），与本地最新（77085b6）存在差异
- **服务状态**: 运行中（自2026-04-28 22:32:00 CST起，已运行约2小时，HTTP 302正常，内存121.1M）
- **本次变更影响评估**: 主要为论文文档和投稿材料（docs目录），不涉及核心服务代码（app.py/models.py/collector_engine.py等未变更）
- **结论**: GitHub网络问题持续，本地代码已提交（77085b6）但未同步到GitHub和服务器。由于本次变更主要是论文文档和投稿材料，不影响OGD采集服务运行。建议：1) 等待网络恢复后手动补推GitHub；2) 如需紧急同步论文文件到服务器，可使用SCP直接上传docs目录。

## 2026-04-28 16:56
- **状态**: GitHub推送成功，服务器代码更新成功，服务已恢复
- **本地提交**: 成功（commit 88bed35，6个文件变更，+71行/-84行）
  - 新增：5篇小论文投稿包完整版、6篇论文初稿（A-F）、v3采集日志
  - 修改：数据库、平台数据源文档、采集日志、flask错误日志、模板
- **GitHub推送**: 第1次尝试成功（be795d7..88bed35）
- **服务器SSH**: 正常连接
- **服务器git pull**: 成功（0cc738a9 → 88bed356），Fast-forward，14文件变更，+4237行/-158行
- **服务重启**: 成功（2026-04-28 16:57:21 CST）
  - gunicorn 25.3.0正常启动，2个worker已就绪
  - 内存占用120.9M，HTTP 302正常
- **服务状态**: 运行中（HTTP 302正常，5000端口正常）
- **结论**: 本地→GitHub→服务器全链路同步完成。服务器代码已更新，新增论文文件和模板已部署。

## 2026-04-28 01:42
- **状态**: GitHub推送成功，服务器代码更新成功，服务已恢复
- **本地提交**: 成功（commit 9a8cd33，1110个文件变更，+382,819行）
  - 新增：v25论文版本（Word）、6个论文修订脚本、venv_local虚拟环境
  - 修改：app.py, app_v2.py, v24 Markdown, 内存文件
  - 新增模板：v2_collection_flow.html, v2_index.html, v2_thesis.html
- **GitHub推送**: 第1次尝试成功（5267123..9a8cd33）
- **服务器SSH**: 正常连接
- **服务器git pull**: 成功（24b8b29d → 9a8cd338），Fast-forward
- **服务重启**: 成功（2026-04-28 01:42:55 CST）
  - gunicorn 25.3.0正常启动，2个worker已就绪
  - 内存占用122.5M，HTTP 302正常
- **服务状态**: 运行中（HTTP 302正常，5000端口正常）
- **结论**: 本地→GitHub→服务器全链路同步完成。服务器代码已更新至v25版本，新增论文文件和模板已部署。

## 2026-04-27 22:17
- **状态**: GitHub推送成功，服务器代码更新成功，服务已恢复
- **本地提交**: 成功（commit 24b8b29，55个文件变更，+27,682行）
  - 新增：v20-v24论文版本、图表修复脚本、静态图表文件
  - 修改：数据库、现有图表、内存文件
- **GitHub推送**: 第1次尝试成功（1e338f1..24b8b29）
- **服务器SSH**: 正常连接
- **服务器git pull**: 成功（265ee55e → 24b8b29d）
  - 耗时约3分20秒，fetch阶段较慢但成功完成
- **服务重启**: 成功（2026-04-27 23:58:36 CST）
  - 问题：venv目录结构变更（Windows格式Scripts/而非bin/），导致systemd配置中gunicorn路径失效
  - 修复：修改systemd服务文件，使用系统Python + 用户本地gunicorn + PYTHONPATH
  - 最终配置：ExecStart=/usr/bin/python3 /home/ubuntu/.local/bin/gunicorn wsgi:app
- **服务状态**: 运行中（HTTP 302正常，5000/5001/5002/80全部正常）
- **结论**: 本地→GitHub→服务器全链路同步完成。服务器代码已更新至v24版本，新增图表和论文文件已部署。

## 2026-04-26 09:56
- **状态**: GitHub推送成功，服务器端GitHub不可达（仅内存文件变更，无需部署）
- **本地提交**: 成功（commit 16ff990，1个文件变更，+13行）
  - .codebuddy/automations/ogd/memory.md（自动化内存文件）
- **GitHub推送**: 第1次尝试成功
  - 5cd1599..16ff990  main -> main
- **服务器SSH**: 正常连接
- **服务器git pull**: 失败
  - GnuTLS recv error (-110): The TLS connection was non-properly terminated
- **服务状态**: 运行中（自2026-04-26 09:58:28 CST起，HTTP 302正常）
- **结论**: 本地与GitHub远程已同步（16ff990）。服务器端GitHub持续不可达，但本次变更仅涉及自动化内存文件，不影响服务运行。服务器代码与GitHub远程仍存在差异，建议网络恢复后手动同步。

## 2026-04-26 03:32
- **状态**: 无需更新（本地无变更，已与GitHub远程同步）
- **本地commit**: 5cd1599 (2026-04-26 02:08, 用真实数据更新论文核心表格)
- **远程commit**: 5cd1599b8a128fc6a8af5f4e991af39524ded3e4
- **本地变更**: 无（working tree clean）
- **服务器状态**: 运行中（自2026-04-26 02:08:47 CST起，已运行1.5小时，HTTP 302正常）
- **服务器代码**: bc7e67d（2026-04-24 12:22，服务器端临时提交），与GitHub远程不同步
- **服务器git pull**: 3次重试均失败
  - 第1次：GnuTLS recv error (-110): The TLS connection was non-properly terminated
  - 第2次：Connection timed out（130秒）
  - 第3次：Connection timed out（129秒）
- **结论**: 本地与GitHub远程已完全同步，无需执行git push。服务器端GitHub持续不可达（TLS连接被终止/超时），但服务运行正常。服务器代码（bc7e67d）与GitHub远程（5cd1599）存在差异，建议网络恢复后手动同步。

## 2026-04-25 18:39
- **状态**: GitHub推送失败（网络问题），本次变更仅自动化内存文件，无需部署
- **本地提交**: 成功（commit e27fb3d，1个文件变更，+60行/-1行）
  - .workbuddy/memory/2026-04-25.md（自动化内存文件）
- **GitHub推送**: 3次重试均失败
  - 第1次：Connection was reset
  - 第2次：Connection was reset
  - 第3次：Couldn't connect to server（连接超时21秒）
- **服务器SSH**: 正常连接
- **服务状态**: 运行中（自2026-04-25 15:21:03 CST起，已运行3小时20分钟，HTTP 302正常）
- **结论**: 本次变更仅涉及自动化内存文件，不影响服务运行。GitHub网络问题持续，建议等待网络恢复后手动补推。

## 2026-04-25 13:13
- **状态**: 无需更新（本地无变更，已与远程同步）
- **本地commit**: ff4d236 (2026-04-25 12:50, V3.3: 22/23平台确认+全套计算+论文第五章框架+8张图表)
- **远程commit**: ff4d236bfc0b03a86edb284ba34e9db9864b737c
- **本地变更**: 无（working tree clean）
- **结论**: 本地与GitHub远程已完全同步，无需执行git push或服务器部署

## 2026-04-24 10:20
- **状态**: GitHub推送失败（Push Protection拦截），已通过SCP直接部署到服务器
- **本地提交**: 成功（commit c115387，5个文件变更，+843行/-34行）
  - app.py, models.py, auto_collect.py, collector_engine.py
  - templates/collector.html, dashboard.html, thesis.html
- **GitHub推送**: 3次重试均失败
  - 原因：GitHub Push Protection检测到历史commit中包含腾讯云Secret ID（docs/txcloud.py）
  - 与之前多次失败原因相同，需用户清理历史commit中的secret
- **服务器SSH**: 正常连接
- **SCP部署**: 成功上传所有变更文件（Python核心文件 + templates + static）
- **服务重启**: 成功（2026-04-24 10:20:24 CST，HTTP 302正常）
- **结论**: 代码已通过SCP直接部署到服务器，服务运行正常。GitHub推送仍被安全策略拦截，需用户处理历史commit中的secret问题。

## 2026-04-24 06:20
- **状态**: GitHub推送失败（网络问题），服务器服务运行正常
- **本地提交**: 成功（commit 3f40843，11个文件变更，+2849行/-627行）
- **GitHub推送**: 3次重试均失败
  - 第1次：Connection was reset
  - 第2次：Couldn't connect to server（连接超时21秒）
  - 第3次：Connection was reset
- **服务器SSH**: 正常连接
- **服务器git pull**: 成功但Already up to date（服务器端GitHub可达，但无新commit）
- **服务状态**: 运行中（自2026-04-24 05:01:14 CST起，已运行1小时20分钟，HTTP 302正常）
- **问题发现**: 服务器日志显示dashboard.html存在`checksums`未定义错误（jinja2.exceptions.UndefinedError），但不影响首页访问
- **结论**: 本地代码已提交（commit 3f40843），但GitHub推送失败。服务器端GitHub可达，但拉取不到新代码（因为本地未推送到GitHub）。本次变更是较大更新（dashboard.html重写、index.html优化、app.py和models.py修改），需尽快同步到服务器。建议：1) 等待网络恢复后手动推送GitHub；2) 或使用SCP直接部署到服务器。

## 2026-04-24 04:15
- **状态**: GitHub推送失败（网络问题），服务器服务运行正常
- **本地提交**: 成功（commit bb6a67a，1个文件变更，+11行）
- **GitHub推送**: 3次重试均失败
  - 第1次：Connection was reset
  - 第2次：Couldn't connect to server（连接超时21秒）
  - 第3次：Connection was reset
- **服务器SSH**: 正常连接
- **服务器git pull**: 失败，GitHub TLS连接被终止（与本地同样网络问题）
- **服务状态**: 运行中（自2026-04-23 23:42:08 CST起，已运行4小时37分钟，HTTP 302正常）
- **结论**: 本地代码已提交（commit bb6a67a），但GitHub推送失败。服务器端GitHub同样不可达，无法git pull。由于本次变更仅涉及自动化内存文件（.codebuddy/automations/ogd/memory.md），不影响服务运行。待网络恢复后需手动补推GitHub并同步服务器。

## 2026-04-23 23:36
- **状态**: GitHub推送失败（Push Protection拦截），已通过SCP直接部署到服务器
- **本地提交**: 成功（commit ff49b84，5个文件变更，+276行/-43行）
- **GitHub推送**: 3次重试均失败
  - 第1次：SSL连接超时
  - 第2-3次：GitHub Push Protection拦截，检测到历史commit中包含腾讯云Secret ID（docs/txcloud.py）
- **服务器SSH**: 正常连接
- **SCP部署**: 成功上传 app.py, models.py, auto_collect.py, setup_cron.sh, templates/, static/
- **服务重启**: 成功（2026-04-23 23:42:08 CST，HTTP 302正常）
- **结论**: 代码已通过SCP直接部署到服务器，服务运行正常。GitHub推送仍需用户手动清理历史commit中的secret后重推。

## 2026-04-23 21:29
- **状态**: GitHub推送失败（Secret泄露保护），服务器端GitHub连接超时
- **本地提交**: 成功（commit 42b0f8d，4个文件变更，+283行/-9行）
- **GitHub推送**: 3次重试均失败，GitHub Push Protection拦截，检测到历史commit中包含腾讯云Secret ID（docs/txcloud.py）
- **服务器SSH**: 正常连接
- **服务器git pull**: 失败，GitHub SSL连接超时
- **服务状态**: 运行中（已重启于21:35:16，HTTP 302正常）
- **结论**: GitHub推送被安全策略拦截，且服务器端GitHub不可达。当前代码仅本地提交，未同步到GitHub和服务器。需用户处理：1) 清理历史commit中的secret后重推；2) 或改用SCP直接部署到服务器。

## 2026-04-23 19:26
- **状态**: GitHub推送失败（网络问题），服务已通过SCP修复并恢复
- **本地提交**: 成功（commit f979fe4，修复重复函数定义）
- **GitHub推送**: 3次重试均失败，连接被重置/超时
- **问题发现**: app.py 存在重复的 `api_monitoring_health` 函数定义，导致 gunicorn Worker 启动失败（502 Bad Gateway）
- **修复方式**: 删除第786-810行的旧版函数，保留增强版（887行起）
- **部署方式**: SCP直接上传修复后的app.py到服务器
- **服务状态**: 已重启并恢复正常（HTTP 302，重定向到登录页）
- **结论**: 服务已恢复。GitHub仍不可达，代码仅本地提交+SCP部署，待网络恢复后需补推GitHub。

## 2026-04-23 15:11
- **状态**: GitHub推送失败，服务器端GitHub连接超时
- **本地提交**: 成功（commit da15510，8个文件变更，+1129行）
- **GitHub推送**: 3次重试均失败，连接被重置/超时
- **服务器SSH**: 正常连接
- **服务器git pull**: 失败，GitHub 443端口连接超时
- **服务状态**: 运行中（已重启于15:18:17）
- **结论**: 网络问题导致GitHub不可达，代码已本地提交但未同步到GitHub和服务器。需用户手动处理或等待网络恢复后重试。
