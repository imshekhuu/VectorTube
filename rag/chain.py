import os
from pathlib import Path
from operator import itemgetter
from typing import Dict, Tuple

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from rag.embeddings import Embeddings
from rag.loader import Loader
from rag.retriever import Retriever
from rag.splitter import Splitter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=PROJECT_ROOT / ".env", override=True)


class VectorTubeChain:
    def __init__(self) -> None:
        self.loader = Loader()
        self.splitter = Splitter()
        self.embeddings = Embeddings()
        self.retriever_builder = Retriever()
        self.retriever_cache: Dict[str, object] = {}
        self.model = self._build_model()

        self.prompt = PromptTemplate(
            template="""
You are a helpful assistant.
Answer only from the provided transcript context.
If the context is insufficient, say you don't know.

Context:
{context}

Question:
{question}
            """.strip(),
            input_variables=["context", "question"],
        )

        self.parser = StrOutputParser()

    @staticmethod
    def _format_docs(docs) -> str:
        return "\n\n".join(doc.page_content for doc in docs)

    @staticmethod
    def _build_model():
        token = os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv("HF_TOKEN")
        if token:
            token = token.strip().strip('"').strip("'")

        if not token:
            raise RuntimeError(
                "Missing Hugging Face token. Set HUGGINGFACEHUB_API_TOKEN or HF_TOKEN."
            )

        # Backward compatibility with older huggingface_hub builds in local envs.
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = token
        os.environ["HF_TOKEN"] = token
        os.environ["HUGGING_FACE_HUB_TOKEN"] = token

        llm = HuggingFaceEndpoint(
            repo_id=os.getenv("HF_REPO_ID", "meta-llama/Llama-3.1-8B-Instruct"),
            task=os.getenv("HF_TASK", "text-generation"),
            temperature=float(os.getenv("HF_TEMPERATURE", "0.3")),
            max_new_tokens=int(os.getenv("HF_MAX_NEW_TOKENS", "512")),
            huggingfacehub_api_token=token,
        )
        return ChatHuggingFace(llm=llm)

    def _build_retriever(self, video_url: str) -> Tuple[str, object]:
        video_id, transcript = self.loader.load_transcript(video_url)
        if not video_id:
            raise ValueError("Invalid YouTube URL.")
        if not transcript:
            raise ValueError("No transcript found for this video.")

        chunks = self.splitter.script_splitter(transcript)
        vector_store = self.embeddings.create_embedding(chunks)
        retriever = self.retriever_builder.semantic_search(vector_store)
        self.retriever_cache[video_id] = retriever

        return video_id, retriever

    def _get_retriever(self, video_url: str) -> Tuple[str, object]:
        video_id = self.loader.extract_video_id(video_url)
        if video_id and video_id in self.retriever_cache:
            return video_id, self.retriever_cache[video_id]

        return self._build_retriever(video_url)

    def ask(self, video_url: str, question: str) -> Dict[str, str]:
        cleaned_question = question.strip()
        if not cleaned_question:
            raise ValueError("Question is required.")

        video_id, retriever = self._get_retriever(video_url)

        chain = (
            {
                "context": itemgetter("question")
                | retriever
                | RunnableLambda(self._format_docs),
                "question": itemgetter("question"),
            }
            | self.prompt
            | self.model
            | self.parser
        )

        answer = chain.invoke({"question": cleaned_question}).strip()

        return {
            "video_id": video_id,
            "answer": answer,
        }
