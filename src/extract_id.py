from urllib.parse import urlparse, parse_qs
import re

class Video_id:
    def extract_video_id(url: str):
        parsed = urlparse(url)
        query = parse_qs(parsed.query)

        if "v" in query:
            return query["v"][0]
        
        pattern = r"(?:youtu\.be/|shorts/|embed/)([^?&/]+)"
        match = re.search(pattern, url)

        return match.group(1) if match else None