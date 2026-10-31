"""Tests for POST /v3/tasks/."""
import pytest
from fastapi.exceptions import RequestValidationError

TASKS_URL = "/v3/tasks/"


def valid_payload(**overrides):
    payload = {
        "title": "Finish unit tests",
        "priority": "high",
        "done": False,
    }
    payload.update(overrides)
    return payload


def test_create_task_returns_created_task(client):
    response = client("POST", TASKS_URL, json=valid_payload())

    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"task"}
    assert body["task"]["id"] is not None
    assert body["task"]["title"] == "Finish unit tests"
    assert body["task"]["priority"] == "high"
    assert body["task"]["done"] is False


def test_create_defaults_priority_and_done_when_omitted(client):
    response = client("POST", TASKS_URL, json={"title": "Use defaults"})

    assert response.status_code == 201
    task = response.json()["task"]
    assert task["title"] == "Use defaults"
    assert task["priority"] == "normal"
    assert task["done"] is False


def test_create_allows_priority_to_be_omitted(client):
    response = client(
        "POST",
        TASKS_URL,
        json={"title": "Default priority", "done": True},
    )

    assert response.status_code == 201
    task = response.json()["task"]
    assert task["priority"] == "normal"
    assert task["done"] is True


def test_create_allows_done_to_be_omitted(client):
    response = client(
        "POST",
        TASKS_URL,
        json={"title": "Default completion state", "priority": "high"},
    )

    assert response.status_code == 201
    task = response.json()["task"]
    assert task["priority"] == "high"
    assert task["done"] is False


@pytest.mark.parametrize("priority", ["low", "normal", "high", "critical"])
def test_create_accepts_each_valid_priority(client, priority):
    response = client("POST", TASKS_URL, json=valid_payload(priority=priority))

    assert response.status_code == 201
    assert response.json()["task"]["priority"] == priority


@pytest.mark.parametrize("done", [True, False])
def test_create_accepts_both_done_values(client, done):
    response = client("POST", TASKS_URL, json=valid_payload(done=done))

    assert response.status_code == 201
    assert response.json()["task"]["done"] is done


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"priority": "normal", "done": False},
    ],
)
def test_create_rejects_missing_required_fields(client, payload):
    response = client("POST", TASKS_URL, json=payload)

    assert response.status_code == 422


@pytest.mark.parametrize("priority", ["urgent", "LOW", "", None, 1])
def test_create_rejects_invalid_priority(client, priority):
    response = client("POST", TASKS_URL, json=valid_payload(priority=priority))

    assert response.status_code == 422


def test_create_rejects_title_longer_than_50_characters(client):
    response = client("POST", TASKS_URL, json=valid_payload(title="x" * 51))

    assert response.status_code == 422


def test_create_accepts_title_of_exactly_50_characters(client):
    title = "x" * 50
    response = client("POST", TASKS_URL, json=valid_payload(title=title))

    assert response.status_code == 201
    assert response.json()["task"]["title"] == title


@pytest.mark.parametrize("title", [123, True, ["title"], {"text": "title"}])
def test_create_rejects_non_string_title(client, title):
    response = client("POST", TASKS_URL, json=valid_payload(title=title))

    assert response.status_code == 422
