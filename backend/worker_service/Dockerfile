FROM python:3.12-slim


WORKDIR /app

# Instalar dependencias de sistema (para psycopg2, PIL, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean

# Copiar requirements del worker
COPY ../requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del worker
COPY ./worker_service/worker ./worker

# Establecer entrypoint para iniciar Kafka consumer
CMD ["python", "-m", "worker.main"]
