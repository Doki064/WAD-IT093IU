###############################################
# Base Image
###############################################
FROM python:3.8-slim as python-base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV POETRY_VERSION=1.1.6
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1
ENV PYSETUP_PATH="/opt/pysetup"
ENV VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    libpq-dev

###############################################
# Builder Image
###############################################
FROM python-base as builder-base

# Install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

# Copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY pyproject.toml poetry.lock ./

# Install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-root --no-dev

###############################################
# Production Image
###############################################
FROM python-base as production

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY . /app

EXPOSE 8080
