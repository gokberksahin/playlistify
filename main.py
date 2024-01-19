import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os


def main():
    load_dotenv('.env')
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    CLIENT_ID = os.environ.get("CLIENT_ID")
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET))

    results = sp.search(q='cramps', limit=20)
    for idx, track in enumerate(results['tracks']['items']):
        print(idx, track['name'])






if __name__ == '__main__':
    main()
   