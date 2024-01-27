import spotipy
from playlistfy import Playlistify, Playlist, Track
from unittest.mock import Mock
import pytest


@pytest.fixture
def input_sentence():
    return "lorem ipsum dolor sit amet consectetur adipiscing elit"


@pytest.fixture
def mock_client():
    mock_client = Mock(spec=spotipy.Spotify)
    mock_client.user_playlist_create.return_value = {
        "name": "test_playlist",
        "description": "test_descirption",
        "id": "id",
        "uri": "uri",
    }
    mock_client.playlist_add_items.return_value = None
    return mock_client


def test_create_playlist_happy_path(input_sentence, mock_client):
    """Test the happy path where all search queries return a track"""

    track1_name = "lorem ipsum dolor sit amet"
    track2_name = "consectetur adipiscing elit"
    expected_tracks = [
        Track(name=track1_name, uri=f"uri_{track1_name}"),
        Track(name=track2_name, uri=f"uri_{track2_name}"),
    ]

    # Assume spotify track search will return a song that matches the word every time
    def search_side_effect(word, limit=50):
        return {"tracks": {"items": [{"name": word, "uri": f"uri_{word}"}]}}

    mock_client.search.side_effect = search_side_effect

    playlistify = Playlistify(
        "test_user", mock_client, "test_playlist", "test_descirption"
    )
    playlist = playlistify.create_playlist(input_sentence)
    assert playlist == Playlist(
        name="test_playlist",
        description="test_descirption",
        id="id",
        uri="uri",
        tracks=expected_tracks,
    )


def test_create_playlisy_sadge_path(input_sentence, mock_client):
    """Test the sadge path where it's impossible to create playlist for sentence"""

    def search_side_effect(word, limit=50):
        return {"tracks": {"items": []}}

    mock_client.search.side_effect = search_side_effect

    with pytest.raises(ValueError):
        playlistify = Playlistify(
            "test_user", mock_client, "test_playlist", "test_descirption"
        )
        playlistify.create_playlist("lorem ipsum dolor sit amet consectetur")
