import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.tasks.clear()
    app_module.next_id = 1
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_index_lists_endpoints(client):
    response = client.get("/")
    body = response.get_json()
    assert response.status_code == 200
    assert "/tasks" in body["endpoints"]


def test_create_and_list_tasks(client):
    response = client.post("/tasks", json={"title": "write a Dockerfile"})
    assert response.status_code == 201
    task = response.get_json()
    assert task["id"] == 1
    assert task["done"] is False

    response = client.get("/tasks")
    assert response.get_json() == [task]


def test_create_task_requires_title(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 400


def test_delete_task(client):
    client.post("/tasks", json={"title": "temp"})
    assert client.delete("/tasks/1").status_code == 204
    assert client.delete("/tasks/1").status_code == 404
