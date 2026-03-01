"""
PPTX 渲染与导出 - /api/export
"""
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from backend.api.schemas import PPTOutline
from backend.services.pptx_builder import build_pptx

router = APIRouter(prefix="/api", tags=["export"])


class ExportRequest(BaseModel):
    outline: dict
    template_path: str | None = None


@router.post("/export")
async def export_pptx(req: ExportRequest) -> Response:
    """
    将 PPTOutline 渲染为 .pptx 文件流返回。
    """
    try:
        outline = PPTOutline.model_validate(req.outline)
    except Exception as e:
        raise HTTPException(422, str(e))
    template = Path(req.template_path) if req.template_path else None
    if template and not template.is_absolute():
        template = Path(__file__).resolve().parent.parent / "templates" / req.template_path
    pptx_bytes = build_pptx(outline, template_path=template)
    return Response(
        content=pptx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": "attachment; filename=presentation.pptx"},
    )
