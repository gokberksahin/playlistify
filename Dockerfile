FROM python:3.9

WORKDIR /code

# Requirements
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the fastapi app
COPY ./app /code/app

# Compile and minify tailwind for production
RUN curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
RUN chmod +x ./tailwindcss-linux-x64
RUN mv ./tailwindcss-linux-x64 ./tailwindcss
RUN ./tailwindcss -i /code/app/static/css/input.css -o /code/app/static/css/tailwind.css -c /code/app/tailwind.config.js --minify

WORKDIR /code/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]