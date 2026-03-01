"""
图表服务 - Graphviz 流程图渲染为 PNG；原生数据图表由 pptx_builder 使用 ChartData
"""
import io
from typing import Optional

import graphviz


def render_dot_to_png(dot_source: str, format: str = "png") -> bytes:
    """
    将 Graphviz DOT 源码渲染为 PNG 字节流。
    """
    try:
        g = graphviz.Source(dot_source)
        png_bytes = g.pipe(format=format)
        return png_bytes if png_bytes else b""
    except Exception:
        return b""
