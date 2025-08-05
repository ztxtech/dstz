#!/bin/bash

# clean.sh - 清理构建生成的文件和目录

echo "清理构建生成的文件和目录..."

# 删除Python构建目录
rm -rf build/
echo "已删除 build/ 目录"

# 删除Python分发目录
rm -rf dist/
echo "已删除 dist/ 目录"

# 删除Python egg-info目录
rm -rf *.egg-info/
echo "已删除 *.egg-info/ 目录"

# 删除文档构建目录（如果存在）
rm -rf site/
echo "已删除 site/ 目录"

# 删除Python缓存文件
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
echo "已删除所有 __pycache__ 目录"

# 删除Python编译文件
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo "已删除所有 *.pyc 文件"

# 删除Python编译目录
find . -type d -name "*.pyc" -exec rm -rf {} + 2>/dev/null || true
echo "已删除所有 *.pyc 目录"

echo "清理完成！"