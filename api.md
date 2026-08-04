# API Docs

## 🌂 Endpoints

| Method | Endpoint            | Description           |
| ------ | ------------------- | --------------------- |
| GET    | /v1/tasks/          | Get all tasks         |
| GET    | /v1/tasks/{\_id}    | Get a task by ID      |
| POST   | /v1/tasks/          | Create a task         |
| DELETE | /v1/tasks/          | Delete all tasks      |
| DELETE | /v1/tasks/{\_id}    | Delete a task by ID   |
| DELETE | /v1/tasks/completed | Delete finished tasks |
| PUT    | /v1/tasks/{\_id}    | Update a task by ID   |
| PATCH  | /v1/tasks/{\_id}    | Update part of a task |

---

## 📨 Example Requests

### Create a task

#### Request

```http
POST /v1/tasks/ HTTP/1.1
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
GET /v1/tasks/1 HTTP/1.1
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
DELETE /v1/tasks/1 HTTP/1.1
```

#### Response

```http
HTTP/1.1 204 No Content
```

---

### Update part of a task

#### Request

```http
PATCH /v1/tasks/1 HTTP/1.1
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
