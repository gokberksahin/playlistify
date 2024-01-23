# playlistify
Turn your sentences to spotify playlists

## How to update the requirements?
Make sure that you are in your virtual python env so you don't dump all packages you have install so far with pip.
```
pip freeze > requirements.txt
```

## How to create a virtual env and activate it?
```
python3 -m venv env
source env/bin/activate
```

## How to start the server?
```
uvicorn main:app --reload --host 0.0.0.0
```
