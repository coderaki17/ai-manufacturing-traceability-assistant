# AI Manufacturing Traceability Assistant

A Python-based manufacturing traceability API that retrieves pipe production details and quality inspection history from PostgreSQL.

## Features

- Retrieve all pipe records.
- Retrieve individual pipes by pipe ID.
- Track quality inspection history.
- Add inspections through a REST API.
- Validate inspection results using Pydantic.
- Store production and inspection data in PostgreSQL.
- Run automated API tests with pytest.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- Pydantic
- pytest

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| GET | `/pipes` | List all pipes |
| GET | `/pipes/{pipe_id}` | Retrieve pipe details and inspections |
| POST | `/pipes/{pipe_id}/inspections` | Add an inspection |

Interactive API documentation is available at `/docs` while the application is running.

## Run Locally

1. Create and activate a Python virtual environment.
2. Install the project dependencies.
3. Start PostgreSQL using Docker.
4. Configure `DATABASE_URL` in a local `.env` file.
5. Initialize and seed the database.
6. Start the API with Uvicorn.

Keep `.env` and all credentials out of version control.

## Run Tests

```bash
python -m pytest -v
```

## Project Status

The initial database-backed API and automated tests are implemented. Future improvements include stronger database constraints, expanded test coverage, and AI-assisted manufacturing insights.
