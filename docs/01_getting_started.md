# Getting Started

## Table of contents
* [Installation](#installation)
* [Configuration](#configuration)
* [Running](#running)

## Installation

Make sure that you have installed Poetry with Python 3.11.

Activate the virtual environment of Poetry:
```bash
poetry shell
```

To install dependencies of the project:

```bash
poetry install
```

## Configuration

You need to export environment variables to run devops-task project.
You can check the `.env.test` file for the required environment variables.

```bash
export $(cat .env.test | xargs)
```

## Running

For development, you can run the project with:

```bash
uvicorn run uvicorn app.api.app:app --reload --log-level debug
```

or

```bash
make run
```

### Development

If you don't want to install and use database that is in your local, you can use docker-compose.development.yml.

```bash
docker compose -f docker-compose.development.yml up -d
```
You can reach this db localhost:15432. Also, a docker volume is connected to this db to prevent data lose when container is down.

You can then access the API at <http://localhost:8000> and the [Swagger UI](https://swagger.io/tools/swagger-ui/) (interactive API documentation) at <http://localhost:8000/docs>.