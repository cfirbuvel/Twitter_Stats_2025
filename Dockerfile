FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for cryptography
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["/usr/local/bin/python3", "main.py"]
# Explicitly use python3