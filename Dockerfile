FROM python:3.12-slim

LABEL maintainer="amirhosein"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Create non-root user
RUN groupadd --gid 1000 django && \
    useradd --uid 1000 --gid 1000 --create-home --shell /usr/sbin/nologin django && \
    mkdir -p /usr/src/app/staticfiles && \
    chown -R 1000:1000 /usr/src/app

USER 1000:1000

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4"]


