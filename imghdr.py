"""
Compatibility shim for the removed stdlib module 'imghdr' in Python 3.13.

Streamlit imports 'imghdr' unconditionally in its image element module. On
Python 3.13, the stdlib 'imghdr' no longer exists (PEP 594). This shim
implements a minimal subset of the original interface so imports succeed.

Only the 'what' function is provided. It attempts to determine the image type
from the file header. Supported types: 'png', 'jpeg', 'gif', 'bmp'. For other
types, it returns None.
"""

from typing import Optional, Union


def _read_header(file: Union[str, bytes], h: Optional[bytes]) -> Optional[bytes]:
    if isinstance(file, (bytes, bytearray)):
        return bytes(file)
    if h is not None:
        return h
    try:
        with open(file, "rb") as f:
            return f.read(32)
    except Exception:
        return None


def what(file: Union[str, bytes], h: Optional[bytes] = None) -> Optional[str]:
    """
    Return the image type ('png', 'jpeg', 'gif', 'bmp') detected from header,
    or None if unknown.
    Mirrors the original imghdr.what signature.
    """
    header = _read_header(file, h)
    if not header:
        return None

    # PNG: 89 50 4E 47 0D 0A 1A 0A
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"

    # JPEG: FF D8 FF
    if header[:3] == b"\xff\xd8\xff":
        return "jpeg"

    # GIF: GIF87a or GIF89a
    if header.startswith(b"GIF87a") or header.startswith(b"GIF89a"):
        return "gif"

    # BMP: 42 4D
    if header[:2] == b"BM":
        return "bmp"

    return None

