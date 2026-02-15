from src.logger import logger

class Retriever:
    def semantic_search(self, vectorstore):
        logger.info("Semantic Search Started")
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
        logger.info("Semantic Search completed")
        return retriever