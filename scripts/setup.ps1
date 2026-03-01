# AI PPT Generator - Windows 统一安装脚本 (uv)
$ErrorActionPreference = "Stop"

Write-Host "=== AI PPT Generator 环境准备 ===" -ForegroundColor Cyan

# 1. 检查/安装 uv
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "正在安装 uv..." -ForegroundColor Yellow
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
}

# 2. 后端依赖
Write-Host "安装后端 Python 依赖 (uv sync)..." -ForegroundColor Yellow
Set-Location $PSScriptRoot\..
uv sync
if ($LASTEXITCODE -ne 0) { exit 1 }

# 3. 前端依赖（如存在 frontend/package.json）
if (Test-Path "frontend\package.json") {
    Write-Host "安装前端依赖 (npm install)..." -ForegroundColor Yellow
    Set-Location frontend
    npm install
    Set-Location ..
}

Write-Host "环境就绪。启动: uv run uvicorn backend.main:app --reload" -ForegroundColor Green
