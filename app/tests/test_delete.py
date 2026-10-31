"""Tests for DELETE /v3/tasks/ and DELETE /v3/tasks/{_id}."""
TASKS_URL = "/v3/tasks/"


def create_task(client, *, title="Task to delete", priority="normal", done=False):
    response = client(
        "POST",
        TASKS_URL,
        json={"title": title, "priority": priority, "done": done},
    )
    assert response.status_code == 201
    return response.json()["task"]


def test_delete_task_by_id_returns_204_and_removes_task(client):
    task = create_task(client)

    response = client("DELETE", f"{TASKS_URL}{task['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client("GET", f"{TASKS_URL}{task['id']}").status_code == 404


def test_delete_missing_id_returns_404(client):
    response = client("DELETE", f"{TASKS_URL}2147483000")

    assert response.status_code == 404


def test_delete_all_tasks_without_body(client):
    create_task(client, title="First")
    create_task(client, title="Second")

    response = client("DELETE", TASKS_URL)

    assert response.status_code == 204
    assert client("GET", TASKS_URL).json()["tasks"] == []


def test_delete_all_tasks_rejects_empty_json_object(client):
    create_task(client)

    response = client("DELETE", TASKS_URL, json={})

    assert response.status_code == 422


def test_delete_selected_ids(client):
    first = create_task(client, title="Keep")
    second = create_task(client, title="Delete one")
    third = create_task(client, title="Delete two")

    response = client("DELETE", TASKS_URL, json={"ids": [second["id"], third["id"]]})

    assert response.status_code == 204
    remaining_ids = [task["id"] for task in client("GET", TASKS_URL).json()["tasks"]]
    assert remaining_ids == [first["id"]]


def test_delete_selected_ids_deduplicates_repeated_ids(client):
    task = create_task(client)

    response = client("DELETE", TASKS_URL, json={"ids": [task["id"], task["id"]]})

    assert response.status_code == 204
    assert client("GET", TASKS_URL).json()["tasks"] == []


def test_delete_selected_empty_ids_returns_422(client):
    response = client("DELETE", TASKS_URL, json={"ids": []})

    assert response.status_code == 422


def test_delete_selected_nonexistent_id_returns_404(client):
    task = create_task(client)

    response = client("DELETE", TASKS_URL, json={"ids": [task["id"], 2147483000]})

    assert response.status_code == 404
    # The dependency should roll back the partial DELETE when the endpoint
    # raises HTTPException; verify the existing task was not lost.
    assert client("GET", f"{TASKS_URL}{task['id']}").status_code == 200


def test_delete_done_tasks_removes_only_completed_tasks(client):
    completed_one = create_task(client, title="Completed one", done=True)
    completed_two = create_task(client, title="Completed two", done=True)
    pending = create_task(client, title="Still pending", done=False)

    response = client("DELETE", f"{TASKS_URL}completed")

    assert response.status_code == 204
    remaining = client("GET", TASKS_URL).json()["tasks"]
    assert [task["id"] for task in remaining] == [pending["id"]]
    assert all(task["id"] not in {completed_one["id"], completed_two["id"]} for task in remaining)


def test_delete_done_tasks_is_safe_when_none_are_completed(client):
    task = create_task(client, done=False)

    response = client("DELETE", f"{TASKS_URL}completed")

    assert response.status_code == 204
    assert client("GET", f"{TASKS_URL}{task['id']}").status_code == 200


def test_delete_selected_requires_ids_to_be_a_list(client):
    response = client("DELETE", TASKS_URL, json={"ids": "1"})

    assert response.status_code == 422
