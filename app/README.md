To run locally in the backend dir with reload
`uv run uvicorn app:app --host "localhost" --port 8000 --env-file .env/.env.local --app-dir ./src/ --reload`

To run locally in the backend dir without reload
`uv run uvicorn app:app --host "localhost" --port 8000 --env-file .env/.env.local --app-dir ./src/`

To run locally in docker
`uv run uvicorn app:app --host "localhost" --port 8000 --app-dir ./src/`
