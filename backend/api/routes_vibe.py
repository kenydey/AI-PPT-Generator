"""
Vibe 对话式编辑 - POST /api/v1/ppt/presentation/{id}/vibe，WebSocket 实时预览
"""
import json
import re
from typing import Optional

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from backend.api.schemas import PPTOutline, SlideOutline
from backend.core.llm_gateway import generate_response

router = APIRouter(prefix="/api/v1/ppt", tags=["vibe"])

# 内存状态：presentation_id -> PPTOutline（生产可用 Redis/DB）
_store: dict[str, PPTOutline] = {}


class VibeRequest(BaseModel):
    instruction: str
    slide_index: Optional[int] = None
    region_id: Optional[str] = None


VIBE_SYSTEM = """你是一个演示文稿编辑助手。用户会给出当前大纲的 JSON 和一条自然语言修改指令。你只输出修改后的完整 JSON，且符合 PPTOutline 结构（slides 数组，每项含 title, bullets, chart_type, chart_data, image_urls, layout_id）。不要输出任何其他文字或 markdown 标记。"""


async def _apply_vibe(outline: PPTOutline, instruction: str, slide_index: Optional[int], region_id: Optional[str]) -> PPTOutline:
    """编辑智能体：LLM 根据指令修改大纲，返回新 PPTOutline"""
    import json as _json
    outline_json = outline.model_dump_json()
    user = f"当前大纲：\n{outline_json}\n\n用户指令：{instruction}"
    if slide_index is not None:
        user += f"\n（指定页码：第 {slide_index + 1} 页）"
    messages = [{"role": "system", "content": VIBE_SYSTEM}, {"role": "user", "content": user}]
    raw = await generate_response("gpt-4o", messages)
    text = raw.strip()
    for pattern in [r"```(?:json)?\s*([\s\S]*?)```", r"(\{[\s\S]*\})"]:
        m = re.search(pattern, text)
        if m:
            text = (m.group(1) if m.lastindex else m.group(0)).strip()
            break
    data = _json.loads(text)
    return PPTOutline.model_validate(data)


@router.post("/presentation/{presentation_id}/vibe")
async def vibe_edit(presentation_id: str, req: VibeRequest) -> dict:
    """自然语言修改指定演示文稿，返回更新后的 outline"""
    outline = _store.get(presentation_id)
    if not outline:
        raise HTTPException(404, "presentation not found")
    updated = await _apply_vibe(outline, req.instruction, req.slide_index, req.region_id)
    _store[presentation_id] = updated
    return {"updated_outline": updated.model_dump(), "preview_url": f"/presentation/{presentation_id}"}


@router.websocket("/presentation/{presentation_id}/vibe/ws")
async def vibe_websocket(websocket: WebSocket, presentation_id: str):
    """WebSocket：客户端发 { instruction } 或 { outline }，服务端推送 partial_update"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            if "outline" in msg:
                _store[presentation_id] = PPTOutline.model_validate(msg["outline"])
                await websocket.send_json({"type": "ack", "status": "ok"})
            elif "instruction" in msg:
                outline = _store.get(presentation_id)
                if not outline:
                    await websocket.send_json({"type": "error", "message": "presentation not found"})
                    continue
                updated = await _apply_vibe(
                    outline,
                    msg["instruction"],
                    msg.get("slide_index"),
                    msg.get("region_id"),
                )
                _store[presentation_id] = updated
                await websocket.send_json({"type": "partial_update", "outline": updated.model_dump()})
    except WebSocketDisconnect:
        pass


def set_presentation_outline(presentation_id: str, outline: PPTOutline) -> None:
    _store[presentation_id] = outline
