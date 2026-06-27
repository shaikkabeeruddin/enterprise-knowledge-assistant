# Enterprise Knowledge Assistant

A production-oriented Retrieval Augmented Generation (RAG) application that answers questions from enterprise documents using semantic search and LLM-based grounded generation.

## Overview

This project was built as part of the AI Engineer assignment to create an Enterprise Knowledge Assistant for internal company documents. 

The system allows users to:
- Upload PDF documents
- Extract and chunk document text
- Generate embeddings and store them in a FAISS vector index
- Ask natural language questions
- Retrieve relevant context from the indexed documents
- Generate concise answers using Gemini
- Display document-level source references

## Architecture Diagram

## Architecture Diagram

User → Streamlit UI → FastAPI Backend

Document Ingestion Flow:
PDF Upload → Text Extraction → Text Chunking → Metadata Attachment → Embedding Generation → FAISS Index Storage

Question Answering Flow:
User Question → Query Embedding → Semantic Retrieval from FAISS → Top-k Relevant Chunks → Gemini LLM → Answer + Sources → Streamlit UI

## Architecture Overview

The application follows a simple RAG pipeline. 

1. **Document Ingestion**
   - Upload PDF through the API or Streamlit UI
   - Extract text from the PDF
   - Split text into chunks
   - Attach metadata such as document name and page placeholder
   - Generate embeddings for each chunk
   - Store vectors and metadata in FAISS

2. **Query Processing**
   - Accept a user question
   - Convert the question into an embedding
   - Retrieve top-k relevant chunks from FAISS
   - Build a prompt using only retrieved context
   - Generate an answer with Gemini
   - Return the answer, sources, and confidence score

## Tech Stack

The implementation uses the following stack:

- **Backend:** FastAPI
- **Frontend/UI:** Streamlit
- **Vector Store:** FAISS
- **LLM:** Google Gemini 2.5 Flash
- **PDF Parsing:** PyPDF2
- **Language:** Python
- **HTTP Client:** requests

This stack was chosen because the assignment allows any technology stack and explicitly lists Python, vector databases, LLMs, and simple UI options such as Streamlit and API endpoints. 

## Project Structure

```text
project/
├── app/
│   ├── main.py
│   ├── routes/
│   │   ├── upload.py
│   │   └── query.py
│   ├── services/
│   │   ├── pdf_service.py
│   │   ├── chunk_service.py
│   │   ├── embedding_service.py
│   │   ├── faiss_service.py
│   │   ├── retrieval_service.py
│   │   └── llm_service.py
│   └── utils/
│       └── config.py
├── data/
│   ├── uploads/
│   └── faiss_index/
├── frontend/
    ├── app.py
├── requirements.txt
└── README.md
```

## Features Implemented

### Core Requirements

- PDF upload and ingestion 
- Text extraction from uploaded documents 
- Chunking strategy for document processing 
- Metadata attachment for indexed chunks 
- Embedding generation and FAISS indexing 
- Semantic retrieval using top-k nearest chunks 
- Context-aware answer generation 
- Hallucination prevention through prompt constraints 
- Source reference display in the UI 
- Streamlit-based interaction interface 
- FastAPI-based `/ask` endpoint, which is preferred in the assignment 

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

In utils/config.py add your google gemini api key

```
GOOGLE_API_KEY=your_google_api_key_here
```

### 4. Run the FastAPI backend

```bash
uvicorn app.main:app --reload
```

### 5. Run the Streamlit frontend

```bash
streamlit run frontend/app.py
```

## API Usage

### Upload a PDF

**Endpoint:**
```http
POST /upload/
```

Upload a PDF document as multipart form-data.

### Ask a Question

**Endpoint:**
```http
POST /ask
```

**Request**
```json
{
  "question": "What is the refund policy?"
}
```

**Response**
```json
{
  "question": "What is the refund policy?",
  "answer": "Refunds are allowed within 30 days.",
  "sources": [
    {
      "document": "Customer_Policy.pdf",
      "page": 5
    }
  ]
}
```

This matches the assignment’s preferred API style for question answering systems.

"The page number in the output is printed only if it founds the page number from the source file where the output is generated. Page numbers are shown only when page metadata is available from the source document."

## Design Decisions

### 1. FAISS for vector retrieval
FAISS was selected because it is lightweight, fast, local, and easy to integrate for a prototype RAG system. The assignment explicitly accepts FAISS as a valid vector database option.

### 2. Chunk-based retrieval
Documents are split into smaller chunks so that semantic retrieval can focus on relevant passages instead of searching an entire PDF at once. This improves retrieval quality and reduces prompt noise. 

### 3. Prompt-grounded answer generation
The LLM prompt explicitly instructs the model to answer only from retrieved context and say “I don't know based on the available documents.” when support is missing. This was done to reduce hallucinations, which is a stated evaluation focus in the assignment. 

### 4. Streamlit for fast UI delivery
Streamlit was chosen because the assignment accepts Streamlit applications and the time constraint favors a fast, clear, working interface. 

### 5. API-first backend design
FastAPI endpoints were added so the system can be used through both the UI and direct API requests. This improves modularity and aligns with the assignment’s preference for an API layer. 

## Retrieval and Answering Flow

1. User uploads a PDF.
2. Text is extracted from the PDF.
3. Extracted text is chunked into smaller segments.
4. Embeddings are generated for each chunk.
5. Embeddings are stored in a FAISS index with metadata.
6. User asks a question.
7. The question is embedded.
8. Top-k similar chunks are retrieved.
9. Retrieved chunks are passed to Gemini as context.
10. The model generates a grounded response.
11. The system returns the answer and source document reference.

## Evaluation Approach

The assignment asks for an explanation of how performance was measured, what test cases were created, and what improvements were attempted. 

The current evaluation approach is manual but structured:

- Test factual questions whose answers clearly exist in the documents.
- Test paraphrased questions to verify semantic retrieval.
- Test unsupported questions to verify “I don’t know” behavior.
- Check whether returned sources match the answer context.
- Observe whether the answer is concise, relevant, and grounded.

### Example test categories

- Direct factual lookup, for example: “What is the refund policy?”
- Summary-style question, for example: “What is AnthraSuite used for?”
- Ambiguous question, for example: “Tell me about policies.”
- Unanswerable question, for example: a topic not present in the uploaded document

### Improvements attempted

- Removed duplicate sources from the API response
- Hid sources when the answer is unavailable
- Prevented `Page None` from being shown in the UI when page metadata is missing
- Added explicit prompt instructions to avoid hallucination
- Structured the response to include answer, source, and confidence

## Engineering Quality Considerations

### Code structure
The project is split into routes and services for cleaner separation of concerns, which improves maintainability and readability. 

### Error handling
The application includes handling for:
- Empty PDF uploads
- Missing question input
- Missing FAISS index
- LLM request errors
- UI request failures

### Maintainability
Service-based separation allows individual components such as retrieval, indexing, and LLM integration to be updated independently. 

### Scalability considerations
For larger-scale production use, the following upgrades would be recommended:
- Replace local FAISS storage with a managed vector database
- Add background ingestion jobs
- Support multi-user document collections
- Add authentication and authorization
- Add caching for repeated queries
- Add better metadata and true page-level tracking
- Introduce re-ranking or hybrid retrieval

These align with the assignment’s emphasis on scalability and production-oriented design. 

## Known Limitations

- Page-level citation is not fully reliable because the current prototype does not preserve exact PDF page mapping through chunk creation.
- Retrieval is currently semantic only; it does not yet include hybrid keyword search.
- Confidence is heuristic and not model-calibrated.
- Only PDF input is currently supported.
- Multi-document reasoning is limited in the current prototype.
- Conversation memory is not implemented.

## Future Improvements

- True page-aware chunking and citations
- Hybrid search using keyword + semantic retrieval
- Re-ranking retrieved chunks before answer generation
- Query rewriting for ambiguous questions
- Feedback collection for answers
- Authentication and user access control
- Deployment on cloud infrastructure
- Better automated evaluation metrics
- Support for DOCX, TXT, and HTML documents


