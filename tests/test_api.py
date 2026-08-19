from fastapi.testclient import TestClient

from api.main import app


def test_root():
    with TestClient(app) as client:

        response = client.get("/")

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "ok"


def test_health():
    with TestClient(app) as client:

        response = client.get("/health")

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "healthy"
        assert data["model_ready"] is True


def test_ask_resume():
    with TestClient(app) as client:

        response = client.post(
            "/ask",
            json={
                "question": "Where does Aman currently work?"
            }
        )

        assert response.status_code == 200

        data = response.json()

        assert "answer" in data
        assert "sources" in data

        assert "NEXLINE PHARMA" in data["answer"].upper()

        assert len(data["sources"]) > 0


if __name__ == "__main__":

    print("=" * 60)
    print("FASTAPI PRODUCTION TEST")
    print("=" * 60)

    test_root()
    print("✅ GET / passed")

    test_health()
    print("✅ GET /health passed")

    test_ask_resume()
    print("✅ POST /ask passed")

    print("\n" + "=" * 60)
    print("FASTAPI PRODUCTION TEST COMPLETED")
    print("=" * 60)