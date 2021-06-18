# WAD-IT093IU

Web App Development course project (IT093IU) at IU-VNUHCMC.

## Prerequisites

- Linux-based platforms or Windows Subsystem for Linux (WSL)
- [Docker Compose](https://docs.docker.com/compose/install/) is installed

## Build

- `sh ./build.sh`

## Run

- `docker-compose up`

## Open app on the browser

- Streamit: http://localhost
- FastAPI: http://localhost:8080/docs
- pgAdmin4: http://localhost:5050

> admin is the default username and password for Streamlit

## Dependencies

#### Backend

- <a href="https://github.com/tiangolo/fastapi" target="_blank"><code>fastapi</code></a> - web framework for building APIs
- <a href="https://github.com/sqlalchemy/sqlalchemy" target="_blank"><code>sqlalchemy</code></a> - database toolkit
- <a href="https://github.com/sqlalchemy/alembic" target="_blank"><code>alembic</code></a> - database migrations tool for SQLAlchemy
- <a href="https://github.com/MagicStack/asyncpg" target="_blank"><code>asyncpg</code></a> - driver for asynchronous PostgreSQL
- <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - faster JSON Response
- <a href="https://github.com/mpdavis/python-jose" target="_blank"><code>python-jose</code></a> - for JSON Web Token
- <a href="https://github.com/efficks/passlib" target="_blank"><code>passlib</code></a> - for password hashing

#### Frontend

- <a href="https://github.com/streamlit/streamlit" target="_blank"><code>fastapi</code></a> - user interface
- <a href="https://github.com/pandas-profiling/pandas-profiling" target="_blank"><code>pandas-profiling</code></a> - create reports for pandas Dataframe
- <a href="https://github.com/plotly/plotly.py" target="_blank"><code>plotly</code></a> - create interactive graph
- <a href="https://github.com/encode/httpx" target="_blank"><code>httpx</code></a> - HTTP client for Python 3
