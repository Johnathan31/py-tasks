"""Tests for PUT and PATCH /v2/tasks/{_id}."""
TASKS_URL = "/v2/tasks/"


def create_task(client, *, title="Original title", priority="normal", done=False):
    response = client(
        "POST",
        TASKS_URL,
        json={"title": title, "priority": priority, "done": done},
    )
    assert response.status_code == 201
    return response.json()["task"]


def test_put_replaces_all_mutable_fields(client):
    task = create_task(client, title="Before", priority="low", done=False)

    response = client(
        "PUT",
        f"{TASKS_URL}{task['id']}",
        json={"title": "After", "priority": "critical", "done": True},
    )

    assert response.status_code == 204
    updated = client("GET", f"{TASKS_URL}{task['id']}").json()["task"]
    assert updated["title"] == "After"
    assert updated["priority"] == "critical"
    assert updated["done"] is True


def test_put_missing_id_returns_404(client):
    response = client(
        "PUT",
        f"{TASKS_URL}2147483000",
        json={"title": "Replacement", "priority": "normal", "done": False},
    )

    assert response.status_code == 404


def test_put_accepts_missing_fields(client):
    task = create_task(client)
    response = client("PUT", f"{TASKS_URL}{task['id']}", json={"title": "Incomplete"})

    assert response.status_code == 204


def test_put_rejects_invalid_priority(client):
    task = create_task(client)
    response = client(
        "PUT",
        f"{TASKS_URL}{task['id']}",
        json={"title": "Updated", "priority": "urgent", "done": False},
    )

    assert response.status_code == 422


def test_put_rejects_title_over_50_characters(client):
    task = create_task(client)
    response = client(
        "PUT",
        f"{TASKS_URL}{task['id']}",
        json={"title": "x" * 51, "priority": "normal", "done": False},
    )

    assert response.status_code == 422


def test_patch_updates_only_supplied_field(client):
    task = create_task(client, title="Keep title", priority="low", done=False)

    response = client("PATCH", f"{TASKS_URL}{task['id']}", json={"done": True})

    assert response.status_code == 204
    updated = client("GET", f"{TASKS_URL}{task['id']}").json()["task"]
    assert updated["title"] == "Keep title"
    assert updated["priority"] == "low"
    assert updated["done"] is True


def test_patch_can_update_multiple_fields(client):
    task = create_task(client, title="Before", priority="low", done=False)

    response = client(
        "PATCH",
        f"{TASKS_URL}{task['id']}",
        json={"title": "After", "priority": "high"},
    )

    assert response.status_code == 204
    updated = client("GET", f"{TASKS_URL}{task['id']}").json()["task"]
    assert updated["title"] == "After"
    assert updated["priority"] == "high"
    assert updated["done"] is False


def test_patch_can_set_done_to_false(client):
    task = create_task(client, done=True)

    response = client("PATCH", f"{TASKS_URL}{task['id']}", json={"done": False})

    assert response.status_code == 204
    assert client("GET", f"{TASKS_URL}{task['id']}").json()["task"]["done"] is False


def test_patch_empty_body_returns_422(client):
    task = create_task(client)
    response = client("PATCH", f"{TASKS_URL}{task['id']}", json={})

    assert response.status_code == 422


def test_patch_missing_id_returns_404(client):
    response = client("PATCH", f"{TASKS_URL}2147483000", json={"done": True})

    assert response.status_code == 404


def test_patch_rejects_invalid_priority(client):
    task = create_task(client)
    response = client("PATCH", f"{TASKS_URL}{task['id']}", json={"priority": "urgent"})

    assert response.status_code == 422


def test_patch_rejects_title_over_50_characters(client):
    task = create_task(client)
    response = client(
        "PATCH",
        f"{TASKS_URL}{task['id']}",
        json={"title": "x" * 51},
    )

    assert response.status_code == 422


def test_patch_explicit_null_is_distinct_from_omitted_field(client):
    task = create_task(client, title="Original")
    response = client("PATCH", f"{TASKS_URL}{task['id']}", json={"title": None})

    # TaskOptionalFields currently permits Optional[str]. The SQL schema also
    # permits NULL in title, so this request is expected to succeed.
    assert response.status_code == 204
    updated = client("GET", f"{TASKS_URL}{task['id']}").json()["task"]
    assert updated["title"] is None
