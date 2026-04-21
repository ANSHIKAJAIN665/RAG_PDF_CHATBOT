🚀 RAG PDF Chatbot

🔗 Live Demo: https://ragpdfchatbot-5gsrudr6xrzlemgerp8nqw.streamlit.app [Not fully deployed (uses local LLM via Ollama)]
📌 Overview

This project is a Retrieval-Augmented Generation (RAG) based PDF Question Answering system that allows users to ask questions from documents and get accurate, context-based answers.

It retrieves relevant content from PDFs using semantic search and generates grounded responses using a Large Language Model.

🧠 How It Works (RAG Pipeline)

PDF → Text Chunking → Embeddings → FAISS → Retrieval → LLM → Answer

Steps:
PDF is loaded using PyPDFLoader
Text is split into chunks
Chunks are converted into embeddings
Stored in FAISS vector database
User query retrieves relevant chunks
LLM generates context-based answer
⚙️ Tech Stack
LangChain
FAISS
FastAPI
Streamlit
Ollama (Local LLM)
PyPDF
✨ Features
📄 Ask questions from PDF documents
🔍 Semantic search using embeddings
🧠 Context-aware answer generation
📌 Source attribution (page number)
⚡ FastAPI backend
🌐 Streamlit interactive UI
💸 Runs locally (no API cost)
📂 Project Structure

rag_pdf_chatbot/
│
├── api.py
├── ui.py
├── data/
│ ├── sample.pdf
│ ├── cricket.pdf
│
├── requirements.txt
├── README.md

🚀 How to Run
1️⃣ Install dependencies

pip install -r requirements.txt

2️⃣ Start backend (FastAPI)

uvicorn api:app --reload

3️⃣ Start frontend (Streamlit)

streamlit run ui.py

4️⃣ Open UI

http://localhost:8501

🧪 Example Queries
What is this document about?
What are the formats of cricket?
Who are famous cricket players?
Summarize the document
⚠️ Note
This project uses a local LLM via Ollama
Ensure Ollama is running:
ollama run llama3
🎯 Future Improvements
Upload multiple PDFs dynamically
Add chat history (memory)
Deploy full system online
Use advanced vector databases (Pinecone, ChromaDB)
👩‍💻 Author

Anshika Jain
