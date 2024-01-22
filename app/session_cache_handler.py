from spotipy import CacheHandler


class SessionCacheHandler(CacheHandler):
    def __init__(self, session):
        self.session = session

    def get_cached_token(self):
        return self.session.get("spotify_token_info")

    def save_token_to_cache(self, token_info):
        self.session["spotify_token_info"] = token_info
