#FROM arm64v8/python:3.11.4-slim
FROM python:3.11.4-slim
LABEL authors="linyuchen"
WORKDIR /app

COPY . /app

EXPOSE 8080
EXPOSE 5000

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "/app/client/mirai_http/main.py", "1577491075"]
