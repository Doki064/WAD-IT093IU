# syntax=docker/dockerfile:1.2
###############################################
# Base Image
###############################################
FROM python:3.8-slim as python-base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYSETUP_PATH="/opt/pysetup"
ENV VENV_PATH="/opt/pysetup/.venv"

###############################################
# Builder Image
###############################################
FROM python-base as builder-base

ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV POETRY_VERSION=1.1.6
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential

# install poetry - respects $POETRY_VERSION
RUN pip install "poetry==$POETRY_VERSION"

# Copy project requirement files here to ensure they will be cached
WORKDIR $PYSETUP_PATH
COPY pyproject.toml poetry.lock ./

# Install runtime dependencies
RUN poetry install --no-root --no-dev --no-ansi

###############################################
# Production Image
###############################################
FROM python-base as production

# prepend virtualenv to path
ENV PATH="$VENV_PATH/bin:$PATH"
ENV PYTHONPATH="$VENV_PATH/lib/python3.8/site-packages:$PYTHONPATH"

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY . /app/frontend

CMD [ "streamlit", "run", "main.py" ]
