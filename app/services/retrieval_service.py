
import numpy as np
from app.services.embedding_service import get_embeddings


def retrieve_top_k(query: str, index, chunks: list, k: int = 3, score_threshold: float | None = None):
    """
    Embed the query, search FAISS index, and return top-k chunks with metadata and scores.
    """
    # 1. Query → embedding
    query_embedding = get_embeddings([query])[0]

    # 2. FAISS search
    query_vector = np.array([query_embedding], dtype="float32")
    distances, indices = index.search(query_vector, k)

    results = []
    for idx, dist in zip(indices[0], distances[0]):
        if idx == -1:
            continue

        chunk = chunks[idx]

        if score_threshold is not None and dist > score_threshold:
            continue

        results.append({
            "text": chunk["text"],
            "doc_name": chunk.get("doc_name"),
            "page": chunk.get("page"),
            "score": float(dist),
            "index": int(idx),
        })

    return results