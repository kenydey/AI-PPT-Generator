"""
文档解析服务 - 封装微软 MarkItDown，将 PDF/Word/Excel/PPTX/HTML/TXT/图片 转为 Markdown
"""
from pathlib import Path
from typing import BinaryIO

from markitdown import MarkItDown


def parse_to_markdown(source: str | Path | BinaryIO) -> str:
    """
    将上传文件解析为纯文本 Markdown。
    支持：PDF, Word (DOCX), Excel, PPTX, HTML, TXT, 图片（含 EXIF/OCR）
    """
    md = MarkItDown()
    result = md.convert(source)
    return result.text_content or ""


def parse_file_path(file_path: Path) -> str:
    """从本地路径解析"""
    return parse_to_markdown(str(file_path))
