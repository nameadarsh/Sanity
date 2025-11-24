import types

import pytest

from backend import app as backend_app


@pytest.fixture()
def client(monkeypatch):
    backend_app.app.testing = True
    monkeypatch.setattr(backend_app, "load_model", lambda: ("tokenizer", "model"))
    return backend_app.app.test_client()


def test_predict_success(client, monkeypatch):
    monkeypatch.setattr(backend_app, "resolve_text", lambda payload: "sample text")
    monkeypatch.setattr(
        backend_app,
        "run_model_inference",
        lambda text: {
            "label": "Real",
            "confidence": 0.92,
            "needs_verification": False,
            "probabilities": {"fake": 0.08, "real": 0.92},
        },
    )
    response = client.post("/predict", json={"text": "foo"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["label"] == "Real"
    assert pytest.approx(data["confidence"], rel=1e-3) == 0.92


def test_predict_validation_error(client, monkeypatch):
    def raise_error(_payload):
        raise ValueError("No text provided.")

    monkeypatch.setattr(backend_app, "resolve_text", raise_error)
    response = client.post("/predict", json={})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_verify_endpoint(client, monkeypatch):
    dummy_response = types.SimpleNamespace(
        prediction="Real",
        reasoning="Looks legitimate.",
        raw={"id": "abc"},
    )

    class DummyGroq:
        def verify_article(self, article_text):
            assert article_text == "sample"
            return dummy_response

    monkeypatch.setattr(backend_app, "get_groq_client", lambda: DummyGroq())
    response = client.post("/verify", json={"article_text": "sample"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["prediction"] == "Real"
    assert "reasoning" in data


def test_verify_requires_article_text(client):
    response = client.post("/verify", json={})
    assert response.status_code == 400


def test_ask_endpoint(client, monkeypatch):
    class DummyGroq:
        def answer_question(self, summary, question):
            assert summary == "context"
            assert question == "What?"
            return "Answer"

    monkeypatch.setattr(backend_app, "get_groq_client", lambda: DummyGroq())
    response = client.post("/ask", json={"article_summary": "context", "question": "What?"})
    assert response.status_code == 200
    assert response.get_json()["answer"] == "Answer"


def test_ask_requires_fields(client):
    response = client.post("/ask", json={"article_summary": "only"})
    assert response.status_code == 400


def test_log_endpoint(client, monkeypatch):
    captured = {}

    def fake_log(message):
        captured["msg"] = message

    monkeypatch.setattr(backend_app, "update_progress_log", fake_log)
    response = client.post("/log", json={"message": "Test entry"})
    assert response.status_code == 200
    assert captured["msg"] == "Test entry"

