FROM python:3.12-slim

WORKDIR /ClauVieira_Clin

ENV DEBIAN_FRONTEND=noninteractive
# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libcairo2 \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]