from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


def test_health_is_available_without_a_gemini_key():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_question_validation_rejects_blank_input():
    response = client.post("/qa", json={"question": "   "})
    assert response.status_code == 422


def test_qa_endpoint_uses_the_question_contract(monkeypatch):
    monkeypatch.setattr(main, "answer_question", lambda question: f"Answer: {question}")
    response = client.post("/qa", json={"question": "Which is the largest ocean?"})
    assert response.status_code == 200
    assert response.json() == {"answer": "Answer: Which is the largest ocean?"}


def test_learning_path_accepts_a_level(monkeypatch):
    monkeypatch.setattr(main, "get_learning_recommendations", lambda topic, level: f"{level}: {topic}")
    response = client.post(
        "/learn/recommendations",
        json={"topic": "SQL", "level": "intermediate"},
    )
    assert response.status_code == 200
    assert response.json() == {"result": "intermediate: SQL"}


def test_routes_manifest_is_served_as_json():
    response = client.get("/manus-routes.json")
    assert response.status_code == 200
    assert response.json()["routes"][0]["path"] == "/"
