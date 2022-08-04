# syntax=docker/dockerfile:1
FROM python:3-alpine
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT [ "python3", "main.py" ]
