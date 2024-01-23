import spotipy
from playlistfy import Playlistify, Playlist
from unittest.mock import Mock


def test_create_playlist():
    mock_client = Mock(spec=spotipy.Spotify)
    mock_client.search.return_value = {
        "tracks": {
            "items": [
                {
                    "name": "song1",
                    "artists": [{"name": "artist1"}],
                    "uri": "uri1",
                },
                {
                    "name": "song2",
                    "artists": [{"name": "artist2"}],
                    "uri": "uri2",
                },
                {
                    "name": "song3",
                    "artists": [{"name": "artist3"}],
                    "uri": "uri3",
                },
                {
                    "name": "song4",
                    "artists": [{"name": "artist4"}],
                    "uri": "uri4",
                },
                {
                    "name": "song5",
                    "artists": [{"name": "artist5"}],
                    "uri": "uri5",
                },
            ]
        }
    }
    mock_client.user_playlist_create.return_value = {
        "name": "test_playlist",
        "description": "test_descirption",
        "id": "id",
        "uri": "uri",
    }
    mock_client.playlist_add_items.return_value = None

    playlistify = Playlistify(
        "test_user", mock_client, "test_playlist", "test_descirption"
    )
    playlist = playlistify.create_playlist("song1 song2 song3")
    assert playlist == Playlist(
        name="test_playlist",
        description="test_descirption",
        id="id",
        uri="uri",
    )
