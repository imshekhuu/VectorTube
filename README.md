# 🎥 YouTube Transcript RAG Chatbot

An AI chatbot that lets users **chat with YouTube video transcripts**
using Retrieval-Augmented Generation (RAG).

The system extracts transcripts, converts them into embeddings,
retrieves relevant context, and generates accurate answers using an LLM.

------------------------------------------------------------------------

# 🚀 Features

-   Chat with YouTube videos
-   Transcript-based answers
-   RAG Architecture
-   Vector Database Search
-   Clean Web UI
-   Context-aware responses

------------------------------------------------------------------------

# 🧠 How It Works

1.  Extract YouTube Transcript
2.  Split into text chunks
3.  Generate embeddings
4.  Store in Vector Database
5.  Retrieve relevant context
6.  Send context + query to LLM
7.  Generate final response

------------------------------------------------------------------------

# 🏗️ Architecture Diagram

Add your architecture image here:

![RAG Architecture](/screenshots/IMG_0747.PNG)

------------------------------------------------------------------------

# 🎨 UI Screenshots

Place your UI images inside the `/screenshots` folder.

Example:

![Home UI](screenshots/home.png) ![Chat UI](screenshots/chat.png) ![Dark
Mode UI](screenshots/ui_dark.png)

------------------------------------------------------------------------

# 📂 Project Structure

    VectorTube/
    │
    ├── app.py
    ├── requirements.txt
    ├── rag/
    │   ├── loader.py
    │   ├── embeddings.py
    │   ├── retriever.py
    │   └── chain.py
    │
    ├── templates/
    ├── static/
    └── screenshots/

------------------------------------------------------------------------

# ⚙️ Installation

``` bash
git clone https://github.com/imshekhuu/VectorTube.git
cd youtube-transcript-chatbot

python -m venv env
env\Scripts\activate

pip install -r requirements.txt
```

------------------------------------------------------------------------

# ▶️ Run Project

``` bash
python app.py
```

Open:

http://localhost:5000

------------------------------------------------------------------------

# 🔧 Tech Stack

-   Python
-   LangChain
-   FAISS / ChromaDB
-   Flask
-   HTML CSS JavaScript
-   LLM API

------------------------------------------------------------------------

# 📈 Future Improvements

-   Multiple video support
-   Streaming responses
-   Authentication
-   Cloud deployment

------------------------------------------------------------------------

# 👨‍💻 Author

Divya S. Shekhekhawat
