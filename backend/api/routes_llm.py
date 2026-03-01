"""
LiteLLM 对话与大纲生成 - /api/generate-outline
"""
import json
import re

from fastapi import APIRouter, HTTPException

from backend.api.schemas import GenerateOutlineRequest, GenerateOutlineResponse, PPTOutline
from backend.core.llm_gateway import generate_response
from backend.services.research_service import web_search

router = APIRouter(prefix="/api", tags=["llm"])

OUTLINE_SYSTEM = """你是一名专业的演示文稿大纲撰写专家。根据用户提供的文档内容（Markdown），生成符合以下 JSON 结构的大纲，且只输出该 JSON，不要输出任何其他文字或 Markdown 代码块标记。

JSON 结构要求：
- slides: 数组，每个元素包含 title（幻灯片标题）、bullets（要点列表，字符串数组）、chart_type（可选，取值为 "bar"|"line"|"pie"|"bubble"|"none" 之一，若该页需要数据图表则填对应类型否则 "none"）、chart_data（仅当 chart_type 不为 none 时存在，格式 {"categories": ["A","B"], "series": [{"name": "系列1", "values": [10, 20]}]}）、image_urls（可选，默认 []）
- 页数控制在用户要求的 n_slides 以内，第一页一般为标题/封面，最后一页可为总结或致谢。"""


@router.post("/generate-outline", response_model=GenerateOutlineResponse)
async def generate_outline(req: GenerateOutlineRequest) -> GenerateOutlineResponse:
    """
    接收 Markdown 文本，调用 LiteLLM 生成符合 PPTOutline 的 JSON 大纲。
    若 web_search=True，先联网搜索再增强上下文。
    """
    context = req.markdown[:12000]
    search_context = ""
    if req.web_search:
        query = (req.markdown[:300] or "presentation outline").replace("\n", " ").strip()
        results = await web_search(query, max_results=5)
        if results:
            search_context = "\n\n【联网搜索参考】\n" + "\n".join(
                f"- {r['title']}: {r['content'][:200]}..." for r in results
            )
    user_content = f"请根据以下文档内容生成演示文稿大纲，共 {req.n_slides} 页左右。{search_context}\n\n文档内容：\n{context}"
    messages = [
        {"role": "system", "content": OUTLINE_SYSTEM},
        {"role": "user", "content": user_content},
    ]
    try:
        raw = await generate_response(req.model, messages)
    except Exception as e:
        raise HTTPException(502, f"LLM 调用失败: {str(e)}")

    # 尝试从回复中提取 JSON（可能被 markdown 代码块包裹）
    text = raw.strip()
    for pattern in [r"```(?:json)?\s*([\s\S]*?)```", r"(\{[\s\S]*\})"]:
        m = re.search(pattern, text)
        if m:
            text = m.group(1).strip() if m.lastindex else m.group(0)
            break
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise HTTPException(422, f"模型返回非合法 JSON: {e}")

    try:
        outline = PPTOutline.model_validate(data)
    except Exception as e:
        raise HTTPException(422, f"大纲结构不符合 PPTOutline: {e}")

    return GenerateOutlineResponse(outline=outline)
