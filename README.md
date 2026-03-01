# AI PPT Generator - 企业级 AI PPT 全自动生成系统

基于 [企业级 AI PPT SaaS 架构蓝图](企业级%20AI%20PPT%20SaaS%20架构蓝图.pdf)，支持关键词/多格式文件输入、联网搜索、AI 大纲、原生图表、Vibe 对话式编辑、导出 PPTX。

## 技术栈

- **后端**: FastAPI, LiteLLM, MarkItDown, python-pptx, Pillow, Tavily/SearXNG
- **前端**: React 18, Vite 5, TypeScript, Tailwind, Zustand
- **包管理/部署**: uv

## 环境准备（uv）

```bash
# 安装 uv（未安装时）
# Windows PowerShell:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆后进入项目
cd AI-PPT-Generator
uv sync
cd frontend && npm install && cd ..
```

## 启动

```bash
# 后端（项目根目录）
uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 前端（新终端）
cd frontend && npm run dev
```

- 前端: http://localhost:6000  
- API 文档: http://localhost:8000/docs  
- 健康检查: http://localhost:8000/health  

## 一键脚本

- Windows: `.\scripts\setup.ps1`
- macOS/Linux: `bash scripts/setup.sh`

## Docker

```bash
docker compose up -d
# 后端 8000，前端 6000
```

## 环境变量（示例）

- `OPENAI_API_KEY` - LiteLLM 使用
- `TAVILY_API_KEY` - 联网搜索（可选）
- `SEARXNG_HOST` - 自建 SearXNG（可选）
- `PEXELS_API_KEY` / `UNSPLASH_ACCESS_KEY` - 素材搜索（可选）

## API 概览

| 接口 | 说明 |
|------|------|
| POST /api/upload | 上传文件，返回 Markdown |
| POST /api/generate-outline | Markdown → PPTOutline |
| POST /api/v1/ppt/generate | 一键生成大纲（可选联网） |
| POST /api/export | PPTOutline → .pptx 文件流 |
| POST /api/v1/ppt/presentation/{id}/vibe | Vibe 自然语言修改 |
| GET /api/images/search?q= | 图片搜索 |
| GET /api/icons/search?q= | 图标搜索 |

详见 http://localhost:8000/docs 。
