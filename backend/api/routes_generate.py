"""
一键生成 - 整合编排器：content/markdown -> 研究+大纲+设计 -> outline
"""
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.api.routes_vibe import set_presentation_outline
from backend.services.orchestrator import research_and_outline

router = APIRouter(prefix="/api/v1/ppt", tags=["generate"])


class GenerateRequest(BaseModel):
    content: str = ""
    markdown: str | None = None
    n_slides: int = 8
    model: str = "gpt-4o"
    web_search: bool = False


class GenerateResponse(BaseModel):
    presentation_id: str
    outline: dict


@router.post("/generate")
async def generate(req: GenerateRequest) -> GenerateResponse:
    """
    一键生成大纲：content 或 markdown 作为输入，经编排器返回 PPTOutline 与 presentation_id（供 Vibe 使用）。
    """
    markdown = req.markdown or req.content or ""
    if not markdown.strip():
        raise HTTPException(400, "请提供 content 或 markdown")
    outline = await research_and_outline(
        markdown, req.model, req.n_slides, req.web_search
    )
    pid = str(uuid.uuid4())
    set_presentation_outline(pid, outline)
    return GenerateResponse(presentation_id=pid, outline=outline.model_dump())
