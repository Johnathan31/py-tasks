# API Docs

## 🌂 Endpoints

| Method | Endpoint         | Description           |
| ------ | ---------------- | --------------------- |
| GET    | /v2/tasks/          | Get all tasks         |
| GET    | /v2/tasks/{\_id}    | Get a task by ID      |
| POST   | /v2/tasks/          | Create a task         |
| DELETE | /v2/tasks/          | Delete all tasks      |
| DELETE | /v2/tasks/{\_id}    | Delete a task by ID   |
| DELETE | /v2/tasks/completed | Delete finished tasks |
| PUT    | /v2/tasks/{\_id}    | Update a task by ID   |
| PATCH  | /v2/tasks/{\_id}    | Update part of a task |

---

## 📨 Example Requests

### Create a task

#### Request

```http
POST /v2/tasks/ HTTP/1.1
Content-Type: application/json
```

```JSON
{
  "title": "Buying groceries",
  "priority": "high",
  "done": false
}
```

#### Response

```http
HTTP/1.1 201 Created
```

```JSON
{
  "task": {
    "id": 1,
    "title": "Buying groceries",
    "priority": "high",
    "done": false
  }
}
```

---

### Get a task

#### Request

```http
GET /v2/tasks/1 HTTP/1.1
```

#### Response

```http
HTTP/1.1 200 OK
```

```JSON
{
  "task": {
    "id": 1,
    "title": "Buying groceries",
    "priority": "high",
    "done": false
  }
}
```

---

### Get all tasks

#### Request

```http
GET /v2/tasks/?search=groceries HTTP/1.1
```

#### Response

```http
HTTP/1.1 200 OK
```

```JSON
{
  "tasks": [
    {
      "done": false,
      "id": 1,
      "priority": "high",
      "title": ""
    }
  ]
}
```

---

### Delete a task by ID

#### Request

```http
DELETE /v2/tasks/1 HTTP/1.1
```

#### Response

```http
HTTP/1.1 204 No Content
```

---

### Update part of a task

#### Request (example 1)

```http
PATCH /v2/tasks/1 HTTP/1.1
```

```JSON
{
  "done": true
}
```

Worth noting that one or more fields in the task can be updated, each being optional.

#### Response

```http
HTTP/1.1 204 No Content
```

#### Request (example 2)

```http
PATCH /v2/tasks/1 HTTP/1.1
```

```JSON
{}
```

#### Response

```http
HTTP/1.1 422 Unprocessable Content
```

```JSON
{
  "error": "HTTPException",
  "message": {
    "error": "Empty request body content."
  }
}
```

---

### Update a task by ID

#### Request

```http
PUT /v2/tasks/1 HTTP/1.1
```

```JSON
{
  "title": "Studying",
  "priority": "low",
}
```

#### Response

```http
HTTP/1.1 422 Unprocessable Content
{
  "error": "Request Validation Error",
  "details": [
    {
      "type": "missing",
      "msg": "Field required",
      "loc": ["body", "done"],
      "input": {
        "title": "Shopping",
        "priority": "high"
      }
    }
  ]
}
```
