# README

New project generated from my cookiecutter template.

## Features

1. Logging via Loguru
3. Dockerfile to run the script in a container

## Usage

### Running locally

First run to setup virtualenv and run locally with debugging.

```bash
mkvenv
./main.py 10.1.1.1 --debug
```

### Run with Dockerfile

Build image and run

```bash
docker build -t ipdb .
docker run ipdb:latest 10.1.1.1 --debug
```
