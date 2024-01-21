import spotipy
import secrets
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from session_cache_handler import SessionCacheHandler


load_dotenv('.env')
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
CLIENT_ID = os.environ.get("CLIENT_ID")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

app = FastAPI() # FastAPI instance
# Middlewares
app.add_middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(32))
# For more info on CORS: https://fastapi.tiangolo.com/tutorial/cors/?h=cors
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index(request: Request):
    # Get spotify token info from session
    spotify_token_info = request.session.get("spotify_token_info")
    # Get the SpotifyOAuth object
    auth_manager = _get_spotify_oauth(request)
    # Check if token is valid
    if auth_manager.validate_token(spotify_token_info):
        # Use access token to create Spotify client
        spotify_client = spotipy.Spotify(auth=spotify_token_info['access_token'])

        # Example: Fetch user profile data
        user_data = spotify_client.me()
        return user_data

    return {"Hello": "World"}

@app.get("/login")
def login(request: Request):
    auth_manager = _get_spotify_oauth(request)
    return RedirectResponse(auth_manager.get_authorize_url())

@app.get("/callback")
async def callback(request: Request):
    # Authorization code that spotify sends back https://developer.spotify.com/documentation/web-api/tutorials/code-flow
    code = request.query_params.get('code')
    if not code:
        return {"Error": "No code provided"}

    # Get the SpotifyOAuth object
    auth_manager = _get_spotify_oauth(request)
    # Exchange code for an access token
    token_info = auth_manager.get_access_token(code)
    
    if not token_info:
        return {"Error": "Could not retrieve token"}
    
    # Finally redirect to the index page
    return RedirectResponse("/")

# Healthcheck endpoint to make sure the server is running
@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

# Convenience function to get the SpotifyOAuth object
def _get_spotify_oauth(request: Request):
    return SpotifyOAuth(
        scope='user-library-modify',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        cache_handler=SessionCacheHandler(request.session)
    )