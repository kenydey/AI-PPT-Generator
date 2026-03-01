"""
FastAPI 应用入口 - 企业级 AI PPT 全自动生成系统
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI PPT Generator API",
    description="企业级 AI PPT 全自动生成系统 - 支持关键词/多格式文件、联网搜索、Vibe 编辑",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


from backend.api.routes_parse import router as parse_router
from backend.api.routes_llm import router as llm_router
from backend.api.routes_generate import router as generate_router
from backend.api.routes_export import router as export_router

app.include_router(parse_router)
app.include_router(llm_router)
app.include_router(generate_router)
app.include_router(export_router)
