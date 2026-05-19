# FastAPI Task Service

A FastAPI-based CRUD API for a Task Management System. It supports task creation, listing with pagination and status filtering, retrieving by ID, updating, deleting, async SQLite persistence, and Redis-backed IP rate limiting on GET APIs.

## Features

- Create, update, retrieve, and delete tasks
- Task status validation: `pending`, `in_progress`, `completed`
- `created_at` timestamp stored for each task
- Paginated task listing with optional status filter
- Total matching task count returned by `GET /tasks`
- Async SQLModel/SQLAlchemy database access
- SQLite persistence by default
- Logging for startup, task actions, not-found cases, and rate-limit events
- Swagger UI at `http://127.0.0.1:8000/docs`

## Project Structure

- `app/main.py` - FastAPI app entrypoint
- `app/database.py` - async database setup
- `app/models.py` - SQLModel task table
- `app/schemas.py` - Pydantic request and response schemas
- `app/crud.py` - async CRUD helpers
- `app/rate_limiter.py` - Rate limiter
- `app/logger.py` - logging configuration
- `app/routers/tasks.py` - task API routes
- `requirements.txt` - Python dependencies

## Requirements

- Python 3.10+
- Redis running locally or reachable through environment configuration

Install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

For macOS/Linux activation:

```bash
source .venv/bin/activate
```

## Configuration

Create a `.env` file in the project root if you want to override defaults:

```env
DATABASE_URL=sqlite+aiosqlite:///./tasks.db
RATE_LIMIT_REQUESTS=5
RATE_LIMIT_WINDOW_SECONDS=60
```

Defaults are used when these values are not provided.

## Run Locally

Then run the FastAPI app:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

- `GET /` - health check
- `POST /tasks` - create a task
- `GET /tasks?page=1&limit=10&status=pending` - list tasks
- `GET /tasks/{task_id}` - retrieve a task by ID
- `PUT /tasks/{task_id}` - update a task
- `DELETE /tasks/{task_id}` - delete a task

Rate limiting applies only to:

- `GET /tasks`
- `GET /tasks/{task_id}`

Maximum allowed GET requests: 5 per minute per client IP. When exceeded:

```json
{
  "detail": "Rate limit exceeded. Try again later."
}
```

## Example Requests

Create a task:

```bash
curl -X POST http://127.0.0.1:8000/tasks ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Write README\",\"description\":\"Create project README\",\"status\":\"pending\"}"
```

List tasks:

```bash
curl "http://127.0.0.1:8000/tasks?page=1&limit=10"
```

Filter by status:

```bash
curl "http://127.0.0.1:8000/tasks?page=1&limit=10&status=pending"
```

Get task by ID:

```bash
curl http://127.0.0.1:8000/tasks/1
```

Update task:

```bash
curl -X PUT http://127.0.0.1:8000/tasks/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"status\":\"completed\"}"
```

Delete task:

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

## Verification Checklist

- `/docs` loads successfully.
- Creating a task with a valid status returns `201`.
- Invalid status returns a validation error.
- `GET /tasks` supports `page`, `limit`, and optional `status`.
- `GET /tasks` returns the full matching `total`, not just the current page size.
- Missing task IDs return `404`.
- The 6th GET request within one minute from the same client returns `429`.
- `POST`, `PUT`, and `DELETE` are not rate limited.
