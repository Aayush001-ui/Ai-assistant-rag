# AI Assistant (RAG + Llama3)

A local AI assistant that answers questions based on uploaded PDF documents using Retrieval-Augmented Generation (RAG).

## Tech Stack

- Python (FastAPI)
- Llama 3 (via Ollama)
- FAISS (Vector Database)
- Sentence Transformers (Embeddings)
- HTML, CSS, JavaScript (Frontend)

## Features

-  Chat interface similar to ChatGPT
-  Upload PDF documents
-  Context-aware answers using RAG
-  Local LLM (no external API required)
-  Dynamic document processing after upload


##  How It Works

1. User uploads a PDF document  
2. Text is extracted and split into chunks  
3. Each chunk is converted into embeddings  
4. Embeddings are stored in FAISS vector database  
5. User query is converted into embedding  
6. Relevant chunks are retrieved using similarity search  
7. LLM generates answer using retrieved context  

##  Example Workflow

Upload a PDF → Ask a question → Get a contextual answer based on document content

## ▶ How to Run Locally

### 1. Install dependencies
### 2. Run Ollama (LLM)
### 3. Start backend
### 4. Open frontend

##  Limitations

- Supports one active document at a time  
- Basic chunking (can be improved with overlap)  
- No chat memory (stateless responses)  

##  Future Improvements

- Multi-document support  
- Chat memory (conversation context)  
- Improved chunking strategy  
- Better UI/UX  

##  Screenshots

(Add screenshots of your UI here before uploading to GitHub)


##  Learning Outcome

This project helped me understand:

- Retrieval-Augmented Generation (RAG)
- Embeddings and vector search
- How LLM-based systems work internally
- Building full-stack AI applications

##  Author

Aayush Kasaudhan  


