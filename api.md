# API Docs

## 🌂 Endpoints

| Method | Endpoint         | Description           |
| ------ | ---------------- | --------------------- |
| GET    | /tasks/          | Get all tasks         |
| GET    | /tasks/{\_id}    | Get a task by ID      |
| POST   | /tasks/          | Create a task         |
| DELETE | /tasks/          | Delete all tasks      |
| DELETE | /tasks/{\_id}    | Delete a task by ID   |
| DELETE | /tasks/completed | Delete finished tasks |
| PUT    | /tasks/{\_id}    | Update a task by ID   |
| PATCH  | /tasks/{\_id}    | Update part of a task |

---

## 📨 Example Requests

### Create a task

#### Request

```http
POST /tasks/ HTTP/1.1
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
GET /tasks/1 HTTP/1.1
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

### Delete a task by ID

#### Request

```http
DELETE /tasks/1 HTTP/1.1
```

#### Response

```http
HTTP/1.1 204 No Content
```

---

### Update part of a task

#### Request

```http
PATCH /tasks/1 HTTP/1.1
```

```JSON
{
  "done": true
}
```

#### Response

```http
HTTP/1.1 204 No Content
```
