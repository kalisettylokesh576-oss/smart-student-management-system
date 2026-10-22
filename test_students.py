import pytest
from fastapi.testclient import TestClient
import app.database as database
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test_students.db"
    monkeypatch.setattr(database, "DATABASE", str(db_path))
    database.init_db()

    with TestClient(app) as test_client:
        yield test_client


def sample_student(email="priya@example.com"):
    return {
        "name": "Priya Sharma",
        "dob": "2005-11-20",
        "email": email,
        "course": "AI and ML"
    }


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_create_and_read_student(client):
    response = client.post("/students", json=sample_student())
    assert response.status_code == 201
    student_id = response.json()["student_id"]

    response = client.get(f"/students/{student_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Priya Sharma"


def test_read_all_students(client):
    client.post("/students", json=sample_student())
    response = client.get("/students")
    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_update_student(client):
    created = client.post("/students", json=sample_student())
    student_id = created.json()["student_id"]

    updated = sample_student()
    updated["course"] = "Computer Science"

    response = client.put(f"/students/{student_id}", json=updated)
    assert response.status_code == 200

    result = client.get(f"/students/{student_id}")
    assert result.json()["course"] == "Computer Science"


def test_delete_student(client):
    created = client.post("/students", json=sample_student())
    student_id = created.json()["student_id"]

    response = client.delete(f"/students/{student_id}")
    assert response.status_code == 200
    assert client.get(f"/students/{student_id}").status_code == 404


def test_search_student(client):
    client.post("/students", json=sample_student())

    response = client.get("/search/students", params={"name": "Priya"})
    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_duplicate_email(client):
    client.post("/students", json=sample_student())
    response = client.post("/students", json=sample_student())
    assert response.status_code == 409


def test_invalid_email(client):
    data = sample_student("not-an-email")
    response = client.post("/students", json=data)
    assert response.status_code == 422


def test_invalid_date(client):
    data = sample_student()
    data["dob"] = "2020-15-40"
    response = client.post("/students", json=data)
    assert response.status_code == 422


def test_missing_student(client):
    response = client.get("/students/999999")
    assert response.status_code == 404
