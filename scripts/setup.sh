#!/usr/bin/env bash
# AI PPT Generator - 统一安装脚本 (uv)
set -e

echo "=== AI PPT Generator 环境准备 ==="

# 1. 安装 uv（若未安装）
if ! command -v uv &>/dev/null; then
    echo "正在安装 uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# 2. 后端依赖
echo "安装后端 Python 依赖 (uv sync)..."
cd "$(dirname "$0")/.."
uv sync

# 3. 前端依赖
if [ -f "frontend/package.json" ]; then
    echo "安装前端依赖 (npm install)..."
    cd frontend && npm install && cd ..
fi

echo "环境就绪。启动: uv run uvicorn backend.main:app --reload"
