from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from src.logger import logger
from dotenv import load_dotenv

load_dotenv()

class Embeddings:
    def create_embedding(self, chunks):
        logger.info("embedding Started")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        vector_store = FAISS.from_documents(chunks, embeddings)
        logger.info("embedding completed")
        return vector_store
