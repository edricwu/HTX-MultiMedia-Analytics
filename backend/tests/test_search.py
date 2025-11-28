def test_search_text(client):
    response = client.get("/search", params={"q": "car"})

    assert response.status_code == 200