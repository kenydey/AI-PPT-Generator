"""
一键生成 - 整合编排器：content/markdown -> 研究+大纲+设计 -> outline
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.api.schemas import GenerateOutlineResponse
from backend.services.orchestrator import research_and_outline

router = APIRouter(prefix="/api/v1/ppt", tags=["generate"])


class GenerateRequest(BaseModel):
    content: str = ""
    markdown: str | None = None
    n_slides: int = 8
    model: str = "gpt-4o"
    web_search: bool = False


@router.post("/generate", response_model=GenerateOutlineResponse)
async def generate(req: GenerateRequest) -> GenerateOutlineResponse:
    """
    一键生成大纲：content 或 markdown 作为输入，经编排器返回 PPTOutline。
    """
    markdown = req.markdown or req.content or ""
    if not markdown.strip():
        raise HTTPException(400, "请提供 content 或 markdown")
    outline = await research_and_outline(
        markdown, req.model, req.n_slides, req.web_search
    )
    return GenerateOutlineResponse(outline=outline)
