#!/bin/bash
# OGD-Collector Pro 定时采集cron设置
# 每日02:00自动采集省级平台，每周日06:00全量采集

# 确保日志目录存在
mkdir -p /opt/ogd-collector-pro/logs

# 添加crontab（不覆盖已有的）
(crontab -l 2>/dev/null; echo "# OGD-Collector Pro 定时采集"; echo "0 2 * * * cd /opt/ogd-collector-pro && /usr/bin/python3 auto_collect.py --tier provincial >> /opt/ogd-collector-pro/logs/auto_collect.log 2>&1"; echo "0 6 * * 0 cd /opt/ogd-collector-pro && /usr/bin/python3 auto_collect.py --tier full >> /opt/ogd-collector-pro/logs/auto_collect_full.log 2>&1") | crontab -

echo "Crontab设置完成！"
crontab -l
