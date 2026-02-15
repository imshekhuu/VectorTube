from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.logger import logger


class Splitter:
    def script_splitter(self, transcript):
        logger.info("splitting Started")
        text = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text.create_documents([transcript])
        logger.info("splitting completed")
        return chunks