FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /users
COPY requirements.txt /users/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ /users/src
COPY tests/ /users/tests
RUN mkdir -p /data
ENV PORT=5002
ENV DB_PATH=/data/user_service.db
EXPOSE 5002
CMD ["python", "src/app.py"]