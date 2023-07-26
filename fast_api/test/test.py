import sys
from fastapi.testclient import TestClient
from unittest.mock import patch

# Adicione o diretório raiz da sua aplicação FastAPI ao PYTHONPATH
sys.path.append("/app/fast_api")

from fast_api.main import app  # Agora você pode importar o módulo main corretamente

client = TestClient(app)


def test_get_items_with_urls():
    response = client.get("/items")
    print(">>>>>>")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert isinstance(response.json(), list)
    assert all(isinstance(item, dict) for item in response.json())


def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert isinstance(response.json(), list)
    assert all("title" in item and "link" in item for item in response.json())


def test_get_items_with_urls_no_source_url():
    # Teste de sucesso: Verificar o comportamento quando um item de notícia não possui URL de fonte
    feed_with_no_source_url = [
        {"title": "News 1", "link": "https://news.com/1"},
        {
            "title": "News 2",
            "link": "https://news.com/2",
            "source": {"@url": "https://source.com"},
        },
    ]

    with patch(
        "fast_api.main.get_news_from_feed", return_value=feed_with_no_source_url
    ):
        response = client.get("/items")
        assert response.status_code == 200
        assert response.json()[0]["source_url"] is None
        assert response.json()[1]["source_url"] == "https://source.com"


def test_get_items_with_urls_empty_feed():
    # Teste de sucesso: Verificar o comportamento quando o feed RSS está vazio
    empty_feed = []
    with patch("fast_api.main.get_news_from_feed", return_value=empty_feed):
        response = client.get("/items")
        assert response.status_code == 200
        assert response.json() == []
