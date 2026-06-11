import os
import json
import pytest
from app.main import create_app
from app.config import settings

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_and_ready(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"

    res_ready = client.get("/api/v1/ready")
    assert res_ready.status_code == 200
    data_ready = res_ready.get_json()
    assert data_ready["status"] == "ready"

def test_list_documents(client):
    res = client.get("/api/v1/documents")
    assert res.status_code == 200
    data = res.get_json()
    assert "total" in data
    assert "items" in data

def test_search_endpoint(client):
    res = client.post("/api/v1/search", json={
        "query": "payment terms Net 30 days",
        "top_k": 3
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "results" in data
    assert "retrieval_latency_ms" in data

def test_chat_grounded_answer(client):
    res = client.post("/api/v1/chat", json={
        "message": "What are the payment terms under the agreement?",
        "top_k": 3,
        "strict_grounding": True
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "answer" in data
    assert "citations" in data
    assert data["abstained"] is False

def test_chat_abstention_on_unanswerable(client):
    res = client.post("/api/v1/chat", json={
        "message": "What is the secret alien recipe for anti-gravity propulsion mentioned in the contract?",
        "top_k": 3,
        "strict_grounding": True
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["abstained"] is True
    assert "ABSTAIN" in data["answer"]

def test_agent_run_workflow(client):
    res = client.post("/api/v1/agent/run", json={
        "goal": "Audit contract payment terms and identify compliance obligations"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "run_id" in data
    assert data["status"] == "completed"
    assert len(data["steps"]) >= 4
    assert data["final_output"] is not None
