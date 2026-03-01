"""
Pydantic 模型 - 与前端 TypeScript 类型对齐
"""
from pydantic import BaseModel, Field


class SlideOutline(BaseModel):
    title: str
    bullets: list[str] = Field(default_factory=list)
    chart_type: str | None = None  # bar | line | pie | bubble | none
    chart_data: dict | None = None
    image_urls: list[str] = Field(default_factory=list)
    layout_id: str | None = None  # title_slide | content | dual_column_list | chart


class PPTOutline(BaseModel):
    slides: list[SlideOutline]


class GenerateOutlineRequest(BaseModel):
    markdown: str
    model: str = "gpt-4o"
    n_slides: int = 8
    web_search: bool = False


class GenerateOutlineResponse(BaseModel):
    outline: PPTOutline
