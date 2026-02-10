#!/bin/bash
# 自动更新路线图脚本

CURRENT_TIME=$(date "+%Y-%m-%d %H:%M UTC+8")
START_TIME="2026-02-09 18:00"
CURRENT_EPOCH=$(date "+%s")
START_EPOCH=$(date -d "2026-02-09 18:00" "+%s")
ELAPSED_SECONDS=$((CURRENT_EPOCH - START_EPOCH))
ELAPSED_HOURS=$((ELAPSED_SECONDS / 3600))
ELAPSED_MINUTES=$(((ELAPSED_SECONDS % 3600) / 60))
ELAPSED="${ELAPSED_HOURS}小时${ELAPSED_MINUTES}分钟"

# 更新文件
sed -i "s/当前时间: .*/当前时间: $CURRENT_TIME/" RESEARCH_ROADMAP_v3.0.md
sed -i "s/已执行: .*/已执行: $ELAPSED/" RESEARCH_ROADMAP_v3.0.md
sed -i "s/总执行时间: .*/总执行时间: $ELAPSED/" RESEARCH_ROADMAP_v3.0.md

echo "✓ 路线图已更新: $CURRENT_TIME, 已执行: $ELAPSED"
