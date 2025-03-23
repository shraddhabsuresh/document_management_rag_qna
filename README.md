Document Management and RAG-based Q&A Application
📝 Overview
This project is a Document Management and Retrieval-Augmented Generation (RAG) based Question-and-Answer application. It allows users to:

Ingest documents and generate embeddings using a Large Language Model (LLM)

Perform retrieval-based Q&A to get accurate answers using relevant documents

Select specific documents to narrow down the search for more accurate results

🚀 Features
Document Ingestion API for uploading documents and generating embeddings

Q&A API for answering user queries using RAG

Document Selection API for filtering specific documents for Q&A

Scalable backend with asynchronous API handling

Efficient storage using PostgreSQL for storing embeddings

🛠️ Tech Stack
Programming Language: Python

Framework: FastAPI

Database: PostgreSQL

Embeddings: Using LLM via Ollama Llama 3.18B, LangChain, or Hugging Face

Libraries: Scikit-learn, BM25, TF-IDF

ORM: SQLAlchemy

Containerization: Docker (optional)

⚙️ Installation and Setup
Clone the Repository

bash
Copy
Edit
git clone https://github.com/shraddhabsuresh/document_management_rag_qna.git
cd document_management_rag_qna
Create a Virtual Environment (Recommended)

bash
Copy
Edit
python -m venv env
source env/bin/activate  # On macOS/Linux
env\Scripts\activate     # On Windows
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Set Environment Variables
Create a .env file in the root directory:

env
Copy
Edit
DATABASE_URL=postgresql://username:password@localhost/document_rag
SECRET_KEY=your_secret_key
Run Database Migrations

bash
Copy
Edit
alembic upgrade head
Start the Application

bash
Copy
Edit
uvicorn app.main:app --reload
Access APIs

API Docs available at: http://localhost:8000/docs

📤 APIs Overview
Document Ingestion API

Endpoint: POST /documents/upload

Purpose: Upload documents and generate embeddings

Q&A API

Endpoint: POST /query

Purpose: Accept user questions and retrieve relevant answers using RAG

Document Selection API

Endpoint: POST /documents/select

Purpose: Allow users to select specific documents for Q&A

🧑‍💻 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.

Create a new branch (git checkout -b feature/new-feature).

Commit changes (git commit -m 'Add new feature').

Push to the branch (git push origin feature/new-feature).

Open a pull request.

