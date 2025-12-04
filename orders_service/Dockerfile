FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /orders
COPY requirements.txt /orders/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ /orders/src
COPY tests/ /orders/tests
RUN mkdir -p /data
ENV PORT=5003
ENV DB_PATH=/data/orders_service.db
EXPOSE 5003
CMD ["python", "src/app.py"]