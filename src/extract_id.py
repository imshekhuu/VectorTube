import re
from typing import Optional
from urllib.parse import parse_qs, urlparse

from src.logger import logger


class VideoIdExtractor:
    _pattern = re.compile(r"(?:youtu\.be/|shorts/|embed/|live/)([^?&/]+)")

    def extract_video_id(self, url: str) -> Optional[str]:
        logger.info("Video ID extraction started")

        if not url:
            return None

        parsed = urlparse(url.strip())
        query = parse_qs(parsed.query)

        if "v" in query and query["v"]:
            return query["v"][0]

        match = self._pattern.search(url)
        video_id = match.group(1) if match else None

        logger.info("Video ID extraction completed")
        return video_id
