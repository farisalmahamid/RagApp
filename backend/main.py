from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
from db_utils import add_document_to_db, get_pdf_text
from pydantic import BaseModel
from openai import OpenAI
from db_utils import query_db
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    question: str

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("temp_files", exist_ok=True)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_location = f"temp_files/{file.filename}"
    
   
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    
    if file.filename.endswith(".pdf"):
        text = get_pdf_text(file_location)
    elif file.filename.endswith(".txt"):
        with open(file_location, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        return {"error": "Unsupported file type"}
        
   
    num_chunks = add_document_to_db(file.filename, text)
    
    
    os.remove(file_location)
    
    return {"message": f"Successfully processed {file.filename} into {num_chunks} chunks."}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    
    context = query_db(request.question)
    
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Answer the user question based ONLY on the context provided below."},
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {request.question}"}
    ]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    answer = response.choices[0].message.content
    return {"answer": answer, "context_used": context}