"""Tests for GET /v2/tasks/ and GET /v2/tasks/{_id}."""
TASKS_URL = "/v2/tasks/"


def create_task(client, *, title="Read test task", priority="normal", done=False):
    response = client(
        "POST",
        TASKS_URL,
        json={"title": title, "priority": priority, "done": done},
    )
    assert response.status_code == 201
    return response.json()["task"]


def test_list_tasks_returns_tasks_array(client):
    created = create_task(client)
    response = client("GET", TASKS_URL)

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["tasks"], list)
    assert any(task["id"] == created["id"] for task in body["tasks"])


def test_list_tasks_can_return_empty_list(client):
    response = client("GET", TASKS_URL)

    assert response.status_code == 200
    assert response.json() == {"tasks": []}


def test_get_task_by_id_returns_matching_task(client):
    created = create_task(client, title="Find this task", priority="critical", done=True)

    response = client("GET", f"{TASKS_URL}{created['id']}")

    assert response.status_code == 200
    assert response.json()["task"] == created


def test_get_missing_task_returns_404(client):
    response = client("GET", f"{TASKS_URL}2147483000")

    assert response.status_code == 404
    assert "error" in response.json()
    assert "message" in response.json()


def test_get_task_rejects_non_integer_id(client):
    response = client("GET", f"{TASKS_URL}not-an-id")

    assert response.status_code == 404


def test_filter_by_priority(client):
    matching = create_task(client, title="High priority", priority="high")
    create_task(client, title="Low priority", priority="low")

    response = client("GET", TASKS_URL, params={"priority": "high"})

    assert response.status_code == 200
    tasks = response.json()["tasks"]
    assert [task["id"] for task in tasks] == [matching["id"]]


def test_filter_by_done_false_does_not_treat_false_as_missing(client):
    incomplete = create_task(client, title="Incomplete", done=False)
    create_task(client, title="Complete", done=True)

    response = client("GET", TASKS_URL, params={"done": "false"})

    assert response.status_code == 200
    tasks = response.json()["tasks"]
    assert [task["id"] for task in tasks] == [incomplete["id"]]


def test_filter_by_done_true(client):
    complete = create_task(client, title="Complete", done=True)
    create_task(client, title="Incomplete", done=False)

    response = client("GET", TASKS_URL, params={"done": "true"})

    assert response.status_code == 200
    assert [task["id"] for task in response.json()["tasks"]] == [complete["id"]]


def test_filter_by_title_search_is_case_insensitive_and_partial(client):
    matching = create_task(client, title="Prepare PYTEST Report")
    create_task(client, title="Clean desk")

    response = client("GET", TASKS_URL, params={"search": "pytest"})

    assert response.status_code == 200
    assert [task["id"] for task in response.json()["tasks"]] == [matching["id"]]


def test_filters_can_be_combined(client):
    matching = create_task(client, title="Study maths", priority="high", done=False)
    create_task(client, title="Study history", priority="low", done=False)
    create_task(client, title="Study physics", priority="high", done=True)

    response = client(
        "GET",
        TASKS_URL,
        params={"priority": "high", "done": "false", "search": "study"},
    )

    assert response.status_code == 200
    assert [task["id"] for task in response.json()["tasks"]] == [matching["id"]]


def test_invalid_priority_filter_returns_422(client):
    response = client("GET", TASKS_URL, params={"priority": "urgent"})

    assert response.status_code == 422


def test_invalid_done_filter_returns_422(client):
    response = client("GET", TASKS_URL, params={"done": "sometimes"})

    assert response.status_code == 422


def test_empty_search_returns_all_tasks(client):
    create_task(client, title="Alpha")
    create_task(client, title="Beta")

    response = client("GET", TASKS_URL, params={"search": ""})

    assert response.status_code == 200
    assert len(response.json()["tasks"]) == 2
