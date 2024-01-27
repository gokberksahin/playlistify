import spotipy
from dataclasses import dataclass
from thefuzz import fuzz
from typing import Optional


@dataclass
class Track:
    uri: str
    name: str


@dataclass
class Playlist:
    name: str
    description: str
    id: str
    uri: str
    tracks: list[Track]


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

    def _get_matching_track(self, word: str) -> Optional[Track]:
        for _ in range(4):
            # Search for the word in Spotify
            items = self.client.search(word, limit=50)["tracks"]["items"]
            # For each track compare the word with track name using the fuzz ratio
            for track in items:
                ratio = fuzz.ratio(word.lower(), track["name"].lower())
                # If the ratio is greater than 90% return the track
                if ratio >= 90:
                    return Track(uri=track["uri"], name=track["name"])

    def _backtrack(
        self,
        words: list[str],
        tracks: list[Track],
        start_idx: int,
        group_size: int = 5,
    ) -> bool:
        if start_idx >= len(words):
            return True
        for end_idx in range(
            min(len(words), start_idx + group_size) - 1, start_idx - 1, -1
        ):
            word = " ".join(words[start_idx : end_idx + 1])
            track = self._get_matching_track(word)
            if track:
                tracks.append(track)
                ok = self._backtrack(words, tracks, end_idx + 1)
                if ok:
                    return ok
                tracks.pop()
        return False

    def _get_tracks_from_sentence(self, sentence: str) -> list[Track]:
        tracks: list[Track] = []
        words = self._parse_sentence(sentence)
        ok = self._backtrack(words, tracks, 0)
        if not ok:
            raise ValueError("Could not create playlist for sentence")
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
            tracks=tracks,
        )
