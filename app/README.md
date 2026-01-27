# RAG Application Backend

This repository contains the backend for a Retrieval-Augmented Generation (RAG) application. It is built using **FastAPI** and integrates with **Qdrant** for vector storage, **Ollama** for embeddings, and **OpenAI's GPT-4o** for the Large Language Model (LLM).

## Features

-   **FastAPI Backend**: High-performance, async API.
-   **RAG Pipeline**: Implemented using **LangChain**.
-   **Vector Database**: **Qdrant** integration for efficient similarity search.
-   **Embeddings**: Uses **Ollama** for local or remote embedding generation.
-   **LLM**: Integrated with **OpenAI GPT-4o** for answering queries.
-   **Document Management**: APIs to add, list, and query documents.
-   **Collection Management**: Create, list, and delete Qdrant collections.
-   **Dependency Management**: Uses `uv` for fast Python package management.
-   **Docker Support**: Ready for containerized deployment.

## Tech Stack

-   **Language**: Python >= 3.13
-   **Web Framework**: FastAPI, Uvicorn
-   **RAG Framework**: LangChain
-   **Vector Store**: Qdrant
-   **Embeddings**: Ollama
-   **AI Model**: OpenAI GPT-4o

## Prerequisites

Before running the application, ensure you have the following installed:

1.  **Python** (>= 3.13)
2.  **uv** (Python package manager)
3.  **Qdrant** instance (running locally or remotely)
4.  **Ollama** instance (running locally or remotely)
5.  **OpenAI API Key**

## Environment Variables

Create a `.env` file (or use `.env/.env.local`) with the following variables:

```env
OLLAMA_URL=http://localhost:11434  # URL of your Ollama instance
QDRANT_URL=http://localhost:6333   # URL of your Qdrant instance
OPENAI_API_KEY=sk-...              # Your OpenAI API Key
```

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd RAG_App/app
    ```

2.  Install dependencies using `uv`:
    ```bash
    uv sync
    ```

## Running the Application

### Locally

To run the backend locally with hot-reloading (for development):

```bash
uv run uvicorn main:app --host "localhost" --port 8000 --env-file .env/.env.local --app-dir ./src/ --reload
```

To run locally without reload:

```bash
uv run uvicorn main:app --host "localhost" --port 8000 --env-file .env/.env.local --app-dir ./src/
```

### With Docker

To run the application using Docker:

```bash
uv run uvicorn main:app --host "localhost" --port 8000 --app-dir ./src/
```

*(Note: Ensure your Docker container is configured to access the necessary services like Qdrant and Ollama).*

## API Endpoints

The API is structured into several routers under `v1`:

### System
-   `GET /`: Health check or welcome message (if implemented).

### Collections (`/collections`)
-   `GET /collections`: List all Qdrant collections.
-   `POST /collections`: Create a new collection.
-   `DELETE /collections`: Delete a collection.

### Documents (`/documents`)
-   `POST /documents/add`: Add text content to the vector store (chunks and embeds automatically).
-   `POST /documents/query`: Perform a similarity search on stored documents.

### Embeddings (`/embed`)
-   `GET /embed`: Embed a single query string.
-   `POST /embed`: Embed multiple text strings.

### RAG (`/rag`)
-   `POST /rag/ask`: Ask a question. Retrieves relevant context from the vector store and uses GPT-4o to generate an answer.

## Project Structure

```
├── .env                # Environment variables
├── data/               # Data storage (if applicable)
├── notebooks/          # Jupyter notebooks for experimentation
├── src/
│   ├── app/
│   │   ├── api/        # API route handlers
│   │   ├── core/       # App configuration and lifecycle
│   │   ├── services/   # Business logic (RAG, Collections, etc.)
│   │   └── utils/      # Utility functions
│   └── main.py         # Application entry point
├── pyproject.toml      # Project dependencies (uv)
└── README.md           # Project documentation
```
