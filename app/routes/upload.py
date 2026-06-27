
from fastapi import APIRouter, UploadFile, File
import os

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import chunk_text
from app.services.embedding_service import get_embeddings
from app.services.faiss_service import load_faiss, append_to_index

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    # 1. Save uploaded PDF
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # 2. Extract text
    text = extract_text_from_pdf(file_path)

    # 3. Chunk text (sentence-based, 500 chars, 1 sentence overlap)
    raw_chunks = chunk_text(text, chunk_size=500, overlap_sentences=1)
    if not raw_chunks:
        return {"error": "Empty PDF or no extractable text"}

    # 4. Add metadata (doc_name, optional page)
    # For now we don't track page; you can extend later if needed.
    chunks = [
        {
            "text": c,
            "doc_name": file.filename,
            "page": None,
        }
        for c in raw_chunks
    ]

    # 5. Embeddings for new chunks
    embeddings = get_embeddings([c["text"] for c in chunks])

    # 6. Load existing index + chunks, then append
    existing_index, existing_chunks = load_faiss()
    index, all_chunks = append_to_index(existing_index, existing_chunks, embeddings, chunks)

    return {
        "message": "PDF processed and stored successfully",
        "filename": file.filename,
        "num_new_chunks": len(chunks),
        "num_total_chunks": len(all_chunks),
    }