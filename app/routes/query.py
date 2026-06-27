
        
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.faiss_service import load_faiss
from app.services.retrieval_service import retrieve_top_k
from app.services.llm_service import generate_answer


router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_question(request: QueryRequest):
    try:
        question = request.question

        # 1. Load FAISS index + chunk metadata
        index, chunks = load_faiss()
        if index is None or not chunks:
            return {"error": "No documents indexed yet. Please upload PDFs first."}

        # 2. Retrieve top-k chunks (with text + metadata + score)
        top_chunks = retrieve_top_k(question, index, chunks, k=5)

        if not top_chunks:
            # No relevant context found → grounded "I don't know"
            return {
                "question": question,
                "answer": "I don't know based on the available documents.",
                "sources": [],
            }

        # 3. Generate answer from LLM using retrieved context
        result = generate_answer(question, top_chunks)


        return {
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"],
        }

    except Exception as e:
        return {"error": str(e)}