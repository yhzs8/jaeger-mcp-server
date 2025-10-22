FROM python:3.12-slim

WORKDIR /app

COPY . /app

EXPOSE 8000

RUN pip install --no-cache-dir fastmcp requests

CMD ["python", "main.py"]