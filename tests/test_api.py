import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["loaded_transcripts"] == 3

def test_get_transcripts():
    res = client.get("/api/transcripts")
    assert res.status_code == 200
    data = res.json()
    assert data["count"] == 3
    assert len(data["transcripts"]) == 3

def test_get_interview_guide():
    res = client.get("/api/interview-guide")
    assert res.status_code == 200
    data = res.json()
    assert data["total_questions"] == 6
    assert len(data["analysis"]) == 6

def test_get_synthesis():
    res = client.get("/api/synthesis")
    assert res.status_code == 200
    data = res.json()
    assert "executive_summary" in data
    assert len(data["market_comparison"]) == 3
    assert len(data["common_themes"]) >= 3
    assert len(data["disagreements"]) >= 3

def test_qa_grounded_query():
    res = client.post("/api/qa", json={"query": "What do experts say about surgeon training?"})
    assert res.status_code == 200
    data = res.json()
    assert data["is_grounded"] is True
    assert len(data["citations"]) > 0
    assert data["confidence_score"] > 0.9

def test_qa_out_of_domain_refusal():
    res = client.post("/api/qa", json={"query": "What is the capital of Australia?"})
    assert res.status_code == 200
    data = res.json()
    assert data["is_grounded"] is False
    assert "Not Mentioned in Transcripts" in data["answer"]
