import spotipy
from dataclasses import dataclass


@dataclass
class Playlist:
    name: str
    description: str
    id: str


class Playlistify:
    def __init__(
        self,
        spotify_client: spotipy.Spotify,
        playlist_name: str,
        playlist_description: str,
    ):
        self.playlist_name = playlist_name
        self.playlist_description = playlist_description
        self.client = spotify_client

    def create_playlist(self, sentence: str) -> Playlist:
        pass
