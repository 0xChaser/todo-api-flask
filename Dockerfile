# Utiliser une image de base légère
FROM python:3.11-slim

# Variables d'environnement (pas de .pyc, logs non bufferisés)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /app

# Créer un utilisateur non-root
RUN useradd -m appuser && chown -R appuser /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
