"""
Pillow 图像增强 - object-fit: cover、色彩对齐（LAB 空间微调）
"""
import io
from typing import Tuple

from PIL import Image


def fit_cover(img_bytes: bytes, target_width: int, target_height: int) -> bytes:
    """
    缩放并裁剪为覆盖目标尺寸，保持比例（object-fit: cover）。
    使用 Lanczos 重采样，居中裁剪。
    """
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    w, h = img.size
    if w <= 0 or h <= 0:
        return img_bytes
    scale = max(target_width / w, target_height / h)
    nw, nh = int(w * scale), int(h * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - target_width) // 2
    top = (nh - target_height) // 2
    img = img.crop((left, top, left + target_width, top + target_height))
    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


def align_color_lab(img_bytes: bytes, hex_ref: str) -> bytes:
    """
    根据参考主色 hex_ref 在 LAB 空间微调图像色相/饱和度（占位实现）。
    完整实现可：RGB->LAB，按 ref 调整 A/B 通道，再转回 RGB。
    """
    return img_bytes
