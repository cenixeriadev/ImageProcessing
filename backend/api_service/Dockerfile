FROM python:3.12-slim

WORKDIR /app

# 1. Copiar requirements.txt primero para caché
COPY ../requirements.txt .

# 2. Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt


COPY ./api_service .

# 3. Crear usuario no privilegiado
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && chown -R appuser:appuser /app

# 4. Establecer PYTHONPATH y directorio de trabajo
ENV PYTHONPATH="${PYTHONPATH}:/app"
WORKDIR /app/app

# 5. Cambiar a usuario no privilegiado
USER appuser

# 6. Comando para ejecutar (igual a tu comando local)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]