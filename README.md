# RAG Application

This repository contains a full-stack Retrieval-Augmented Generation (RAG) application. It features a robust Python backend using FastAPI and LangChain, a containerized vector database (Qdrant), and an embedding service (Ollama). The frontend is built with Flutter (currently a skeleton application).

## 🚀 Features

### Backend (`/app`)
- **FastAPI**: High-performance, asynchronous API framework.
- **RAG Pipeline**: Built with **LangChain**, integrating retrieval and generation.
- **Vector Database**: Uses **Qdrant** for storing and querying vector embeddings.
- **Embeddings**: Utilizes **Ollama** (running `nomic-embed-text`) for local embedding generation.
- **LLM Integration**: Configured to use **OpenAI's GPT-4o** for generation.
- **Dependency Management**: Uses `uv` for ultra-fast Python package management.

### Infrastructure
- **Dockerized Services**:
  - **Qdrant**: Vector database running on ports `6333` (HTTP) and `6334` (GRPC).
  - **Ollama**: Embedding service running on port `11435`.
  - **App**: The FastAPI backend running on port `8088`.

### Frontend (`/ui`)
- **Flutter**: Cross-platform framework for building native interfaces.
- *Note: The UI is currently a starting skeleton and is ready for development.*

## 🛠️ Prerequisites

Ensure you have the following installed:
- **Docker & Docker Compose**: To run the backend services.
- **Python 3.13+**: For local backend development.
- **Flutter SDK**: For frontend development.
- **Just** (Optional): For running command shortcuts (if applicable).

## 🏁 Getting Started

### 1. Backend Setup (Docker)

The easiest way to run the backend services (API, Database, Embedder) is via Docker Compose.

1.  **Configure Environment Variables**:
    Create a `.env` file in `app/` (or use `app/.env/.env`) based on the example in `app/README.md`.
    ```env
    # Example .env configuration
    OLLAMA_URL=http://embedder:11434
    QDRANT_URL=http://vector_db:6333
    OPENAI_API_KEY=your_openai_api_key_here
    ```

2.  **Start Services**:
    Run the following command from the root directory:
    ```bash
    docker compose up --build
    ```
    This will start:
    -   **Ollama/Embedder**: Available at `http://localhost:11435`
    -   **Qdrant**: Available at `http://localhost:6333`
    -   **FastAPI Backend**: Available at `http://localhost:8088`

3.  **Verify Backend**:
    Open your browser and navigate to `http://localhost:8088/docs` to see the interactive API documentation.

### 2. Frontend Setup (Flutter)

To run the mobile/web application:

1.  Navigate to the UI directory:
    ```bash
    cd ui
    ```

2.  Install dependencies:
    ```bash
    flutter pub get
    ```

3.  Run the application:
    ```bash
    flutter run
    ```
    *Select your target device (Chrome, Android Emulator, iOS Simulator) when prompted.*

## 📂 Project Structure

```
├── app/                # FastAPI Backend & RAG Logic
│   ├── src/            # Source code (API, Core, Services)
│   ├── Dockerfile      # Backend container definition
│   └── README.md       # Detailed backend documentation
├── db/                 # Database data (volume mount for Qdrant)
├── embedder/           # Embedder data (volume mount for Ollama)
├── ui/                 # Flutter Frontend application
├── compose.yaml        # Docker Compose configuration
└── README.md           # This file
```

## 📚 Documentation

-   **Backend Details**: See [app/README.md](./app/README.md) for detailed API endpoints and development instructions.
-   **Docker Help**: See [app/README.Docker.md](./app/README.Docker.md) for specific Docker-related guides.
