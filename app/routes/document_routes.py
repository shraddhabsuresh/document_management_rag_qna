from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
# from app.core.database import get_db
import logging
from pydantic import BaseModel
from transformers import pipeline
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy.sql import text
from pydantic import BaseModel
from fastapi import HTTPException, APIRouter


# ✅ Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ✅ Initialize FastAPI router with "/api" prefix
router = APIRouter()
# router = APIRouter(prefix="/api")

# ✅ Debugging print
logger.info("✅ document_routes loaded")

# ✅ Define Pydantic model for request body
class QuestionRequest(BaseModel):
    question: str

# ✅ Load pre-trained QA model
qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# ✅ Embedding model for document embeddings
embedder = pipeline("feature-extraction", model="sentence-transformers/all-MiniLM-L6-v2")

async def get_relevant_documents(question: str, db: AsyncSession):
    try:
        logger.info("Fetching relevant documents from database...")
        
        query = text("SELECT id, text FROM documents")  # Ensure your schema has `text`
        result = await db.execute(query)
        documents = result.fetchall()

        if not documents:
            logger.warning("⚠️ No documents found in the database!")

        return documents
    except Exception as e:
        logger.error(f"🔥 Database error in get_relevant_documents: {e}", exc_info=True)
        return []


def get_relevant_embeddings(question: str, db: Session):
    try:
        query = "SELECT embedding FROM documents;"  # Simplified for now
        result = db.execute(query).fetchall()
        logging.debug(f"Retrieved embeddings: {result}")
        return result
    except Exception as e:
        logging.error(f"Database error: {e}")
        return []

async def generate_answer(question: str, documents: list):
    try:
        logger.info("Generating answer using QA model...")
        context = " ".join([doc.text for doc in documents])  # Ensure doc.text exists
        logger.info(f"Using context: {context[:100]}...")  # Log first 100 chars of context
        answer = qa_model(question=question, context=context)
        logger.info(f"Generated answer: {answer}")
        return answer["answer"]
    except Exception as e:
        logger.error(f"Error generating answer: {e}", exc_info=True)
        return "Could not generate answer"

@router.post("/api/ask")
async def ask_question(question: dict):
    logging.debug(f"Received question: {question}")
    try:
        if "question" not in question:
            raise HTTPException(status_code=400, detail="Missing 'question' field")

        user_question = question["question"]
        logging.debug(f"Processing question: {user_question}")

        # Retrieve relevant documents
        documents = await get_relevant_documents(user_question, db=None)  # Pass DB session correctly
        logging.debug(f"Retrieved {len(documents)} documents")

        # Generate answer
        answer = await generate_answer(user_question, documents)
        logging.debug(f"Generated answer: {answer}")

        return {"answer": answer}

    except Exception as e:
        logging.error(f"🔥 ERROR in /api/ask: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Endpoint to upload and process documents."""
    try:
        contents = await file.read()
        # TODO: Process and store the document
        logger.info(f"Received file: {file.filename}, size: {len(contents)} bytes")
        return {"filename": file.filename, "message": "File uploaded successfully"}

    except Exception as e:
        logger.error(f"Error processing file upload: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to upload file")

@router.post("/api/select-document")
async def select_document(doc_id: int, db: Session = Depends(get_db)):
    try:
        query = "SELECT * FROM documents WHERE id = :doc_id"
        result = db.execute(query, {"doc_id": doc_id}).fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Document not found")

        return {"message": f"Document {doc_id} selected for Q&A"}
    except Exception as e:
        logging.error(f"Error selecting document: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

from rank_bm25 import BM25Okapi
from app.database import get_db

def retrieve_best_document(question: str, db: Session):
    documents = db.execute("SELECT id, filename, embedding FROM documents;").fetchall()
    tokenized_docs = [doc["embedding"]["vector"] for doc in documents]
    
    bm25 = BM25Okapi(tokenized_docs)
    scores = bm25.get_scores(question.split())
    
    best_doc_idx = scores.argmax()
    return documents[best_doc_idx]

