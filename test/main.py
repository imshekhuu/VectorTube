from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint, HuggingFaceEmbeddings
from urllib.parse import urlparse, parse_qs
import re
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
import streamlit as st

load_dotenv()

# ---------------- UI ----------------
st.set_page_config(page_title="YouTube RAG Chatbot")

st.title("🎥 YouTube Transcript Chat")

with st.sidebar:
    video_link = st.text_input("Enter YouTube Video Link")
question = st.text_input("Ask your Question")
run_btn = st.button("Ask")



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
            api = YouTubeTranscriptApi()
            transcript_list = api.fetch(self.video_id)
            self.transcript = " ".join(chunk.text for chunk in transcript_list)
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



def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

if run_btn and video_link and question:

    with st.spinner("Processing..."):


        YouTubeclass = YouTubeTranscript(video_link)
        YouTubeclass.extract_id()
        YouTubeclass.fetch_transcript()
        chunks = YouTubeclass.split_transcript()

        if not chunks:
            raise ValueError("No transcript chunks found.")



        Embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vector_store = FAISS.from_documents(chunks, Embedding)

        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )



        llm = HuggingFaceEndpoint(
            repo_id="HuggingFaceH4/zephyr-7b-beta",
            task="text-generation",
            temperature=0.3,
            max_new_tokens=512,
        )

        model = ChatHuggingFace(llm=llm)



        prompt = PromptTemplate(
            template="""
        You are a helpful assistant.
        Answer ONLY from the provided transcript context.
        If the context is insufficient, just say you don't know.

        {context}
        Question: {question}
        """,
            input_variables=['context', 'question']
        )


        parser = StrOutputParser()

        main_chain = (
            {
                "context": itemgetter("question") | retriever | RunnableLambda(format_docs),
                "question": itemgetter("question")
            }
            | prompt
            | model
            | parser
        )



        final_output = main_chain.invoke({
            "question": question
        })

        st.subheader("Answer")
        st.write(final_output)
