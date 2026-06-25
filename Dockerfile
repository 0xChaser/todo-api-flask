# Utiliser une image de base légère
FROM python:3.11-slim

# Variables d'environnement (pas de .pyc, logs non bufferisés)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /app

RUN useradd -m appuser && mkdir -p /app/data && chown -R appuser /app

ENV DB_PATH=/app/data/todos.db

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
