"""
可编辑 PPTX 导出（可选）- OCR 多图层：背景图 + 文本层
依赖百度 OCR 等；当前为占位，与 pptx_builder 配合后可实现 100% 可编辑。
"""
from backend.api.schemas import PPTOutline


def build_editable_pptx(outline: PPTOutline, template_path=None) -> bytes:
    """
    占位：与 build_pptx 类似，但对含复杂图文页可调用 OCR 分离文字层。
    需配置 BAIDU_API_KEY 等。当前直接委托 pptx_builder.build_pptx。
    """
    from backend.services.pptx_builder import build_pptx
    return build_pptx(outline, template_path=template_path)
