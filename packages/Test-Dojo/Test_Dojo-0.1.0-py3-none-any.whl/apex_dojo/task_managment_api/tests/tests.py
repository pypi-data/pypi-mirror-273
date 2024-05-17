from starlette.testclient import TestClient

from apex_dojo.task_managment_api.fastapi import FastApiConfig


def test_create():
    client = TestClient(FastApiConfig().setup())

    response = client.post("/tasks", json={"task": "hello world"})

    assert response.status_code == 201
    assert response.json() == {
        "id": "e98d12c2-e50a-46d3-8cb8-9add8d426152",
        "task": "hello world",
    }
