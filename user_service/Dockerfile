FROM python:3.11-slim

LABEL org.opencontainers.image.title="user-service"
LABEL org.opencontainers.image.source="https://github.com/chhetrinabin/ecommerce-microservices-soa"

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PORT=5002 \
	DB_PATH=/data/user_service.db

WORKDIR /src

# system deps (kept minimal). Uncomment build-essential if you need to compile wheels.
RUN set -eux; \
	apt-get update && apt-get install -y --no-install-recommends \
		ca-certificates \
	&& rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt /src/requirements.txt

# Install python deps (also install gunicorn for production WSGI serving)
RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt \
	&& pip install --no-cache-dir gunicorn

# Copy application source
COPY src/* /src/

# Create data directory and a non-root user
RUN mkdir -p /data \
	&& groupadd --gid 1000 appgroup || true \
	&& useradd --uid 1000 --gid appgroup --create-home --home-dir /home/appuser appuser || true \
	&& chown -R appuser:appgroup / /data

USER appuser

EXPOSE 5002

# Use gunicorn and the application factory to serve the Flask app in production.
# The app factory is `create_app()` in `src/app.py` so we call it to get the WSGI app.
CMD ["gunicorn", "'src.app:create_app()'", "-b", "0.0.0.0:5002", "--workers", "2", "--threads", "4"]

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://127.0.0.1:5002/health || exit 1
