# Shorten

FastAPI URL shortener service backed by SQLite.

## Requirements

- Python `>=3.14,<3.15`
- Poetry

## Run (development)

The ASGI app is `main:main_app` located in `app/src/main.py`.

```bash
poetry run python src/main.py
```

API docs:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

## API

Base path:

- `/api/v1`

Endpoints:

- `POST /api/v1/links/shorten`
  - Body: `{ "source_url": "https://example.com" }`
  - Returns `201` for a new short code, or `200` if the URL was already shortened.
- `GET /api/v1/links/{code}`
  - Redirects (`301`) to the original `source_url`.

Example:

```bash
curl -X POST "http://localhost:8000/api/v1/links/shorten" \
  -H "Content-Type: application/json" \
  -d '{"source_url":"https://example.com"}'
```

## Database

The service uses SQLite via `aiosqlite`.

- On startup the app creates a `link` table if it does not exist.
- Default DB file name is `database.db` located under `app/`.

## Configuration

Settings are loaded via `pydantic-settings`.

- Environment variable prefix: `APP_CONFIG__`
- Nested delimiter: `__`

Example (change DB file name):

```bash
export APP_CONFIG__DB__NAME="my_database.db"
```

Note: the code references an env file at `app/envs/dev/app.env`. If you want to use it, create that file and put variables there.

## Tests

```bash
poetry  run pytest
```
