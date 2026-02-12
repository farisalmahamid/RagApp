import os
import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

# Setup OpenAI Embedding Function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

# Initialize ChromaDB (The Vector Database)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(
    name="documents",
    embedding_function=openai_ef
)

def get_pdf_text(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def add_document_to_db(file_name, file_text):
    # We split text into chunks (simplified for beginner: chunks of 1000 chars)
    chunk_size = 1000
    chunks = [file_text[i:i+chunk_size] for i in range(0, len(file_text), chunk_size)]
    
    # Generate unique IDs for chunks
    ids = [f"{file_name}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": file_name} for _ in chunks]

    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas
    )
    return len(chunks)

def query_db(query_text, n_results=3):
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    # Combine the retrieved text chunks into one string
    context_text = " ".join(results['documents'][0])
    return context_text