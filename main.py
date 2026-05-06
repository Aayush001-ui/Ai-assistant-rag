import pytz
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from rag_engine import RAGEngine
from ollama_client import OllamaClient
from config import TOP_K_RESULTS
from fastapi.middleware.cors import CORSMiddleware
from fastapi import File, UploadFile
import shutil


# Initialize App
app = FastAPI(
    title="AI Assistant (RAG + Llama3)",
    description="Local AI assistant using Ollama + FAISS",
    version="2.0"
)

# ADD CORS HERE (AFTER app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Components
rag_engine = RAGEngine()
ollama_client = OllamaClient()

DOCUMENT_PATH = "data/documents/sample.pdf"


# Request Model
class ChatRequest(BaseModel):
    query: str


# Utility: Clean Text
def clean_text(text: str) -> str:
    if not text:
        return ""
    return text.replace("\n", " ").replace("\r", " ").strip()


# function for Date and time 
def get_current_time():
    tz = pytz.timezone("Asia/Kolkata")
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")


# Startup Event
@app.on_event("startup")
def startup_event():
    if not os.path.exists(DOCUMENT_PATH):
        raise FileNotFoundError(f"Document not found: {DOCUMENT_PATH}")

    rag_engine.build_index(DOCUMENT_PATH)

# Routes
@app.get("/")
def home():
    return {"message": "AI Assistant is running"}


#Basic Chat
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        query = clean_text(request.query)

        prompt = f"""
You are a helpful AI assistant.

Answer clearly and naturally.

Question:
{query}

Answer:
"""

        response = ollama_client.generate_response(prompt)
        response = clean_text(response)

        return {
            "answer": response,
            "timespent": get_current_time()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#  RAG Chat
@app.post("/ask")
def ask(request: ChatRequest):
    try:
        query = clean_text(request.query)

        # Step 1: Retrieve context
        relevant_chunks = rag_engine.search(query, TOP_K_RESULTS)

        # Step 2: Clean chunks
        cleaned_chunks = [clean_text(chunk) for chunk in relevant_chunks]

        # Step 3: Combine context
        context = " ".join(cleaned_chunks)

        # Step 4: Improved prompt
        prompt = f"""
You are an intelligent AI assistant.

Use the context below to answer the question.

- If the answer is directly present, return it.
- If not, try to logically infer from the context.
- Do NOT make up unrelated information.
- If the answer cannot be determined, say "I don't know."

Answer clearly and concisely.

Context:
{context}

Question:
{query}

Answer:
"""

        # Step 5: Generate answer
        answer = ollama_client.generate_response(prompt)
        answer = clean_text(answer)

        # Step 6: Return clean response
        return {
            "answer": answer,
            "timespent": get_current_time()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Adding upload
@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    try:
        file_path = f"data/documents/{file.filename}"

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Rebuild FAISS index
        rag_engine.build_index(file_path)

        return {"message": f"{file.filename} uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
