from fastapi.testclient import TestClient
from spotipy.oauth2 import SpotifyOAuth
from unittest.mock import Mock
from main import get_spotify_oauth

from main import app

client = TestClient(app, follow_redirects=False)


def test_login():
    mock_auth_manager = Mock(spec=SpotifyOAuth)
    expected_url = (
        mock_auth_manager.get_authorize_url.return_value
    ) = "http://example.com"
    app.dependency_overrides[get_spotify_oauth] = lambda: mock_auth_manager

    response = client.get("/login")
    assert response.status_code == 307
    assert response.headers["location"] == expected_url


def test_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
