"""
文档解析 API - /api/upload，调用 MarkItDown 返回提取的 Markdown
"""
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException

from backend.services.document_service import parse_to_markdown

router = APIRouter(prefix="/api", tags=["parse"])


@router.post("/upload")
async def upload_and_parse(file: UploadFile = File(...)) -> dict:
    """
    上传 PDF/Word/Excel/PPTX/HTML/TXT 或图片，返回提取的 Markdown 文本。
    """
    suffix = Path(file.filename or "").suffix.lower()
    allowed = {".pdf", ".docx", ".xlsx", ".pptx", ".html", ".htm", ".txt", ".md", ".png", ".jpg", ".jpeg"}
    if suffix not in allowed:
        raise HTTPException(400, f"不支持的文件类型: {suffix}，支持: {allowed}")

    content = await file.read()
    if not content:
        raise HTTPException(400, "文件为空")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        try:
            markdown = parse_to_markdown(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)
    except Exception as e:
        raise HTTPException(422, f"解析失败: {str(e)}")

    return {"markdown": markdown, "filename": file.filename}
