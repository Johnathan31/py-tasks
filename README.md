# 🚀 FastAPI + PostgreSQL

A **Python** task manager API (CRUD API) built with FastAPI and PostgreSQL.
It demonstrates building a _Medium-Scaled_ Python API, using FastAPI.

---

## 📚 Tech Stack

| Name         | Description                        |
| ------------ | ---------------------------------- |
| FastAPI      | A REST API server                  |
| Pydantic     | Data Structures and models         |
| Enums        | Making key-value pairs collections |
| PostgreSQL   | Persistent Database Storage        |
| Dotenv       | Accessing Environment variables    |
| psycopg3     | PostgreSQL Python Driver           |
| psycopg_pool | _psycopg3_ Pooling driver          |
| logging      | Logging error tracebacks           |

---

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

---

# 🪾 Project Tree

```text
py-tasks
├── app # application source code
│   ├── database # database configs
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
│   ├── __init__.py
│   ├── exceptions.py # exceptions handler
│   ├── main.py # main FastAPI file
│   └── schema.sql # main SQL Schema
├── .env.example # sample .env file
├── .gitignore
├── README.md
├── __init__.py
├── api.md # Some API descriptions
├── requirements.txt # python packages requirements
└── start.sh # a small script to serve the API
```

---

## 🌀 Prerequisites

### Packages, Modules

- Python _v3.13_
- FastAPI _v0.138_
- Rust (for compiling FastAPI source code)
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

2. Install and activate the _Virtual Environment_, depending on your OS:

```Bash
python -m venv .venv

# Windows command prompt (cmd)
.venv\Scripts\activate.bat

# Windows Powershell
.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate
```

3. Install requirements and dependencies:

```
pip install -r ./requirements.txt
```

4. Run the main [SQL Queries](./app/schema.sql)

```
psql -d tasks -f ./app/schema.sql
```

5. Run _PostgreSQL_ service:

```Bash
# Linux
systemctl start postgresql

# Some Linux Distributions
service postgresql start

# MacOS
brew services start postgresql

# Windows
net start postgresql-x64-17
```

6. Create a `.env` file:

```env
PORT=5432
HOST=localhost
USER=postgres
PASSWORD=my_password
DB=tasks
DEBUG=true
```

For more details, see [.env sample file](./.env.example)

7. Run the server using [uvicorn](https://uvicorn.dev):

```Bash
uvicorn app.main:app --reload --host=0.0.0.0
```

or directly with a ready [shell script](./start.sh):

```Bash
chmod +x start.sh
./start.sh
```

---

## 🌐 Common URIs

| URI                           | Description                           |
| ----------------------------- | ------------------------------------- |
| http://0.0.0.0:8000/v2/tasks/ | CRUD operations                       |
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

## 🔮 Future Improvements

- _Pagination_.

- Using **Docker Container** for a fully isolated environment.

- Implementing a frontend service (e.g. React/Vue) to complete the stack.

- Unit tests.
