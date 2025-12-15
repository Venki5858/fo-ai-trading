FROM python:3.11-slim

WORKDIR /app

COPY src/ ./src
WORKDIR /app/src

RUN pip install fastapi uvicorn pandas

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
