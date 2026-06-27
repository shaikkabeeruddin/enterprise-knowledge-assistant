import re

def chunk_text(text: str, chunk_size=500, overlap_sentences=1):
    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        if current_length + len(sentence) <= chunk_size:
            current_chunk.append(sentence)
            current_length += len(sentence)
        else:
            # save chunk
            chunks.append(" ".join(current_chunk))

            # keep overlap sentences
            current_chunk = current_chunk[-overlap_sentences:]
            current_length = sum(len(s) for s in current_chunk)

            # add new sentence
            current_chunk.append(sentence)
            current_length += len(sentence)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks