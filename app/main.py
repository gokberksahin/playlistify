import secrets
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from session_cache_handler import SessionCacheHandler
from fastapi.templating import Jinja2Templates
from typing import Annotated

# Jinja2 template engine
templates = Jinja2Templates(directory="templates")


load_dotenv("../.env")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
CLIENT_ID = os.environ.get("CLIENT_ID")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

app = FastAPI()  # FastAPI instance
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


# Dependencies
def get_spotify_oauth(request: Request):
    return SpotifyOAuth(
        scope="user-library-modify",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        cache_handler=SessionCacheHandler(request.session),
    )


@app.get("/")
def index(
    auth_manager: Annotated[SpotifyOAuth, Depends(get_spotify_oauth)], request: Request
):
    # Check if we have a cached token
    is_authenticated = bool(auth_manager.get_cached_token())
    # Render index.html template
    return templates.TemplateResponse(
        "index.html", {"request": request, "is_authenticated": is_authenticated}
    )


@app.get("/login")
def login(auth_manager: Annotated[SpotifyOAuth, Depends(get_spotify_oauth)]):
    return RedirectResponse(auth_manager.get_authorize_url())


@app.get("/callback")
async def callback(
    auth_manager: Annotated[SpotifyOAuth, Depends(get_spotify_oauth)], request: Request
):
    # Authorization code that spotify sends back https://developer.spotify.com/documentation/web-api/tutorials/code-flow
    code = request.query_params.get("code")
    if not code:
        return {"Error": "No code provided"}

    # Exchange code for an access token
    token_info = auth_manager.get_access_token(code)

    if not token_info:
        return {"Error": "Could not retrieve token"}

    # Finally redirect to the index page
    return RedirectResponse("/")


@app.post("/playlist")
def playlist(sentence: str = Form(...)):
    return {"status": "ok"}


# Healthcheck endpoint to make sure the server is running
@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}