# FastAPI Task Service

A minimal task management API built with FastAPI, SQLite, and an optional Redis-backed rate limiter. Provides CRUD endpoints for tasks with pagination and simple status filtering.

## Features
- Create, read, update, delete tasks
- SQLite persistence (default: `tasks.db`)
- Optional Redis rate limiting (per-IP)
- Async SQLModel + SQLAlchemy usage

## Project Structure

- `app/` — application code
  - `main.py` — FastAPI app entrypoint
  - `database.py` — async DB setup (SQLite by default)
  - `models.py` — `Task` SQLModel model
  - `schemas.py` — Pydantic request/response schemas
  - `crud.py` — async CRUD helpers
  - `rate_limiter.py` — Redis-based rate limiter utility
  - `logger.py` — logging configuration
  - `routers/tasks.py` — API routes for tasks
- `requirements.txt` — Python dependencies
- `.env` — optional environment variables

## Requirements

- Python 3.10+
- Redis (optional, for rate limiter)

Install Python dependencies:

```bash
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
.venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
```

## Configuration

Create an optional `.env` file at the project root to override defaults. Recognized values (examples):

- `DATABASE_URL` — SQLAlchemy database URL (default: `sqlite+aiosqlite:///./tasks.db`)

If not provided, the app will use an on-disk SQLite DB file `tasks.db` in the project root. The rate limiter uses Redis if configured in code or environment.

## Run Locally

Start the development server with Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints & Examples

Common endpoints (see `app/routers/tasks.py`):

- `GET /` — health check
- `POST /tasks` — create a task
- `GET /tasks` — list tasks (`?page=1&limit=10&status=pending`)
- `GET /tasks/{task_id}` — get a single task
- `PUT /tasks/{task_id}` — update a task
- `DELETE /tasks/{task_id}` — delete a task

Example: create a task

```bash
curl -sS -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Write README", "description": "Create project README.md"}'
```

Example: list tasks (first page)

```bash
curl "http://127.0.0.1:8000/tasks?page=1&limit=10"
```

Example: get task by id

```bash
curl http://127.0.0.1:8000/tasks/1
```

Adjust the JSON payloads to match the schemas in `app/schemas.py` (fields: `title`, `description`, optional `status`).

## Rate Limiting

The project includes a Redis-backed rate limiter in `app/rate_limiter.py`. By default it enforces a small request limit per IP. If you plan to use rate limiting, ensure a Redis instance is available and configured according to your environment.


## Notes & Troubleshooting

- The SQLite DB file `tasks.db` will be created automatically on first run if not provided via `DATABASE_URL`.
- If you see rate-limit `429` responses, either increase limits in `app/rate_limiter.py` or disable Redis/rate limiting in your environment.
- If you plan to deploy to production, replace SQLite with a proper DB (Postgres), configure environment variables, and run behind a production ASGI server.

## Next steps I can do for you

 - Add example `curl` requests for every endpoint including request/response bodies
 - Run the app locally and verify the example requests

---
If you want, I can run a quick local verification of the app now.
