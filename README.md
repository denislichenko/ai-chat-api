# AI Chat API with RAG

A production-style backend project for an AI Software Engineer portfolio.

This service provides a Retrieval-Augmented Generation (RAG) chat API built with FastAPI, PostgreSQL, Qdrant, sentence-transformers embeddings, and OpenRouter LLM inference. It supports document ingestion, semantic retrieval, and multi-turn conversations persisted in a relational database.

## Why this project

This project demonstrates practical backend AI engineering:

- End-to-end RAG pipeline implementation
- LLM integration via external API provider (OpenRouter)
- Vector search with Qdrant
- Conversation state persistence with SQLAlchemy + PostgreSQL
- Containerized deployment with Docker Compose

## Core Features

- Document ingestion endpoint (`/upload`) for indexing text into Qdrant
- Chat endpoint (`/chat`) with retrieval-grounded responses
- Conversation and message storage in PostgreSQL
- Service-oriented architecture (clear boundaries for LLM, embeddings, vector DB, ingestion, and chat orchestration)
- Configurable model and generation parameters via environment variables

## Architecture

1. User uploads text document.
2. Text is chunked (`chunk_size=500`, `overlap=100`).
3. Each chunk is embedded with `all-MiniLM-L6-v2`.
4. Embeddings + payload are stored in Qdrant.
5. User sends a chat message.
6. Query embedding is generated and top-k similar chunks are retrieved from Qdrant.
7. Retrieved context + conversation history are sent to the LLM.
8. Assistant response and usage metadata are returned and stored.

## Tech Stack

- **Backend:** FastAPI
- **LLM Gateway:** OpenRouter API
- **Embeddings:** sentence-transformers (`all-MiniLM-L6-v2`)
- **Vector Store:** Qdrant
- **Relational DB:** PostgreSQL
- **ORM:** SQLAlchemy
- **Containerization:** Docker + Docker Compose

## Project Structure

```text
.
├── main.py
├── core/
│   ├── config.py
│   └── dependecies.py
├── db/
│   ├── models.py
│   └── session.py
├── repositories/
│   └── conversation_repository.py
├── services/
│   ├── chat_service.py
│   ├── chunking.py
│   ├── document_ingestion_service.py
│   ├── embedding_service.py
│   ├── llm_service.py
│   └── qdrant_service.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- OpenRouter API key

### 1) Configure environment

Create/update `.env`:

```env
# For docker-compose runtime inside containers:
DATABASE_URL=postgresql://denys:mysecretpassword@postgres:5432/ai_chat

OPENROUTER_API_KEY=your_openrouter_api_key
MODEL_NAME=stepfun/step-3.5-flash:free
TEMPERATURE=0.7
```

### 2) Start services

```bash
docker compose up --build
```

API will be available at:

- `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`

## API Usage

### Upload a document

```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_document.txt"
```

Example response:

```json
{
  "status": "indexed"
}
```

### Chat with RAG context

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "portfolio-user",
    "message": "Summarize the uploaded document in 3 bullet points",
    "conversation_id": null
  }'
```

Example response:

```json
{
  "answer": "...",
  "tokens_used": {
    "prompt_tokens": 123,
    "completion_tokens": 45,
    "total_tokens": 168
  }
}
```

## Environment Variables

- `DATABASE_URL`: SQLAlchemy/PostgreSQL connection string
- `OPENROUTER_API_KEY`: API key for OpenRouter
- `MODEL_NAME`: LLM identifier (default: `stepfun/step-3.5-flash:free`)
- `TEMPERATURE`: Sampling temperature for generation

## License

MIT
