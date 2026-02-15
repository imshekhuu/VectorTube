from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from logger import logger

api = YouTubeTranscriptApi()


class YouTubeTranscript:
    def extract_YouTubeTranscript(video_id: str):
        try:
            logger.info("Video Transcript extraction Started")
            transcript_list = api.fetch(video_id, languages=["en"])
            transcript = " ".join(chunk.text for chunk in transcript_list)
            logger.info("Video Transcript extraction completed")
            return transcript

        except TranscriptsDisabled:
            return("No captions available for this video.")