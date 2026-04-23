#!/bin/bash
# OGD-Collector Pro 每日自动采集定时任务配置
# 用法: bash setup_cron.sh

echo "===== OGD-Collector Pro 定时任务配置 ====="

APP_DIR="/opt/ogd-collector-pro"
PYTHON="/usr/bin/python3"
LOG_DIR="$APP_DIR/logs"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

# 生成 crontab 内容
CRON_CONTENT="# OGD-Collector Pro 自动采集任务
# 每天凌晨2点执行全量采集
0 2 * * * cd $APP_DIR && $PYTHON auto_collect.py --tier full >> $LOG_DIR/cron.log 2>&1
# 每周一凌晨3点执行省级专项采集
0 3 * * 1 cd $APP_DIR && $PYTHON auto_collect.py --tier provincial >> $LOG_DIR/cron_provincial.log 2>&1
# 每周三凌晨3点执行副省级专项采集
0 3 * * 3 cd $APP_DIR && $PYTHON auto_collect.py --tier subprovincial >> $LOG_DIR/cron_subprovincial.log 2>&1
# 每周五凌晨3点执行地级市专项采集
0 3 * * 5 cd $APP_DIR && $PYTHON auto_collect.py --tier prefectural --workers 5 >> $LOG_DIR/cron_prefectural.log 2>&1
"

# 先删除旧的 OGD 定时任务
(crontab -l 2>/dev/null | grep -v "OGD-Collector" | grep -v "auto_collect") | crontab -

# 添加新的定时任务
(crontab -l 2>/dev/null; echo "$CRON_CONTENT") | crontab -

echo "[OK] 定时任务已配置"
echo ""
echo "任务计划:"
echo "  - 每天 02:00 执行全量采集"
echo "  - 每周一 03:00 执行省级专项采集"
echo "  - 每周三 03:00 执行副省级专项采集"
echo "  - 每周五 03:00 执行地级市专项采集"
echo ""
echo "当前 crontab:"
crontab -l | grep -A 20 "OGD-Collector"
