#!/bin/bash
# Sokoban Game - 一键推送 GitHub 脚本

set -e

REPO_URL=""

# 检查是否已设置远程仓库
if git remote get-url origin &>/dev/null; then
    REPO_URL=$(git remote get-url origin)
    echo "✅ 远程仓库已配置：$REPO_URL"
else
    echo "❌ 未配置远程仓库"
    echo ""
    echo "请先在 GitHub 创建仓库，然后运行："
    echo "  git remote add origin <你的仓库地址>"
    echo ""
    echo "例如："
    echo "  git remote add origin https://github.com/你的用户名/sokoban-game.git"
    echo ""
    exit 1
fi

# 检查是否有未提交的更改
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "⚠️  检测到未提交的更改"
    git status
    echo ""
    read -p "是否先提交这些更改？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add -A
        git commit -m "Auto-commit before deploy: $(date '+%Y-%m-%d %H:%M:%S')"
    fi
fi

# 推送代码
echo "🚀 正在推送到 GitHub..."
git push -u origin master

echo ""
echo "✅ 推送成功！"
echo "📦 仓库地址：$REPO_URL"
echo ""
echo "可以在 GitHub 查看你的代码了！"
