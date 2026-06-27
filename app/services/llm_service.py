  
    
    
from google import genai
from google.genai.types import GenerateContentConfig, HttpOptions
from app.utils.config import GOOGLE_API_KEY

client = genai.Client(
    api_key=GOOGLE_API_KEY,
    http_options=HttpOptions(api_version="v1"),
)


def generate_answer(query: str, context_chunks: list[dict]) -> dict:
    context_parts = []
    for c in context_chunks:
        doc_name = c.get("doc_name", "unknown_document")
        page = c.get("page", "?")
        meta = f"[DOC: {doc_name} | PAGE: {page}]"
        context_parts.append(f"{meta}\n{c.get('text', '')}")

    context = "\n\n".join(context_parts) if context_parts else "No context available."

    prompt = f"""
You are an expert enterprise knowledge assistant.

Answer the question using ONLY the provided context from internal documents.
If the answer is not in the context, clearly say "I don't know based on the available documents."

Be clear, concise, and structured. Do not invent policies or numbers that are not present in the context.

Context:
{context}

Question:
{query}

Answer:
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt,
            config=GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=512,
            ),
        )
        answer_text = response.text or ""
    except Exception as e:
        answer_text = f"LLM error: {e}"

    # If answer is "I don't know...", return no sources
    normalized_answer = answer_text.strip().lower()
    if "i don't know based on the available documents" in normalized_answer:
        return {
            "answer": "I don't know based on the available documents.",
            "sources": []
        }

    # Deduplicate sources and keep best one
    seen = set()
    unique_sources = []
    for c in context_chunks:
        key = (c.get("doc_name"), c.get("page"))
        if key in seen:
            continue
        seen.add(key)
        unique_sources.append({
            "document": c.get("doc_name"),
            "page": c.get("page"),
        })

    if unique_sources:
        sources = [unique_sources[0]]
    else:
        sources = []

    return {
        "answer": answer_text,
        "sources": sources,
    }