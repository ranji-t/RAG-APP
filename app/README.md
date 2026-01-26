To run locally in the app dir with reload
`uv run uvicorn src.app:app --host "localhost" --port 8088 --reload --debug`

To run locally in the app dir without reload
`uv run uvicorn src.app:app --host "localhost" --port 8088`

To run locally in docker
`uv run uvicorn src.app:app --host "0.0.0.0" --port 8088`
