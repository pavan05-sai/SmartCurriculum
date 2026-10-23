# SmartCurriculum Comprehensive API Integration Tests (MongoDB)

import pytest


def _register_user(client, email="test.user@example.com"):
    response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "password123",
            "name": "Test User",
            "semester": 4,
            "skill_level": "intermediate",
            "career_goal": "placement"
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
    assert "MongoDB" in data["database_type"]


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "SmartCurriculum API"
    assert "endpoints" in data


def test_auth_flow(client):
    # 1. Register
    token = _register_user(client, "alice@example.com")
    assert token is not None

    # 2. Duplicate registration should fail with 409
    dup = client.post(
        "/api/auth/register",
        json={"email": "alice@example.com", "password": "password123", "name": "Alice"},
    )
    assert dup.status_code == 409

    # 3. Login
    login = client.post(
        "/api/auth/login",
        json={"email": "alice@example.com", "password": "password123"},
    )
    assert login.status_code == 200
    assert "access_token" in login.get_json()

    # 4. Profile
    profile = client.get(
        "/api/auth/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert profile.status_code == 200
    assert profile.get_json()["user"]["email"] == "alice@example.com"


def test_curriculum_crud(client):
    token = _register_user(client, "curriculum_user@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Generate curriculum
    gen = client.post(
        "/api/curriculum/generate",
        headers=headers,
        json={"duration_weeks": 4, "hours_per_week": 8}
    )
    assert gen.status_code == 201
    curr_data = gen.get_json()["curriculum"]
    curr_id = curr_data["id"]
    assert curr_id is not None
    assert len(curr_data["topics"]) > 0

    # Retrieve all curricula
    get_all = client.get("/api/curriculum/", headers=headers)
    assert get_all.status_code == 200
    assert len(get_all.get_json()["curricula"]) >= 1

    # Retrieve specific curriculum
    get_one = client.get(f"/api/curriculum/{curr_id}", headers=headers)
    assert get_one.status_code == 200
    assert get_one.get_json()["curriculum"]["id"] == curr_id

    # Mark topic completed
    topic_id = curr_data["topics"][0]["id"]
    complete = client.put(
        f"/api/curriculum/{curr_id}/topics/{topic_id}/complete",
        headers=headers
    )
    assert complete.status_code == 200
    assert complete.get_json()["topic"]["status"] == "completed"


def test_ai_features(client):
    token = _register_user(client, "ai_user@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Notes generation
    notes = client.post(
        "/api/ai/generate-notes",
        headers=headers,
        json={"topic_title": "Python Basics", "detail_level": "intermediate"}
    )
    assert notes.status_code == 200
    assert "notes" in notes.get_json()

    # MCQ generation
    mcqs = client.post(
        "/api/ai/generate-mcqs",
        headers=headers,
        json={"topic_title": "Python Basics", "count": 2}
    )
    assert mcqs.status_code == 200
    assert len(mcqs.get_json()["mcqs"]) > 0

    # Skill gap analysis
    gap = client.post(
        "/api/ai/skill-gap",
        headers=headers,
        json={"target_role": "Full Stack Developer"}
    )
    assert gap.status_code == 200
    assert "skill_analysis" in gap.get_json()


def test_resume_skills(client):
    token = _register_user(client, "resume_user@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Add skill
    add_s = client.post(
        "/api/resume/skills",
        headers=headers,
        json={"name": "Python", "level": "intermediate"}
    )
    assert add_s.status_code == 201
    skill_id = add_s.get_json()["skill"]["id"]

    # Get skills
    get_s = client.get("/api/resume/skills", headers=headers)
    assert get_s.status_code == 200
    assert get_s.get_json()["total"] == 1

    # Update skill
    up_s = client.put(
        f"/api/resume/skills/{skill_id}",
        headers=headers,
        json={"level": "advanced", "proficiency_score": 80}
    )
    assert up_s.status_code == 200
    assert up_s.get_json()["skill"]["level"] == "advanced"

    # Export skills
    exp = client.get("/api/resume/export", headers=headers)
    assert exp.status_code == 200
    assert "sections" in exp.get_json()


def test_admin_analytics(client):
    token = _register_user(client, "admin_user@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    analytics = client.get("/api/admin/analytics", headers=headers)
    assert analytics.status_code == 200
    data = analytics.get_json()["analytics"]
    assert "users" in data
    assert "curricula" in data
    assert "skills" in data
