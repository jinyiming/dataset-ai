from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from models.qa_model import QAModel

app = APIRouter()
model = QAModel()

class GenerateRequest(BaseModel):
    prompt: str
    count: int = 10

class QAPair(BaseModel):
    question: str
    answer: str

class GenerateResponse(BaseModel):
    qa_pairs: List[QAPair]

@app.post("/generate", response_model=GenerateResponse)
async def generate_qa(request: GenerateRequest):
    try:
        qa_pairs = model.generate(request.prompt, request.count)
        return GenerateResponse(qa_pairs=qa_pairs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 