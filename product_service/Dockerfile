FROM python:3.11-slim

LABEL org.opencontainers.image.title="product-service"
LABEL org.opencontainers.image.source="https://github.com/chhetrinabin/ecommerce-microservices-soa"

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PORT=5001 \
	DB_PATH=/data/product_service.db

WORKDIR /src

RUN set -eux; \
	apt-get update && apt-get install -y --no-install-recommends \
		ca-certificates \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt \
	&& pip install --no-cache-dir gunicorn

COPY src/ /src/

RUN mkdir -p /data \
	&& groupadd --gid 1000 appgroup || true \
	&& useradd --uid 1000 --gid appgroup --create-home --home-dir /home/appuser appuser || true \
	&& chown -R appuser:appgroup /src /data

USER appuser

EXPOSE 5001

CMD ["gunicorn", "src.app:create_app()", "-b", "0.0.0.0:5001", "--workers", "2", "--threads", "4"]

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://127.0.0.1:5001/health || exit 1
