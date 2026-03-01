"""
联网搜索服务 - Tavily 为主，可选 SearXNG
环境变量: TAVILY_API_KEY, SEARXNG_HOST (可选，如 http://localhost:8888)
"""
import os
from typing import Optional

import httpx


async def web_search(query: str, max_results: int = 5) -> list[dict]:
    """
    执行联网搜索，返回列表 [{ "title": "", "url": "", "content": "" }, ...]。
    优先使用 Tavily，若未配置则尝试 SearXNG。
    """
    results: list[dict] = []
    api_key = os.getenv("TAVILY_API_KEY")
    if api_key:
        try:
            from tavily import AsyncTavilyClient
            client = AsyncTavilyClient(api_key=api_key)
            resp = await client.search(query, max_results=max_results)
            for r in getattr(resp, "results", []) or []:
                results.append({
                    "title": getattr(r, "title", "") or "",
                    "url": getattr(r, "url", "") or "",
                    "content": getattr(r, "content", "") or "",
                })
            return results
        except Exception:
            pass
    searxng = os.getenv("SEARXNG_HOST", "").rstrip("/")
    if searxng:
        try:
            async with httpx.AsyncClient(timeout=15.0) as c:
                r = await c.get(f"{searxng}/search", params={"q": query, "format": "json"})
                r.raise_for_status()
                data = r.json()
                for entry in (data.get("results") or [])[:max_results]:
                    results.append({
                        "title": entry.get("title", ""),
                        "url": entry.get("url", ""),
                        "content": entry.get("content", "") or "",
                    })
        except Exception:
            pass
    return results
