import spotipy
from dataclasses import dataclass


@dataclass
class Playlist:
    name: str
    description: str
    id: str
    uri: str


@dataclass
class Track:
    uri: str
    name: str


class Playlistify:
    def __init__(
        self,
        user_id: str,
        spotify_client: spotipy.Spotify,
        playlist_name: str,
        playlist_description: str,
    ):
        self.playlist_name = playlist_name
        self.playlist_description = playlist_description
        self.client = spotify_client
        self.user_id = user_id

    def _parse_sentence(self, sentence: str) -> list[str]:
        # Trim leading and trailing spaces
        sentence = sentence.strip()
        # Split the sentence into words by spaces
        words = sentence.split()
        # Remove any empty words
        return [word for word in words if word]

    def _get_tracks_from_sentence(self, sentence: str) -> list[Track]:
        tracks: Track = []
        words = self._parse_sentence(sentence)
        for word in words:
            # Search for the word in Spotify
            items = self.client.search(word, limit=50)["tracks"]["items"]
            items += self.client.search(word, limit=50, offset=50)["tracks"]["items"]
            items += self.client.search(word, limit=50, offset=100)["tracks"]["items"]
            # If there is any track that starts with word append it to list of tracks
            for track in items:
                track_words = self._parse_sentence(track["name"])
                if track_words[0].lower() == word.lower():
                    tracks.append(Track(uri=track["uri"], name=track["name"]))
                    break
            else:
                raise Exception(f"Could not find any track that starts with {word}")

        return tracks

    def create_playlist(self, sentence: str) -> Playlist:
        # Get a list of tracks from the sentence
        tracks: list[Track] = self._get_tracks_from_sentence(sentence)
        # Create a playlist and add the first 5 songs from the search result
        playlist = self.client.user_playlist_create(
            user=self.user_id,
            name=self.playlist_name,
            description=self.playlist_description,
        )
        self.client.playlist_add_items(
            playlist_id=playlist["id"],
            items=[track.uri for track in tracks],
        )
        return Playlist(
            name=playlist["name"],
            description=playlist["description"],
            id=playlist["id"],
            uri=playlist["uri"],
        )
