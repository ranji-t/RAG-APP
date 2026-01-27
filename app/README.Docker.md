# Docker Instructions

This guide provides instructions on how to build and run the RAG App backend using Docker.

## Prerequisites

-   [Docker](https://docs.docker.com/get-docker/) installed on your machine.
-   Access to **Qdrant** and **Ollama** instances (running locally or remotely).

## Building the Image

To build the Docker image, run the following command from the root of the `app` directory:

```bash
docker build -t rag-backend .
```

## Running the Container

The application runs on port **8088** inside the container (defined in `Dockerfile`). You need to map this port to your host machine.

### 1. Basic Run

If you have a `.env` file with your configuration, you can pass it to the container using the `--env-file` flag.

```bash
docker run -p 8088:8088 --env-file .env rag-backend
```

### 2. Passing Environment Variables Manually

You can also pass environment variables directly using the `-e` flag:

```bash
docker run -p 8088:8088 \
  -e OLLAMA_URL=http://host.docker.internal:11434 \
  -e QDRANT_URL=http://host.docker.internal:6333 \
  -e OPENAI_API_KEY=sk-... \
  rag-backend
```

### Important: Connectivity to Local Services

If your **Qdrant** and **Ollama** instances are running on your **host machine** (localhost), the Docker container cannot access them using `localhost`.

-   **Mac/Windows**: Use `host.docker.internal` instead of `localhost` in your environment variables (as shown in the example above).
-   **Linux**: Add `--add-host=host.docker.internal:host-gateway` to your `docker run` command to enable access to the host localhost.

Example for Linux:
```bash
docker run -p 8088:8088 \
  --add-host=host.docker.internal:host-gateway \
  --env-file .env \
  rag-backend
```

## Verifying Deployment

Once running, the API documentation will be available at:
[http://localhost:8088/docs](http://localhost:8088/docs)

## Development vs Production

The provided `Dockerfile` is optimized for production:
-   It uses a **multi-stage build** to keep the image size small.
-   It runs as a **non-root user** (`appuser`) for security.
-   It uses `uv` for fast dependency installation.

For local development where you need **hot-reloading**, it is recommended to use the local setup described in the main [README.md](./README.md) instead of Docker.