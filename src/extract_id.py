from urllib.parse import urlparse, parse_qs
from logger import logger
import re

class Video_id:
    def extract_video_id(url: str):
        logger.info("Video id extraction Started")
        parsed = urlparse(url)
        query = parse_qs(parsed.query)

        if "v" in query:
            return query["v"][0]
        
        pattern = r"(?:youtu\.be/|shorts/|embed/)([^?&/]+)"
        match = re.search(pattern, url)
        logger.info("Video id extraction compeleted")

        return match.group(1) if match else None