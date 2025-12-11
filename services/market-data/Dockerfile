FROM python:3.11-slim
WORKDIR /app
COPY src/ .
RUN pip install fastapi uvicorn pandas
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
