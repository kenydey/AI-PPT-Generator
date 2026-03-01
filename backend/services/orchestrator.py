"""
多智能体编排 - 主控调度器：研究 -> 大纲 -> 设计（Layout 映射）
"""
from backend.api.schemas import PPTOutline, SlideOutline
from backend.core.llm_gateway import generate_response
from backend.services.research_service import web_search


def design_agent(outline: PPTOutline) -> PPTOutline:
    """
    设计智能体：根据每页内容为幻灯片分配 layout_id（单列/双列/图文等）。
    """
    updated = []
    for i, s in enumerate(outline.slides):
        layout_id = "title_slide" if i == 0 else "content"
        if len(s.bullets) > 4:
            layout_id = "dual_column_list"
        if s.chart_type and s.chart_type != "none":
            layout_id = "chart"
        updated.append(SlideOutline(**{**s.model_dump(), "layout_id": layout_id}))
    return PPTOutline(slides=updated)


async def research_and_outline(
    markdown: str,
    model: str,
    n_slides: int,
    web_search_enabled: bool,
) -> PPTOutline:
    """
    主控调度：研究智能体（可选联网）-> 大纲生成 -> 设计智能体（Layout 映射）。
    """
    import json
    import re
    from backend.api.routes_llm import OUTLINE_SYSTEM

    context = markdown[:12000]
    if web_search_enabled:
        query = (markdown[:300] or "presentation").replace("\n", " ").strip()
        results = await web_search(query, max_results=5)
        if results:
            context = "【联网参考】\n" + "\n".join(
                f"- {r['title']}: {r['content'][:200]}" for r in results
            ) + "\n\n" + context
    user_content = f"根据以下内容生成演示文稿大纲，约 {n_slides} 页。只输出符合 PPTOutline 的 JSON。\n\n{context}"
    messages = [{"role": "system", "content": OUTLINE_SYSTEM}, {"role": "user", "content": user_content}]
    raw = await generate_response(model, messages)
    text = raw.strip()
    for pattern in [r"```(?:json)?\s*([\s\S]*?)```", r"(\{[\s\S]*\})"]:
        m = re.search(pattern, text)
        if m:
            text = (m.group(1) if m.lastindex else m.group(0)).strip()
            break
    data = json.loads(text)
    outline = PPTOutline.model_validate(data)
    return design_agent(outline)
