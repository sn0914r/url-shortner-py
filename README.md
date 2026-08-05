# URL Shortener API

A URL shortener built with FastAPI and PostgreSQL that generates short links, redirects users to the original URLs, tracks click analytics, and supports URL expiration through a clean REST API.

---

## Highlights

- Asynchronous REST APIs with FastAPI
- Async database operations using SQLAlchemy and asyncpg
- URL expiration support
- Click analytics with IP, User-Agent, and timestamp tracking
- PostgreSQL with Alembic migrations
- Docker-based development environment

---

## Request Flow

### Link Creation

1. The client sends a request containing a long URL and an optional expiration date.
2. The server generates a unique short code.
3. The URL metadata is stored in PostgreSQL.
4. The created short URL is returned to the client.

### Redirection & Analytics

1. A user visits the shortened URL.
2. The service looks up the corresponding long URL.
3. If the URL exists and has not expired, a click record containing the client's IP address, User-Agent, and timestamp is stored.
4. The user is redirected to the original URL.
5. If the URL is missing or expired, the service returns the appropriate HTTP status (404 or 410).

### Statistics

1. The client requests statistics for a short URL.
2. The service retrieves the associated click records.
3. Summary statistics and recent click history are returned.

---

## Core Features

### URL Management

- Generate unique short URLs.
- Optional expiration support for shortened links.
- Automatic redirection to the original destination.

### Analytics

- Track every visit to a shortened URL.
- Record IP address, User-Agent, and click timestamp.
- Retrieve click statistics and recent activity.

### Infrastructure

- Asynchronous APIs built with FastAPI.
- Async database access using SQLAlchemy and asyncpg.
- Database schema versioning with Alembic.
- Docker Compose support for local development.

---

## Tech Stack

| Category         | Technology             |
| ---------------- | ---------------------- |
| Runtime          | Python 3.11            |
| Framework        | FastAPI                |
| Server           | Uvicorn                |
| Database         | PostgreSQL             |
| ORM              | SQLAlchemy (Async)     |
| Migrations       | Alembic                |
| Validation       | Pydantic               |
| Containerization | Docker, Docker Compose |

---

## Folder Structure

```text
.
├── app/
│   ├── api/
│   │   ├── models.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   ├── services.py
│   │   └── utils.py
│   ├── core/
│   │   ├── configs.py
│   │   └── database.py
│   └── main.py
├── migrations/
├── .env.example
├── alembic.ini
├── compose.dev.yml
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Environment Variables

```env
PORT=8000
DATABASE_URL=
```

---

## Run with Docker

Start the application and PostgreSQL using Docker Compose:

```bash
docker compose -f compose.dev.yml up --build
```

The API will be available at:

- http://localhost:8000
- ReDoc: http://localhost:8000/redoc

---

## Local Setup

1. **Clone the repository**

```bash
git clone https://github.com/sn0914r/url-shortner-py.git
cd url-shortener
```

2. **Create a virtual environment and install dependencies**

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

3. **Configure environment variables**

Copy `.env.example` to `.env` and configure your PostgreSQL connection.

4. **Apply database migrations**

```bash
alembic upgrade head
```

5. **Start the development server**

```bash
uvicorn app.main:app --reload
```

---

## API Endpoints

### Health & Documentation

| Method | Endpoint | Description             |
| ------ | -------- | ----------------------- |
| GET    | /health  | Service health check    |
| GET    | /redoc   | ReDoc API documentation |

### URL Management

| Method | Endpoint                 | Description                  |
| ------ | ------------------------ | ---------------------------- |
| POST   | /link/                   | Create a short URL           |
| GET    | /link/{short_code}       | Redirect to the original URL |
| GET    | /link/{short_code}/stats | Retrieve click statistics    |

---

## Security

- Request validation using Pydantic.
- Expiration checks prevent access to expired URLs.
- Parameterized database operations using SQLAlchemy ORM.
- Centralized error handling with appropriate HTTP status codes.
