ARG UV_IMAGE=ghcr.io/astral-sh/uv
ARG VERSION_UV=0.12.0
ARG BASE_IMAGE=python:3.13-slim

FROM ${UV_IMAGE}:${VERSION_UV} AS uv
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
  # Recreate uv.lock and install dependencies: uv sync
  # Install dependencies from an existing uv.lock: uv sync --frozen
  # uv sync --frozen --no-cache --no-dev --no-install-project
  uv export --no-hashes --no-emit-project --frozen --no-group dev \
    --prune plotly --prune matplotlib --prune graphviz --prune scipy \
    -o /tmp/requirements.txt --no-cache-dir && \
  uv pip install --no-cache-dir --system -r /tmp/requirements.txt --no-deps && \
  rm -rf /usr/local/share/jupyter && \
  rm /tmp/requirements.txt

# create user if not exists
RUN addgroup --system app && \
    adduser --system app --ingroup app || true
USER app
COPY --chown=app:app src /
COPY --chown=app:app docker/log_config.json /log_config.json

EXPOSE 8000
ENV PROMETHEUS_MULTIPROC_DIR="/dev/shm"
CMD ["uvicorn", "fastapi_ml_example.main:app", "--host=0.0.0.0", "--port=8000", "--workers=4", "--log-config=log_config.json"]
