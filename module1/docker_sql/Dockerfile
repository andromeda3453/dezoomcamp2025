FROM python:3.13.1

RUN apt-get update && apt-get install -y wget libpq-dev gcc

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ingest_data.py .

ENTRYPOINT ["python", "ingest_data.py"]