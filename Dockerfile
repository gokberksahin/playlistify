FROM python:3.9

WORKDIR /playlistify

# Requirements
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Install Node.js
RUN apt update && apt install -y nodejs npm

# Copy the fastapi app
COPY . /playlistify

# Install npm dependencies
RUN npm install -D tailwindcss daisyui@latest
# Compile and minify tailwind for production
RUN npx tailwindcss -i ./app/static/css/index.css -o ./app/static/css/tailwind.css --minify

WORKDIR /playlistify/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]