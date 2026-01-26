ARG PYTHON_VERSION=3.13.1
FROM python:${PYTHON_VERSION}-slim AS base

# IO, Python and UV settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1

WORKDIR /app

# Security Move to non-privileged user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install UV
COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

# Install Dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=.python-version,target=.python-version \
    uv sync --locked --no-dev --no-install-project

# Copy the source code into the container.
COPY . .
RUN uv sync --locked --no-dev

# Switch to the non-privileged user to run the application.
USER appuser
ENV PATH="/app/.venv/bin:$PATH"

# Expose the port that the application listens on.
EXPOSE 8088

# Run the application.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8088", "--workers", "2", "--app-dir", "./src/"]
