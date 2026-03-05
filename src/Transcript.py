from typing import Optional

from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    YouTubeTranscriptApi,
)

from src.logger import logger


class YouTubeTranscriptLoader:
    def __init__(self) -> None:
        self.api = YouTubeTranscriptApi()

    def fetch_transcript(self, video_id: str, language: str = "en") -> Optional[str]:
        if not video_id:
            return None

        try:
            logger.info("Video transcript extraction started")
            transcript_list = self.api.fetch(video_id, languages=[language])
            transcript = " ".join(chunk.text for chunk in transcript_list).strip()
            logger.info("Video transcript extraction completed")
            return transcript or None
        except (TranscriptsDisabled, NoTranscriptFound):
            logger.warning("No transcript available for video ID: %s", video_id)
            return None
