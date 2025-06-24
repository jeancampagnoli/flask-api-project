FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instala as versões exatas especificadas
RUN pip install --no-cache-dir -r requirements.txt && \
    pip freeze > installed_versions.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]