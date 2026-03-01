"""
第三方图库与图标 API 代理 - /api/images/search, /api/icons/search
Pexels, Unsplash, Pixabay, Iconfinder/Flaticon
"""
import os
from typing import Any

import httpx
from fastapi import APIRouter, Query

router = APIRouter(prefix="/api", tags=["media"])


def _norm(items: list[dict], thumb_key: str = "src", url_key: str = "url") -> list[dict]:
    return [{"thumb": i.get(thumb_key) or i.get("url"), "url": i.get(url_key) or i.get("src")} for i in items]


@router.get("/images/search")
async def search_images(q: str = Query(..., min_length=1)) -> dict:
    """搜索图片，返回标准化列表 { results: [{ thumb, url }] }"""
    results: list[dict] = []
    # Pexels
    key = os.getenv("PEXELS_API_KEY")
    if key:
        try:
            async with httpx.AsyncClient(timeout=10.0) as c:
                r = await c.get(
                    "https://api.pexels.com/v1/search",
                    params={"query": q, "per_page": 10},
                    headers={"Authorization": key},
                )
                if r.is_success:
                    data = r.json()
                    for p in (data.get("photos") or [])[:10]:
                        src = p.get("src") or {}
                        results.append({"thumb": src.get("small"), "url": src.get("original") or src.get("large")})
        except Exception:
            pass
    # Unsplash
    key = os.getenv("UNSPLASH_ACCESS_KEY")
    if key and len(results) < 10:
        try:
            async with httpx.AsyncClient(timeout=10.0) as c:
                r = await c.get(
                    "https://api.unsplash.com/search/photos",
                    params={"query": q, "per_page": 10},
                    headers={"Authorization": f"Client-ID {key}"},
                )
                if r.is_success:
                    data = r.json()
                    for p in (data.get("results") or [])[:10]:
                        urls = p.get("urls") or {}
                        results.append({"thumb": urls.get("thumb"), "url": urls.get("regular") or urls.get("full")})
        except Exception:
            pass
    return {"results": results[:20]}


@router.get("/icons/search")
async def search_icons(q: str = Query(..., min_length=1)) -> dict:
    """搜索图标，返回标准化列表"""
    results: list[dict] = []
    # Iconfinder 需 API key
    key = os.getenv("ICONFINDER_API_KEY")
    if key:
        try:
            async with httpx.AsyncClient(timeout=10.0) as c:
                r = await c.get(
                    "https://api.iconfinder.com/v4/icons/search",
                    params={"query": q, "count": 10},
                    headers={"Authorization": f"Bearer {key}"},
                )
                if r.is_success:
                    data = r.json()
                    for icon in (data.get("icons") or [])[:10]:
                        rasters = (icon.get("raster_sizes") or [])[:1]
                        if rasters:
                            u = rasters[0].get("formats", [{}])[0].get("preview_url") or rasters[0].get("formats", [{}])[0].get("download_url")
                            results.append({"thumb": u, "url": u})
        except Exception:
            pass
    return {"results": results[:20]}
