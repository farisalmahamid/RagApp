# Personal Knowledge Assistant (RAG App)
Application that allows users to upload documents (PDF/TXT) and chat with them using OpenAI.

## Architecture
- **Backend:** FastAPI (Python) handles API requests.
- **Frontend:** React provides the UI.
- **AI:** OpenAI GPT-3.5 for answers, text-embedding-3-small for embeddings.

## Setup Instructions
-Navigate to 'backend/' and install requirements: pip install -r requirements.txt

-Add your OpenAi key in ".env" file in "backend/" with: OPENAI_API_KEY=your_key

-Creat virtual environment: python -m venv venv

-Activate: venv\Scripts\activate

-Run backend: uvicorn main:app --reload

-Navigate to 'frontend/' and install dependencies: "npm install"

-Run frontend: npm start

-Open the app in the browser: 'http://localhost:3000'
