# Choose Python 3.12 to satisfy pyproject constraint (^3.12)
ARG PYTHON_IMAGE=python:3.12-slim
FROM ${PYTHON_IMAGE} AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONPATH=/app

WORKDIR /app

# Build deps for common wheels (adjust to your needs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    git \
    pkg-config \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Poetry
ARG POETRY_VERSION=1.7.1
RUN pip install "poetry==${POETRY_VERSION}"

# Copy only dependency manifests first for better caching
COPY pyproject.toml poetry.lock* ./

# Poetry ≥1.6: --only main replaces --no-dev
# --no-root if your app isn't installed as a package (src/ layout + uvicorn entry)
RUN poetry install --only main --no-interaction --no-ansi --no-root

# Copy app code
COPY src/ ./src/
COPY .env .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -fsS http://localhost:8000/v1/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
