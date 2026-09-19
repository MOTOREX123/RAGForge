# RAGForge

An advanced Retrieval-Augmented Generation (RAG) chatbot for querying multiple documents using semantic retrieval, keyword retrieval, hybrid search, reranking, local LLM inference, and web search.

RAGForge is designed as a learning and portfolio project that demonstrates how a modern RAG system can be built from the ground up.

---

## Features

- Multi-document PDF ingestion
- Text chunking with overlap
- Sentence-transformer embeddings
- FAISS semantic retrieval
- BM25 keyword retrieval
- Reciprocal Rank Fusion (RRF)
- Cross-encoder reranking
- Query routing
- Local LLM inference with Ollama and Gemma
- Gemini Google Search grounding for web queries
- FastAPI backend
- React frontend
- Source citations
- Persistent FAISS vector store
- Automated component testing

---

## Architecture

RAGForge uses a multi-stage Retrieval-Augmented Generation pipeline.

```text
                         ┌─────────────────┐
                         │   User Query    │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  Query Router   │
                         └───────┬─────────┘
                                 │
                 ┌───────────────┼───────────────┐
                 │               │               │
                 ▼               ▼               ▼
            ┌─────────┐    ┌─────────┐    ┌───────────┐
            │  Local  │    │   Web   │    │  General  │
            │   RAG   │    │ Search  │    │   LLM     │
            └────┬────┘    └────┬────┘    └─────┬─────┘
                 │               │               │
                 ▼               ▼               │
          ┌─────────────┐ ┌──────────────┐      │
          │   Hybrid    │ │    Gemini    │      │
          │  Retrieval  │ │ Google Search│      │
          └──────┬──────┘ └──────┬───────┘      │
                 │               │               │
                 ▼               │               │
          ┌─────────────┐        │               │
          │  Cross-     │        │               │
          │  Encoder    │        │               │
          │  Reranker   │        │               │
          └──────┬──────┘        │               │
                 │               │               │
                 └───────────────┼───────────────┘
                                 │
                                 ▼
                         ┌─────────────────┐
                         │  Final Answer   │
                         │  + Citations    │
                         └─────────────────┘

How RAGForge Works

1. Document Ingestion

PDF documents are placed inside the data/ directory.

The ingestion pipeline:

PDF Documents
      │
      ▼
PDF Loader
      │
      ▼
Extracted Text
      │
      ▼
Text Chunking
      │
      ▼
Embeddings
      │
      ▼
FAISS Vector Store


2. Text Chunking

Large documents are divided into smaller overlapping chunks.

The current chunking configuration uses:

Chunk size: 500 characters
Overlap: 100 characters

The overlap helps preserve context between neighboring chunks.

Document
────────────────────────────────────────────────────────

Chunk 1
████████████████████████████████████████

                    Chunk 2
                    ████████████████████████████████████████

                                        Chunk 3
                                        ████████████████████████████████████████

3. Embeddings

Each text chunk is converted into a numerical vector using a Sentence Transformer embedding model.

Conceptually:

"Overfitting occurs when..."
              │
              ▼
      Embedding Model
              │
              ▼
     [0.12, -0.43, 0.87, ...]

These vectors allow RAGForge to perform semantic similarity search.


4. FAISS Semantic Retrieval

FAISS is used to search the vector representations of the document chunks.

When a user asks a question:

User Question
      │
      ▼
Query Embedding
      │
      ▼
FAISS Similarity Search
      │
      ▼
Top Candidate Chunks

FAISS is useful because it can retrieve documents based on meaning rather than requiring exact keyword matches.

5. BM25 Keyword Retrieval

RAGForge also uses BM25 for lexical or keyword-based retrieval.

User Query
     │
     ▼
Tokenization
     │
     ▼
BM25 Search
     │
     ▼
Keyword-Relevant Chunks

BM25 can retrieve documents containing important terms even when semantic similarity is not strong.

6. Hybrid Retrieval

RAGForge combines:

          User Query
              │
       ┌──────┴──────┐
       │             │
       ▼             ▼
     FAISS          BM25
   Semantic       Keyword
   Retrieval      Retrieval
       │             │
       └──────┬──────┘
              │
              ▼
       Reciprocal Rank
          Fusion
             (RRF)
              │
              ▼
       Combined Candidates

This combines semantic and lexical retrieval into a single candidate list.

7. Reciprocal Rank Fusion

RRF combines the rankings produced by FAISS and BM25.

Conceptually:

FAISS ranking ─────┐
                   ├──► RRF ──► Combined ranking
BM25 ranking ──────┘

RRF gives each result a score based on its position in the individual rankings.

This allows RAGForge to combine different retrieval strategies without directly comparing their raw scores.

8. Cross-Encoder Reranking

The hybrid retriever produces candidate chunks, which are then passed to a cross-encoder reranker.

User Query
    │
    ▼
Hybrid Retrieval
    │
    ▼
Candidate Chunks
    │
    ▼
Cross-Encoder
    │
    ▼
Relevance Scores
    │
    ▼
Reranked Results

The cross-encoder evaluates the query and document together rather than embedding them independently.

This allows RAGForge to reorder the candidate documents according to their relevance to the actual question.

9. Local LLM Generation

After reranking, the most relevant chunks are provided to the local LLM.

RAGForge currently uses:

Ollama
   │
   ▼
Gemma 3 4B

The LLM receives:

User Question
      +
Retrieved Context
      │
      ▼
    Gemma
      │
      ▼
Final Answer

The local RAG prompt instructs the model to answer using the retrieved context and include citation numbers.

Query Routing

RAGForge currently supports three query routes.

                       User Query
                           │
                           ▼
                    ┌─────────────┐
                    │Query Router │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
       LOCAL             WEB            GENERAL
          │                │                │
          ▼                ▼                ▼
   Hybrid Retrieval     Gemini          Ollama
          │           Google Search      Gemma
          ▼
      Reranker
          │
          ▼
       Ollama
       Gemma
Local Route

Used when relevant information can be found in the indexed documents.

Query
  ↓
FAISS + BM25
  ↓
RRF
  ↓
Cross-Encoder Reranker
  ↓
Ollama + Gemma
  ↓
Answer + Document Citations
Web Route

Used for questions that require current or time-sensitive information.

Query
  ↓
Gemini
  ↓
Google Search Grounding
  ↓
Answer + Web Sources
General Route

Used when the question does not require the local documents or web search.

Query
  ↓
Ollama + Gemma
  ↓
General Answer
Source Citations

Local document answers include source information such as:

[1] Introduction to Machine Learning with Python.pdf · p.42
[2] AI & ML DIGITAL NOTES.pdf · p.114

The backend exposes citations through the FastAPI response.

Web results can also include web source information returned by Gemini's grounding metadata.

Project Structure

RAGForge/
│
├── data/                       # Source PDF documents
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── api/                # Backend API communication
│   │   ├── components/         # UI components
│   │   ├── context/            # Application context
│   │   ├── hooks/              # Custom React hooks
│   │   └── styles/             # Frontend styling
│   ├── package.json
│   └── vite.config.js
│
├── prompts/                    # Prompt-related files
│
├── tests/                      # Automated tests
│   ├── test_loader.py
│   ├── test_splitter.py
│   ├── test_vectorstore.py
│   ├── test_router.py
│   ├── test_ollama_llm.py
│   ├── test_bm25.py
│   ├── test_hybrid.py
│   └── test_reranker.py
│
├── utils/                      # Core RAG components
│   ├── embeddings.py           # Embedding model
│   ├── loader.py               # PDF loading
│   ├── splitter.py             # Text chunking
│   ├── vectorstore.py          # FAISS vector store
│   ├── retriever.py            # Semantic retrieval
│   ├── bm25_retriever.py       # BM25 retrieval
│   ├── hybrid_retriever.py     # Hybrid retrieval + RRF
│   ├── reranker.py             # Cross-encoder reranking
│   ├── router.py               # Query routing
│   ├── ollama_llm.py           # Ollama/Gemma inference
│   └── web_search.py           # Gemini web search
│
├── vectorstore/                # Persisted FAISS index
│
├── uploads/                    # Uploaded documents
│
├── app.py                      # FastAPI application
├── config.py                   # Configuration
├── ingest.py                   # Document ingestion pipeline
├── main.py                     # CLI application
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git exclusions
└── README.md                   # Project documentation

Tech Stack

Backend
Python
FastAPI
Uvicorn
Retrieval
FAISS
BM25
Reciprocal Rank Fusion (RRF)
Sentence Transformers
Cross-Encoder
LLM
Ollama
Gemma 3 4B
Web Search
Google Gemini API
Gemini Google Search grounding
Frontend
React
Vite
Tailwind CSS
React Markdown
Lucide React
Document Processing
PyPDF
Testing
Python test modules
Component-level retrieval and model tests

Installation
1. Clone the repository
git clone https://github.com/MOTOREX123/RAGForge.git
cd RAGForge
2. Create a virtual environment
python -m venv venv

Activate it on Windows:

.\venv\Scripts\Activate.ps1
3. Install Python dependencies
pip install -r requirements.txt
4. Install Ollama

Install Ollama separately and make sure it is running.

Pull the Gemma model:

ollama pull gemma3:4b

RAGForge currently uses:

gemma3:4b
5. Configure environment variables

Create a .env file in the project root.

Example:

GEMINI_API_KEY=your_gemini_api_key

Never commit your .env file or API keys to GitHub.

Running RAGForge

RAGForge uses three main processes during development:

┌─────────────────────┐
│ Ollama              │
│ localhost:11434     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ FastAPI Backend     │
│ localhost:8000      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ React Frontend      │
│ localhost:5173      │
└─────────────────────┘
Terminal 1 — Ollama
ollama serve

If Ollama is already running, you do not need to start another server.

Terminal 2 — FastAPI

From the project root:

.\venv\Scripts\Activate.ps1
uvicorn app:app --reload --port 8000

The API will be available at:

http://localhost:8000

FastAPI documentation:

http://localhost:8000/docs
Terminal 3 — React frontend
cd frontend
npm install
npm run dev

The frontend will be available at:

http://localhost:5173
Health Check

RAGForge exposes a health endpoint:

GET /api/health

Example:

http://localhost:8000/api/health

The endpoint checks important backend components such as:

Vector store availability
Number of indexed chunks
Ollama availability
Chat API

RAGForge exposes the main chat endpoint:

POST /api/chat

Example request:

{
  "message": "What is overfitting?"
}

Example response structure:

{
  "answer": "...",
  "route": "local",
  "provider": "ollama",
  "model": "gemma3:4b",
  "citations": []
}

The actual citation list depends on the retrieved documents.

Document Ingestion

When adding or changing source PDFs, run the ingestion pipeline:

python ingest.py

This rebuilds the persistent vector store.

You normally do not need to run ingest.py every time you start the application.

Run it when:

New documents are added
Existing documents are changed
The vector index needs to be rebuilt
Current Document Collection

The current development dataset contains multiple machine-learning and AI-related PDF documents.

The indexed collection currently contains approximately:

Documents: 4
Pages:     775
Chunks:    1915

The FAISS embedding dimension is:

384
Example Queries
Local document query
What is overfitting in machine learning?

Expected route:

LOCAL

Pipeline:

FAISS + BM25
      ↓
RRF
      ↓
Cross-Encoder
      ↓
Gemma
      ↓
Citations
General question
What is Python?

If the router determines that the local documents are not sufficiently relevant and the query does not require web information, it can use the general route.

GENERAL
   ↓
Ollama + Gemma
Web query

Example:

What are the latest developments in AI?

Expected route:

WEB

Pipeline:

Gemini
   ↓
Google Search Grounding
   ↓
Current Web Information
Testing

Individual components can be tested separately.

Examples:

python tests/test_loader.py
python tests/test_splitter.py
python tests/test_vectorstore.py
python tests/test_router.py
python tests/test_ollama_llm.py
python tests/test_bm25.py
python tests/test_hybrid.py
python tests/test_reranker.py

These tests help verify individual components before integrating them into the complete application.

Design Goals

RAGForge was built with several goals:

Understand how RAG systems work internally
Separate retrieval from generation
Combine semantic and lexical retrieval
Improve retrieval quality through reranking
Keep local LLM inference possible
Support current web information through Gemini
Provide traceable document citations
Maintain a modular architecture
Make individual components testable
Limitations

The current implementation has several areas that can be improved.

Retrieval

The current system uses a fixed chunking strategy and retrieval parameters.

Possible improvements include:

Better semantic chunking
Metadata-aware retrieval
Query transformation
Query expansion
Retrieval evaluation
More advanced reranking strategies
Conversation Memory

Conversation-aware retrieval and long-term conversational context are not yet implemented.

Document Management

A more complete document management system could support:

Uploading documents through the UI
Removing documents
Re-indexing individual documents
Document metadata
Index versioning
Evaluation

A formal RAG evaluation pipeline can be added to measure:

Retrieval precision
Retrieval recall
Context relevance
Answer faithfulness
Answer correctness
Deployment

The current system is primarily designed for local development.

Future deployment work could include:

Docker
Production configuration
Cloud deployment
Authentication
Logging
Monitoring
Future Roadmap

Planned improvements include:

 Better document chunking
 FAISS semantic retrieval
 BM25 keyword retrieval
 Hybrid retrieval
 Reciprocal Rank Fusion
 Cross-encoder reranking
 Query routing
 Local Ollama inference
 Gemini web search
 FastAPI backend
 React frontend
 Source citations
 Query transformation
 Conversation-aware retrieval
 Document upload and management
 RAG evaluation framework
 Observability and logging
 Dockerization
 Production deployment
Learning Focus

RAGForge is also a learning project.

The architecture demonstrates several important concepts in modern AI systems:

Document Processing
        ↓
Chunking
        ↓
Embeddings
        ↓
Vector Search
        ↓
Keyword Search
        ↓
Hybrid Retrieval
        ↓
Rank Fusion
        ↓
Reranking
        ↓
Context Construction
        ↓
LLM Generation
        ↓
Citations

The project is intentionally modular so that each stage can be studied, tested, and improved independently.

License

This project is currently intended as a personal learning and portfolio project.


### One important thing before you save

I deliberately **didn't put your Gemini API key, `.env` contents, PDFs, FAISS files, or `venv` contents into the README**.

Your `.gitignore` already protects those local/generated files.

After replacing the entire README:

1. Press **Ctrl + S**
2. Run:

```powershell
git status