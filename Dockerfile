FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir ollama langchain-community langchain-core
COPY . .
CMD ["python", "app.py"]
