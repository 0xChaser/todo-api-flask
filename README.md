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

# Lancer un conteneur (volume nommé = persistance de la base)
docker run -p 5000:5000 -v todo-data:/app/data todo-api
```

La base est stockée dans `/app/data/todos.db` (variable `DB_PATH`). On monte un
**volume nommé** sur le dossier `/app/data` : ce dossier est créé et possédé par
l'utilisateur non-root `appuser` dans l'image, ce qui évite les erreurs de droits
(`unable to open database file`) liées au montage d'un simple fichier.

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
## Pousser l'image sur DockerHub

```bash
# Se connecter à DockerHub
docker login

# Construire l'image avec deux tags
docker build -t 0xchaser/todo-api:latest -t 0xchaser/todo-api:v1.0.0 .

# Pousser les deux tags
docker push 0xchaser/todo-api:latest
docker push 0xchaser/todo-api:v1.0.0
```

Repository DockerHub : https://hub.docker.com/r/0xchaser/todo-api

## Déploiement

### Docker

```bash
docker run -d -p 80:5000 -v todo-data:/app/data 0xchaser/todo-api:latest
# Application accessible sur http://localhost/todos
```

### Docker Compose

Le fichier `docker-compose.yml` décrit le service, le volume nommé et le mapping
de port (`80:5000`).

```bash
docker compose up -d
docker compose ps
docker compose logs -f
docker compose down
```

Application accessible sur http://localhost/todos.

## Bonnes pratiques suivies

- **Tagging** : image taguée `latest` (dernière version) **et** `v1.0.0`
  (version figée), pour garantir des déploiements reproductibles.
- **Sécurité** :
  - image de base légère `python:3.11-slim` (surface d'attaque réduite) ;
  - exécution en utilisateur **non-root** (`appuser`) ;
  - scan des vulnérabilités avec **Trivy** + génération d'un **SBOM** (SPDX & CycloneDX) ;
  - aucun secret dans l'image ; `todos.db` exclu du dépôt (`.gitignore`).
- **Cache de build** : `requirements.txt` copié avant le code source pour
  réutiliser la couche d'installation des dépendances.
- **Persistance** : base de données dans un **volume nommé** (`todo-data`),
  indépendant du cycle de vie du conteneur.
- **Résilience** : `restart: unless-stopped` pour redémarrer automatiquement le
  conteneur en cas d'arrêt inattendu.