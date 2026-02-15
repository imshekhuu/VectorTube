class Retriever:
    def semantic_search(self, vectorstore):
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
        return retriever