FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
#COPY core/ ./core/

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5001"]
