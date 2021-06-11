###############################################
# Base Image
###############################################
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim as python-base

# Set environment variables
## For python and pip
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

## For PDM
ENV PYSETUP_PATH="/opt/pysetup"
ENV PACKAGE_PATH="/opt/pysetup/__pypackages__/3.8"

# prepend package to path
ENV PATH="$PACKAGE_PATH/bin:$PATH"
ENV PYTHONPATH="$PACKAGE_PATH/lib:$PYTHONPATH"

###############################################
# Builder Image
###############################################
FROM python-base as builder-base

# Install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN pip install pdm

# Copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY pyproject.toml pdm.lock ./

# Install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN pdm sync --clean

###############################################
# Production Image
###############################################
FROM python-base as production

## For image
ENV MODULE_NAME="server.main"
ENV PORT="8080"
ENV PRE_START_PATH="/app/server/prestart.sh"

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY . /app/server
