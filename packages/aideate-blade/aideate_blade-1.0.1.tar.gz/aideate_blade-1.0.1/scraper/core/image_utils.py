
import logging
from io import BytesIO

from typing import Optional, Tuple

from httpx import AsyncClient, Client
from PIL import Image


async def async_http_get_image(
    http_path: str,
    timeout_secs: Optional[int] = None
) -> Optional[Tuple[str, Image.Image]]:
    try:
        async with AsyncClient() as client:
            img_data = (await client.get(http_path, timeout=timeout_secs)).content
        return http_path, Image.open(BytesIO(img_data))
    except Exception as e:
        logging.error(e)
    return None
