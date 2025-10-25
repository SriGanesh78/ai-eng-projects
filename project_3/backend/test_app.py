# Simple test backend
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask(req: AskRequest):
    """Simple test endpoint"""
    return {"answer": f"Test response for: {req.question}"}

@app.get("/")
async def root():
    return {"message": "Backend is running!"}
