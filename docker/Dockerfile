# ----------------------------------------------------------------------------
# Quant Agent Platform – base dev image
# ----------------------------------------------------------------------------
# - Based on slim Python image to minimize size (<500 MB)
# - Installs core Python dependencies (DuckDB, Polars, Qdrant client, httpx, etc.)
# - Creates non-root user `appuser` for security
# ----------------------------------------------------------------------------

FROM python:3.11-slim AS base

LABEL org.opencontainers.image.title="Quant Agent Platform" \
      org.opencontainers.image.description="Base image for multi-agent trading strategy sandbox" \
      org.opencontainers.image.licenses="MIT"

# ---------------------------------------------------------------------------
# 1. System deps – keep minimal, remove apt cache afterwards
# ---------------------------------------------------------------------------
RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        git \
        tzdata \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------
# 2. Create non-root user
# ---------------------------------------------------------------------------
ENV USER=appuser \
    UID=1000 \
    HOME=/home/$USER

RUN useradd --create-home --uid $UID --shell /bin/bash $USER

# ---------------------------------------------------------------------------
# 3. Python dependencies – pinned to recent stable versions
#    httpx chosen instead of requests for optional async + HTTP/2 support
# ---------------------------------------------------------------------------
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        duckdb==1.2.* \
        polars==1.29.* \
        qdrant-client==1.14.* \
        'httpx[http2]>=0.28,<1.0' \
        pydantic==2.*

# ---------------------------------------------------------------------------
# 4. Workdir & permissions
# ---------------------------------------------------------------------------
WORKDIR /app
RUN chown -R $USER:$USER /app
USER $USER

# ---------------------------------------------------------------------------
# 5. Default command – interactive Python shell; override in compose
# ---------------------------------------------------------------------------
CMD ["python", "-q"]
