FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ /app/
RUN mkdir -p /data
ENV PORT=5001
ENV DB_PATH=/data/product_service.db
EXPOSE 5001
CMD ["python", "app.py"]
