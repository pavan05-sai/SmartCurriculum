def _register_user(client, email="test.user@example.com"):
    response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "password123",
            "name": "Test User",
        },
    )

    assert response.status_code == 201
    data = response.get_json()
    return data["access_token"]


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "SmartCurriculum API"


def test_generate_notes_requires_auth(client):
    response = client.post(
        "/api/ai/generate-notes",
        json={"topic_title": "Python Basics"},
    )
    assert response.status_code == 401


def test_generate_notes_with_token(client):
    token = _register_user(client)
    response = client.post(
        "/api/ai/generate-notes",
        headers={"Authorization": f"Bearer {token}"},
        json={"topic_title": "Python Basics"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["topic"] == "Python Basics"
    assert "notes" in data
    assert "content" in data["notes"]
