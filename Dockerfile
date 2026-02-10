# syntax=docker/dockerfile:1.7
FROM python:3.12-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

ARG APP_USER=appuser
ARG APP_UID=10001
ARG APP_GID=10001

RUN groupadd --gid ${APP_GID} ${APP_USER} \
    && useradd --uid ${APP_UID} --gid ${APP_GID} --create-home --shell /bin/bash ${APP_USER}

RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources \
    && printf '%s\n' \
       'Acquire::Retries "5";' \
       'Acquire::http::Timeout "30";' \
       'Acquire::https::Timeout "30";' \
       > /etc/apt/apt.conf.d/99network-retries

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libpq5 \
       libgdal-dev \
       gdal-bin \
       gettext \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

FROM base AS builder
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r /tmp/requirements.txt

FROM base AS runtime
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN mkdir -p /var/log/django /app/static /app/media \
    && chown -R ${APP_USER}:${APP_USER} /var/log/django /app

COPY --chown=${APP_USER}:${APP_USER} . /app
COPY --chown=${APP_USER}:${APP_USER} docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER ${APP_USER}
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-"]
