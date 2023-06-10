#FROM arm64v8/python:3.11.4-slim
FROM python:3.11.4-slim
LABEL authors="linyuchen"
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
