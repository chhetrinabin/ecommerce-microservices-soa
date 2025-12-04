FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /products
COPY requirements.txt /products/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ /products/src
COPY tests/ /products/tests
RUN mkdir -p /data
ENV PORT=5001
ENV DB_PATH=/data/product_service.db
EXPOSE 5001
CMD ["python", "src/app.py"]