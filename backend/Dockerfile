FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio para media
RUN mkdir -p /app/media

# Exponer puerto
EXPOSE 8000

# Comando por defecto (puede ser sobrescrito en docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
