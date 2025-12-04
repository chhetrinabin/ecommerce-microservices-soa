FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /reviews
COPY requirements.txt /reviews/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ /reviews/src
COPY tests/ /reviews/tests
RUN mkdir -p /data
ENV PORT=5004
ENV DB_PATH=/data/reviews_service.db
EXPOSE 5004
CMD ["python", "src/app.py"]