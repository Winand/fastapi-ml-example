ARG UV_IMAGE=ghcr.io/astral-sh/uv:0.12.0
ARG BASE_IMAGE=python:3.13-slim

FROM ${UV_IMAGE} AS uv
COPY pyproject.toml uv.lock /

FROM ${BASE_IMAGE}
ARG PYPI_MIRROR=https://pypi.org
ENV UV_DEFAULT_INDEX=${PYPI_MIRROR}/simple
# https://docs.astral.sh/uv/configuration/authentication/#custom-ca-certificates
# ENV UV_INSECURE_HOST=${PYPI_MIRROR}
ENV UV_SYSTEM_CERTS=1
# https://docs.astral.sh/uv/concepts/python-versions/#disabling-automatic-python-downloads
ENV UV_PYTHON_DOWNLOADS=never
# for uv sync https://docs.astral.sh/uv/concepts/projects/config/#project-environment-path
# ENV UV_PROJECT_ENVIRONMENT=/usr/local

WORKDIR /
USER root
RUN --mount=from=uv,source=/uv,target=/bin/uv \
    --mount=from=uv,source=/pyproject.toml,target=/pyproject.toml \
    --mount=from=uv,source=/uv.lock,target=/uv.lock \
    --mount=type=cache,target=/root/.cache/uv \
  # Recreate uv.lock and install dependencies: uv sync
  # Install dependencies from an existing uv.lock: uv sync --frozen
  # uv sync --frozen --no-cache --no-dev --no-install-project
  uv export --no-hashes --no-emit-project --frozen --no-group dev \
    --prune plotly --prune matplotlib --prune graphviz --prune scipy \
    -o /tmp/requirements.txt && \
  uv pip install --link-mode=copy --system -r /tmp/requirements.txt --no-deps && \
  rm -rf /usr/local/share/jupyter && \
  rm /tmp/requirements.txt

# wget is required for health check (Debian, Fedora)
# NOTE: Almalinux/Rockylinux have curl preinstalled, BusyBox has wget built-in
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    --mount=type=cache,target=/var/cache/dnf,sharing=locked \
    command -v wget >/dev/null || \
    if command -v apt >/dev/null; then \
        apt update && apt install --no-install-recommends -y wget; \
    elif command -v dnf >/dev/null; then \
        dnf install -y wget; \
    else echo "WARNING: could not find apt or dnf to install wget" >&2; \
    fi
# create user if not exists (Debian, BusyBox, Fedora)
RUN addgroup --system app && adduser --system app --ingroup app || \
    useradd --system app || :

USER app
COPY --chown=app:app src /
COPY --chown=app:app docker/log_config.json /log_config.json

EXPOSE 8000
ENV PROMETHEUS_MULTIPROC_DIR="/dev/shm"
# https://docs.docker.com/reference/dockerfile/#healthcheck
# https://web.archive.org/web/20230706205635/https://docs.docker.com/engine/reference/builder/
HEALTHCHECK \
    # time between checks (1st is after `interval` seconds; default 30s)
    --interval=15s \
    # check command timeout (default 30s)
    --timeout=3s \
    # --retries=3 -- after N retries service is marked as unhealthy (default 3)
    # --start-period=5s -- maximum container bootstrap time (default 0)
    # --start-interval=5s -- time between checks during the start period (Docker 25+; default 5s)
    CMD ["wget", "-qO-", "http://127.0.0.1:8000/health"]
CMD ["uvicorn", "fastapi_ml_example.main:app", "--host=0.0.0.0", "--port=8000", "--log-config=log_config.json"]
