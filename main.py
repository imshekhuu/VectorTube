from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from urllib.parse import urlparse, parse_qs
import re


class YouTubeTranscript:

    def __init__(self, video_link):
        self.video_link = video_link
        self.video_id = None
        self.transcript = None
        
    def extract_id(self):
        parsed = urlparse(self.video_link)
        query = parse_qs(parsed.query)

        if "v" in query:
            self.video_id = query["v"][0]
            return self.video_id
        
        pattern = r"(?:youtu\.be/|shorts/|embed/|live/)([^?&/]+)"
        match = re.search(pattern, self.video_link)

        if match:
            self.video_id = match.group(1)
        
        return self.video_id
    
    def fetch_transcript(self):
        if not self.video_id:
             print("Extract video ID first.")
             return None
        
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(self.video_id)
            self.transcript = " ".join(chunk["text"] for chunk in transcript_list)
            return self.transcript
        except TranscriptsDisabled:
            print("No captions available for this video.")
            return None
        

    def split_transcript(self, chunk_size=1000, chunk_overlap=200):
        if not self.transcript:
             print("Fetch transcript first.")
             return None
        

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap   
        )

        return splitter.create_documents([self.transcript])
