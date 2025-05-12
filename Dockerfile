FROM python:3.11-slim-bullseye AS requirements-stage

WORKDIR /tmp

RUN pip install poetry==1.8

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./scripts /code/scripts

ENV MODULE_NAME="app.api.app"
ENV VARIABLE_NAME="app"
ENV WORKERS_PER_CORE=2
ENV PORT=8000
