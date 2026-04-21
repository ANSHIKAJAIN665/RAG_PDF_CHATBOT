import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel

# LangChain imports
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableMap


# ===== INIT APP =====
app = FastAPI(title="RAG Chatbot API")


# ===== REQUEST MODEL =====
class QueryRequest(BaseModel):
    question: str


# ===== LOAD + PREPARE =====
print("📄 Loading PDF...")
loader = PyPDFLoader("data/sample.pdf")
documents = loader.load()

print("✂️ Splitting...")
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)

print("🧠 Creating vector store...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vectorstore = FAISS.from_documents(chunks, embeddings)

print("🤖 Loading LLM...")
llm = OllamaLLM(model="llama3")

prompt = PromptTemplate.from_template(
    """Answer based only on the context below.

Context:
{context}

Question:
{question}
"""
)

retriever = vectorstore.as_retriever()


# ===== RAG CHAIN =====
rag_chain = (
    RunnableMap({
        "docs": retriever,
        "question": RunnablePassthrough()
    })
    | (lambda x: {
        "context": "\n\n".join(doc.page_content for doc in x["docs"]),
        "question": x["question"],
        "sources": [
            {
                "page": doc.metadata.get("page", 0) + 1,
                "file": os.path.basename(doc.metadata.get("source", ""))
            }
            for doc in x["docs"]
        ]
    })
    | {
        "answer": prompt | llm,
        "sources": lambda x: x["sources"]
    }
)


# ===== ROUTES =====

@app.get("/")
def home():
    return {"message": "RAG API is running 🚀"}


@app.post("/ask")
def ask_question(request: QueryRequest):
    result = rag_chain.invoke(request.question)

    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }