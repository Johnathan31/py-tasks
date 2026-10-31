# 🚀 FastAPI + PostgreSQL

A **Python** task manager API (CRUD API) built with FastAPI, PostgreSQL, and Docker compose.
It demonstrates building an isolated backend server with persistent database (PostgreSQL)

---

## 📚 Tech Stack

| Name           | Description                        |
| -------------- | ---------------------------------- |
| FastAPI        | A REST API server                  |
| Pydantic       | Data Structures and models         |
| Enums          | Making key-value pairs collections |
| PostgreSQL     | Persistent Database Storage        |
| Dotenv         | Accessing Environment variables    |
| psycopg3       | PostgreSQL Python Driver           |
| psycopg_pool   | _psycopg3_ Pooling driver          |
| logging        | Logging error tracebacks           |
| Docker compose | Isolating the project environment  |

---

## New in Version 3.0.0

- Implemented Docker support.
- Added tests.
- tasks priority and done fields are optional in `POST /v3/tasks/`.

for more, see [Change Log](./CHANGELOG.md)

## ⚙️ Features

- A **RESTful API** using FastAPI, controlling:
  - Task creation.
  - Task Reading.
  - Task updating.
  - Task deletion (for details, see [API docs](./api.md))

- 🛠️ _CRUD Operations_ Endpoints.

- Consistent Task structure:

| property | Type                         | Description                              |
| -------- | ---------------------------- | ---------------------------------------- |
| title    | `str`                        | Task title                               |
| priority | [`Priority`](#Priority-Enum) | Task priority                            |
| done     | `bool`                       | indicate whether the task is done or not |

- 🖇️ Connection Pooling.

- 💾 _PostgreSQL_ Persistent database storage.

- 💪 Strong **Validation**.

- 🧾 **Static Type Checking**.

- Strict **Request Body Structure** using Pydantic Models (_BaseModel_).

- ⚪ A _clean, organized, and understandable_ project structure, thus facilitating future improvements.

- **Data filtering** in GET Requests.

- A fully containerized environment

- Test coverage with __60 pytest tests__.
---

# 🪾 Project Tree

```text
py-tasks
├── app # application source code
│   ├── database # database configs
│   │   ├── __init__.py
│   │   ├── connection.py # PostgreSQL Connection pool
│   │   └── dependencies.py # dependency injection
│   ├── internal # shared components and internal utilities
│   │   ├── __init__.py
│   │   ├── env.py # manage environment variables
│   │   ├── log.py # configurate logging
│   │   ├── models.py # Pydantic models and schemas
│   │   └── types.py # types shortcuts
│   ├── routes # FastAPI Endpoints
│   │   ├── __init__.py
│   │   ├── create.py # Create operation
│   │   ├── delete.py # Delete operations
│   │   ├── read.py   # Read operations
│   │   ├── router.py # APIRouter manager
│   │   └── update.py # Update operations
│   ├── tests # Test coverage
│   │   ├── __init__.py
│   │   ├── conftest.py    # pytest configuration
│   │   ├── test_create.py # create operations tests
│   │   ├── test_delete.py # delete operations tests
│   │   ├── test_read.py   # read operations tests
│   │   └── test_update.py # update operations tests
│   ├── __init__.py
│   ├── exceptions.py # exceptions handler
│   ├── main.py # main FastAPI file
│   └── schema.sql # main SQL Schema
├── .dockerignore
├── .env.example # sample .env file
├── .gitignore
├── CHANGELOG.md
├── Dockerfile # Docker image builder
├── README.md
├── __init__.py
├── api.md # API docs
├── compose.yaml # Docker compose config
├── requirements.txt # python packages requirements
└── start.sh # a Shell script to serve the API
```

---

## 🌀 Prerequisites

### Packages, Modules

- Python _v3.13_
- FastAPI _v0.138_
- Rustc (Optional)

### Skills

- Minimal Backend development understanding.
- Solid Python knowledge.
- Understanding Environment variables

---

## ⚡ Getting Started

1. Clone the repository and go to it:

```Bash
git clone https://github.com/<your-username>/py-tasks.git
cd py-tasks
```

2. Create a `.env` file:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=my_password
POSTGRES_DB=tasks
DB_URL=postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}
DEBUG=true
```

For more details, see [.env sample file](./.env.example)

3. Run startup SQL queries:
```Bash
psql -f ./app/schema.sql
```

4. Start the docker container:

```Bash
sudo docker compose up
```
---

## 🌐 Common URIs

| URI                           | Description                           |
| ----------------------------- | ------------------------------------- |
| http://0.0.0.0:8000/v3/tasks/ | CRUD operations                       |
| http://0.0.0.0:8000/docs/     | Auto-generated OpenAPI **Swagger UI** |
| http://0.0.0.0:8000/redoc/    | Auto-generated OpenAPI **ReDoc**      |

---

## Priority Enum

This is an Enumeration containing the main Priorities usually used in Task Management applications.  
It contains 4 main priorities:

```Python
from enum import StrEnum

class Priorities(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"
```

---

# Tests coverage

1. Create a `TEST_DATABASE_URL` env var:
```.env
TEST_DATABASE_URL=postgresql://POSTGRES_USER:POSTGRES_PASSWORD@db:5432/POSTGRES_TEST_DB
```
the intended database must be seperate from the production database.

2. Enter Docker shell:
```Bash
sudo docker exec -it py-tasks-backend-1 sh
```

3. Run tests:
```Bash
cd app
pytest -v
```

---

## 🔮 Future Improvements

- _Pagination_.
