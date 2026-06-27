
    
import os
import faiss
import pickle
import numpy as np

INDEX_PATH = "data/faiss_index/faiss_index.index"
CHUNKS_PATH = "data/faiss_index/chunks.pkl"


def create_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """
    Create a new FAISS index from embeddings.
    """
    vectors = np.array(embeddings, dtype="float32")
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)
    return index


def save_faiss(index: faiss.IndexFlatL2, chunks: list) -> None:
    """
    Persist FAISS index + chunk metadata to disk.
    """
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)


def load_faiss():
    """
    Load FAISS index + chunk metadata. Returns (index, chunks).
    If not existing yet, returns (None, []).
    """
    if not os.path.exists(INDEX_PATH) or not os.path.exists(CHUNKS_PATH):
        return None, []

    index = faiss.read_index(INDEX_PATH)

    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)

    return index, chunks


def append_to_index(existing_index, existing_chunks, new_embeddings, new_chunks):
    """
    Append new embeddings/chunks to existing index, or create a new one if none exists.
    """
    vectors = np.array(new_embeddings, dtype="float32")

    if existing_index is None:
        index = create_faiss_index(vectors)
        chunks = new_chunks
    else:
        index = existing_index
        index.add(vectors)
        chunks = existing_chunks + new_chunks

    save_faiss(index, chunks)
    return index, chunks