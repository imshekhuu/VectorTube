from langchain_text_splitters import RecursiveCharacterTextSplitter


class Splitter:
    def script_splitter(self, transcript):
        text = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text.create_documents([transcript])
        return chunks