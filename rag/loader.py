from typing import Optional, Tuple

from src.Transcript import YouTubeTranscriptLoader
from src.extract_id import VideoIdExtractor


class Loader:
    def __init__(self) -> None:
        self.id_extractor = VideoIdExtractor()
        self.transcript_loader = YouTubeTranscriptLoader()

    def extract_video_id(self, video_url: str) -> Optional[str]:
        return self.id_extractor.extract_video_id(video_url)

    def load_transcript(self, video_url: str) -> Tuple[Optional[str], Optional[str]]:
        video_id = self.extract_video_id(video_url)
        if not video_id:
            return None, None

        transcript = self.transcript_loader.fetch_transcript(video_id)
        return video_id, transcript
