import asyncio
import logging
import re
from enum import Enum
from io import BytesIO, StringIO
from typing import Optional, Union

import aiohttp
import extraction
import html2text
import magic
import pdfplumber
from PIL import Image
from prometheus_client import Counter
from snakemd import Document as mdDocument
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from aideate_scraper.core.image_utils import async_http_get_image
from aideate_scraper.core.schemas import WebScrapeContent, WebContentType
from aideate_scraper.modal.modal_client import playwright_web_scrape
from aideate_scraper.core.scrape_utils import TIMEOUT_SEC, get_user_agent
from settings import ZENROWS_API_KEY

logger = logging.getLogger(__name__)

LLM_SUMMARIZE_FAIL_COUNTER = Counter(
    "scrape_llm_summarize_fail_request", "Number of llm summarize requests that failed"
)

GET_COUNTER = Counter("scrape_get_request", "Number of get requests")
SCRAPING_API_COUNTER = Counter("scrape_api_request", "Number of api requests")

GET_FAIL_COUNTER = Counter(
    "scrape_get_fail_request", "Number of get requests that failed"
)
SCRAPING_API_FAIL_COUNTER = Counter(
    "scrape_api_fail_request", "Number of api requests that failed"
)


HEURISTIC_VALID_HTML_TEXT = 1000
MAX_FILE_SIZE = 512 * 1024 * 1024  # 512 mb




async def parse_html(
    html_text: str,
    url: str,
    image_url: Optional[str] = None,
) -> WebScrapeContent:
    """
    Extract the HTML into various structured metadata
    """
    web_content = WebScrapeContent(content_type=WebContentType.HTML, content=html_text)
    extracted = extraction.Extractor().extract(html_text, source_url=url)

    title, thumbnails, canonical_url = (
        extracted.title,
        extracted.images,
        extracted.url,
    )
    thumbnails = [
        thumbnail_url
        for thumbnail_url in thumbnails
        if thumbnail_url.startswith("http")
    ]
    web_content.url = url
    if canonical_url:
        web_content.url = canonical_url
    if title:
        web_content.title = title
    if image_url:
        try:
            _, image = await async_http_get_image(image_url, 1)
            web_content.thumbnail = image_url
            web_content.thumbnail_width = image.width
            web_content.thumbnail_height = image.height
        except Exception as e:
            logger.info(str(e))
    if not web_content.thumbnail and thumbnails:
        thumbnail = None
        max_width, max_height = 0, 0
        get_image_tasks = [
            async_http_get_image(thumbnail_url, 1)
            for thumbnail_url in thumbnails
        ]
        image_results = await asyncio.gather(*get_image_tasks)
        image_results = [r for r in image_results if r]
        for url, image in image_results:
            try:
                if image.width * image.height > max_width * max_height:
                    thumbnail = url
                    max_width, max_height = image.width, image.height
            except Exception as e:
                logger.info(str(e))
        if thumbnail:
            web_content.thumbnail = thumbnail
            web_content.thumbnail_width = max_width
            web_content.thumbnail_height = max_height

    if extracted.images:
        web_content.images = extracted.images

    return web_content


def parse_image(content_bytes: bytes, image_url: str) -> WebScrapeContent:
    web_content = WebScrapeContent(
        content_type=WebContentType.IMAGE,
        content=content_bytes,
        url=image_url,
        images=[image_url],
        thumbnail=image_url,
    )
    image = Image.open(BytesIO(content_bytes))
    web_content.thumbnail_width=image.width
    web_content.thumbnail_height=image.height
    return web_content


async def parse_pdf(content_bytes: bytes, url: str):
    web_content = WebScrapeContent(content_type=WebContentType.PDF, content=content_bytes)
    pdf_file = BytesIO(content_bytes)

    texts = []
    with pdfplumber.open(pdf_file) as pdf:
        if len(pdf.pages) > 0:
            text = pdf.pages[0].extract_text()
            if text:
                texts.append(text)
        thumbnail_bytes = BytesIO()
        im = pdf.pages[0].to_image(resolution=150, antialias=True)
        im.save(thumbnail_bytes, format="PNG")
        thumbnail_bytes.seek(0)

        web_content.thumbnail_content = thumbnail_bytes.getvalue()

    web_content.title = url
    web_content.texts = texts



class LinkType(str, Enum):
    # be careful of JSON serialization bugs: https://stackoverflow.com/questions/65339635/how-to-deserialise-enumeration-with-string-representation
    # not a scenario now

    HTML = "html"
    PDF = "pdf"
    IMAGE = "image"
    UNKNOWN = "unknown"


def _get_web_type(content: Union[str, bytes]) -> LinkType:
    if isinstance(content, bytes):
        file_buffer = BytesIO(content)
    else:
        file_buffer = StringIO(content)
    content_type = magic.from_buffer(file_buffer.read(2048), mime=True)
    if "text/html" in content_type:
        return LinkType.HTML
    elif "application/pdf" in content_type:
        return LinkType.PDF
    elif any(
        image_type in content_type
        for image_type in [
            "image/png",
            "image/jpeg",
            "image/webp",
            "image/gif",
            "image/svg+xml",
        ]
    ):
        return LinkType.IMAGE
    return LinkType.UNKNOWN


def extract_text_from_content(content: Union[str, bytes]) -> Optional[str]:
    link_type = _get_web_type(content)
    match link_type:
        case LinkType.HTML:
            if isinstance(content, bytes):
                content = content.decode("utf-8")
            return html2text.html2text(content)

        case LinkType.PDF:
            if isinstance(content, str):
                content = content.encode("utf-8")
            source_doc = mdDocument()
            with pdfplumber.open(BytesIO(content)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    source_doc.add_paragraph(text)
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            source_doc.add_table(header=table[0], data=table[1:])

            return str(source_doc)
        case LinkType.IMAGE:
            return None


async def process_web_content(
    content: Optional[Union[str, bytes]],
    url: str,
) -> Optional[WebScrapeContent]:
    if not content:
        return None

    link_type = _get_web_type(content)
    match link_type:
        case LinkType.HTML:
            return await parse_html(content, url)
        case LinkType.PDF:
            return await parse_pdf(content, url)
        case LinkType.IMAGE:
            return parse_image(content, url)
    return None


def is_instagram_url(url: str) -> bool:
    return "instagram.com" in url


async def ascrape_web(
    url: str
) -> Optional[WebScrapeContent]:
    if not is_instagram_url(url):
        # instagram doesn't work for these options but in general we want them first

        content = await aget_scrape_api(url)
        response = await process_web_content(content, url)
        if response:
            return response

        # fallback to requests
        content = await aget(url)
        response = await process_web_content(content, url)
        if response:
            return response

    content = await playwright_web_scrape(url, timeout=int(TIMEOUT_SEC))
    response = await process_web_content(content, url)
    if response:
        return response

    return None


async def async_scrape_web_content(url: str) -> Optional[Union[str, bytes]]:
    # scrape without parsing
    if not is_instagram_url(url):
        # instagram doesn't work for these options but in general we want them first

        content = await aget_scrape_api(url)
        if content:
            return content

        # fallback to requests
        content = await aget(url)
        if content:
            return content

    return await playwright_web_scrape(url, timeout=int(TIMEOUT_SEC))


class ContentExceedMaxLimit(Exception):
    pass


def make_default_headers(user_agent: str) -> dict:
    return {
        "accept": "*/*",
        "content-type": "application/json; charset=utf-8",
        "user-agent": user_agent,
        "accept-language": "en-us",
    }


async def aget(url: str) -> Optional[Union[str, bytes]]:
    GET_COUNTER.inc()
    # Send a GET request to the URL
    try:
        print("fetching url via GET", url)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, headers=make_default_headers(get_user_agent()), timeout=TIMEOUT_SEC
            ) as response:
                print("received url")
                # If the GET request is successful, the status code will be 200
                if response.status == 200:
                    total_size = 0
                    bytes_io = BytesIO()
                    async for chunk in response.content.iter_chunked(n=1024 * 1024):
                        total_size += len(chunk)
                        if total_size > MAX_FILE_SIZE:
                            raise ContentExceedMaxLimit(
                                f"Uh oh, website content is larger than maximum support size of {MAX_FILE_SIZE} bytes"
                            )
                        bytes_io.write(chunk)
                    bytes_data = bytes_io.getvalue()
                    response._body = bytes_data
                    encoding = response.get_encoding()
                    try:
                        return str(bytes_data, encoding, errors="strict")
                    except UnicodeDecodeError as e:
                        return bytes_data

                GET_FAIL_COUNTER.inc()
                return None
    except ContentExceedMaxLimit as e:
        GET_FAIL_COUNTER.inc()
        raise e
    except Exception as e:
        GET_FAIL_COUNTER.inc()
        logger.error(f"cannot crawl url {url}", e)
        return None


def need_enable_javascript(html_text):
    # Check for the presence of <noscript> tags
    if re.search(r"<noscript>", html_text, re.IGNORECASE):
        return True

    # Check for JavaScript-dependent attributes
    if re.search(r"onclick|onload|onsubmit", html_text, re.IGNORECASE):
        return True

    # Check for variations of "JavaScript is disabled" text
    javascript_disabled_patterns = [
        r"javascript\s+is\s+disabled",
        r"enable\s+javascript",
        r"javascript\s+not\s+supported",
        r"please\s+enable\s+javascript",
        r"javascript\s+required",
        # Add more patterns as needed
    ]

    for pattern in javascript_disabled_patterns:
        if re.search(pattern, html_text, re.IGNORECASE):
            return True

    return False


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    retry=retry_if_exception_type(asyncio.exceptions.TimeoutError),
)
async def aget_scrape_api(url: str, enable_javascript: bool = False):
    SCRAPING_API_COUNTER.inc()
    params = {
        "apikey": ZENROWS_API_KEY,
        "url": url,
    }
    if enable_javascript:
        params["js_render"] = "true"

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url="https://api.zenrows.com/v1/",
            params=params,
            timeout=TIMEOUT_SEC,
        ) as response:
            # If the GET request is successful, the status code will be 200
            if response.status != 200:
                SCRAPING_API_FAIL_COUNTER.inc()
                return None

            text = await response.text(errors="replace")
            if need_enable_javascript(text) and not enable_javascript:
                logger.info("enable javascript retry")
                return await aget_scrape_api(url, enable_javascript=True)
            return text


if __name__ == "__main__":
    import asyncio

    # print(asyncio.run(aget_scrapingbee("https://openai.com")))
    # result = asyncio.run(aget("https://arxiv.org/pdf/2307.01952.pdf"))
    # result = asyncio.run(aget_scrapingbee("https://arxiv.org/pdf/2307.01952.pdf"))
    # result = get("https://arxiv.org/pdf/2307.01952.pdf")
    # result = get_scrapingbee("https://arxiv.org/pdf/2307.01952.pdf")
    # result = scrape_web("https://arxiv.org/pdf/2307.01952.pdf")
    # result = ascrape_web("https://arxiv.org/pdf/2307.01952.pdf")
    # print(scrape_web("https://www.youtube.com/watch?v=SKia5QUiGkE"))
    # print(scrape_web("https://www.youtube.com/watch?v=SKia5QUiGkE"))
    # message = asyncio.run(
    #    ascrape_web("https://twitter.com/itsandrewgao/status/1786591700410118295")
    # )
    result = asyncio.run(ascrape_web("https://m-arkitektur.se/villa-hagerman-gotland"))
    print(result)
