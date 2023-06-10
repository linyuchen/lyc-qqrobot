FROM arm64v8/python:3.11.4-slim
#FROM python:3.11.4-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://mirrors.cloud.tencent.com/pypi/simple -r requirements.txt

