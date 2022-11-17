# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

# copy requirements.txt
COPY requirements.txt .

# Install requirements
RUN pip install -r requirements.txt

# Set working directory
WORKDIR /src

# copy project
COPY src/ .

ENTRYPOINT ["python", "main.py"]
