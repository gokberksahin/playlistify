# Playlistify
Turn your sentences to spotify playlists

## Development

### Dependencies
Make sure that you are in your virtual python env so you don't dump all packages you have install so far with pip.
```
pip freeze > requirements.txt  # update requirements
pip install -r requirements.txt  # install requirements
```

### How to create a virtual env and activate it?
```
python3 -m venv env
source env/bin/activate
```

### How to build and start the app?
First compile the `tailwind.css` using the standalone `tailwindcss` CLI tool:
```
./tailwindcss -i app/static/css/input.css -o app/static/css/tailwind.css --watch
```
This will make sure that any new tailwind class used in the templates will reflect to `tailwind.css`.

Then start the server:
```
uvicorn main:app --reload --host 0.0.0.0
```

