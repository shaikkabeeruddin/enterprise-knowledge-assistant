from google import genai
from app.utils.config import GOOGLE_API_KEY

client = genai.Client(
    api_key=GOOGLE_API_KEY
)

def get_embeddings(chunks):
    embeddings = []

    for chunk in chunks:
        if not chunk.strip():
            continue

        response = client.models.embed_content(
            model="models/gemini-embedding-2",   
            contents=chunk
        )

        embeddings.append(response.embeddings[0].values)

    return embeddings