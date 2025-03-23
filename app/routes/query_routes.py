from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
def query_api(request: QueryRequest):
    return {"message": f"Processing query: {request.question}"}
