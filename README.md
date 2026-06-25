# Todo API Flask

API REST de gestion de tâches (Todo) développée avec Flask et SQLite.

## Installation et lancement

```bash
cd todo-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python app.py
```

L'application crée automatiquement la base SQLite (`todos.db`) et est accessible
sur http://localhost:5000/todos.

## Exécuter les tests

```bash
pytest test_app.py -v
```

## Endpoints de l'API

| Méthode | URL           | Description                       |
|---------|---------------|-----------------------------------|
| GET     | `/todos`      | Récupère toutes les tâches        |
| POST    | `/todos`      | Crée une tâche (champ `title` requis) |
| GET     | `/todos/<id>` | Récupère une tâche par son ID     |
| PUT     | `/todos/<id>` | Met à jour une tâche              |
| DELETE  | `/todos/<id>` | Supprime une tâche                |

## Construire et lancer l'image Docker

```bash
# Construire l'image
docker build -t todo-api .

# Lancer un conteneur (le volume persiste la base sur l'hôte)
docker run -p 5000:5000 -v $(pwd)/todos.db:/app/todos.db todo-api
```

## Scanner l'image avec Trivy

```bash
# Scan des vulnérabilités (console)
trivy image todo-api

# Rapport JSON
trivy image --format json --output trivy-report.json todo-api

# Rapport texte
trivy image --format table --output trivy-report.txt todo-api
```

## Générer le SBOM

```bash
# Format SPDX
trivy image --format spdx-json --output sbom.spdx.json todo-api

# Format CycloneDX
trivy image --format cyclonedx --output sbom.cdx.json todo-api

# Inspecter le contenu
cat sbom.spdx.json | jq .
```
