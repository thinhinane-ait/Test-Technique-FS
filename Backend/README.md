# Backend — API FastAPI

API de gestion des antennes et des interventions, développée avec FastAPI et connectée à une base de données PostgreSQL.

## Technologies

- Langage : Python 3.11+ 
- Framework : FastAPI
- SQLAlchemy
- Base de donnée: PostgreSQL
- Psycopg
- Alembic
- Pydantic
- Pytest
- Docker et Docker Compose

La liste complète des dépendances se trouve dans [`requirements.txt`](./requirements.txt).

## Prérequis

- Python 3
- `pip`
- Docker Desktop
- Docker Compose

## Installation

Depuis la racine du projet, se placer dans le dossier du backend :

```bash
cd Backend
```

Créer l’environnement virtuel :

```bash
python -m venv env
```

### Activer l’environnement virtuel

Sous Linux ou macOS :

```bash
source env/bin/activate
```

Sous Windows avec PowerShell :

```powershell
env\Scripts\Activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Variables d’environnement

Créer un fichier `.env` à la racine du projet :

```env
DATABASE_URL=database_url
API_KEY=your_api_key
```

Adapter le nom `API_KEY` et `DATABASE_URL` au noms réellement utilisés dans la configuration de l’application.

Le fichier `.env` contient des informations sensibles et ne doit pas être envoyé sur Git.

## Base de données PostgreSQL

Le fichier `docker-compose.yml` se trouve à la racine du projet.

Créer un fichier `.env` à la racine du projet :

```env
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name
```


Depuis la racine, lancer PostgreSQL :

```bash
docker compose up -d
```

Vérifier l’état du conteneur :

```bash
docker compose ps
```

Le conteneur PostgreSQL doit avoir le statut `healthy`.

Pour arrêter PostgreSQL :

```bash
docker compose down
```

## Migrations

Depuis le dossier `Backend`, avec l’environnement virtuel activé, appliquer les migrations :

```bash
alembic upgrade head
```

Vérifier la migration actuelle :

```bash
alembic current
```

## Lancement de l’API

Depuis le dossier `Backend` :

```bash
uvicorn app.main:app --reload
```

L’API est accessible à l’adresse suivante :

http://127.0.0.1:8000

## Documentation

FastAPI génère automatiquement une documentation interactive :

- Swagger UI : http://127.0.0.1:8000/docs
- OpenAPI JSON : http://127.0.0.1:8000/openapi.json

## Démarrage rapide

Depuis la racine du projet :

```bash
docker compose up -d
```

Puis :

```bash
cd Backend
source env/bin/activate
alembic upgrade head
uvicorn app.main:app --reload
```

## API

### Authentification

Les routes liées aux interventions nécessitent une clé API.

La clé doit être envoyée dans l’en-tête HTTP suivant :

```http
X-API-Key: your_api_key
```

La valeur réelle de la clé doit être définie dans le fichier `.env` et ne doit pas être publiée sur Git.

## Antennas

### Récupérer les antennes

```http
GET /api/v1/antennas
```

Retourne la liste des antennes avec leur dernière intervention, lorsqu’elle existe.

### Paramètres de requête

| Paramètre | Type | Obligatoire | Valeur par défaut | Description |
|---|---|---:|---:|---|
| `limit` | entier | Non | `10` | Nombre d’antennes retournées, entre 1 et 100 |
| `offset` | entier | Non | `0` | Nombre d’antennes à ignorer |
| `city` | chaîne | Non | — | Filtre les antennes par ville |
| `status` | chaîne | Non | — | Filtre les antennes par statut |

### Exemple

```http
GET /v1/antenna?city=Paris&limit=10&offset=0
```

Avec `curl` :

```bash
curl "http://127.0.0.1:8000/api/v1/antennas?city=Paris&limit=10&offset=0"
```

### Réponse réussie

Code HTTP : `200 OK`

```json
[
  {
    "id": 1,
    "name": "Antenne Paris Centre",
    "city": "Paris",
    "status": "UP",
    "created_at": "2026-07-24T14:00:00Z",
    "latest_intervention": null
  }
]
```

Si aucune antenne ne correspond aux critères, l’API retourne une liste vide :

```json
[]
```

## Interventions

### Créer une intervention

```http
POST /api/v1/interventions
```

Crée une intervention pour une antenne existante.

Lors de la création :

- une seule intervention active est autorisée par antenne ;
- le statut de l’antenne passe à `DOWN`.

Cette route nécessite une clé API.

### Corps de la requête

```json
{
  "antenna_id": 1,
  "description": "Panne du réseau principal",
  "technician_identity": "Technicien 1",
  "priority": "HIGH"
}
```

### Réponse réussie

Code HTTP : `200 OK`

```json
{
  "antenna_id": 1,
  "description": "Panne du réseau principal",
  "technician_identity": "Technicien 1",
  "priority": "HIGH",
  "id": 1,
  "created_at": "2026-07-24T15:00:00Z",
  "ended_at": null
}
```

### Erreurs possibles

| Code | Description |
|---|---|
| `401` ou `403` | Clé d'autorisation est invalide |
| `404` | L’antenne n’existe pas |
| `409` | Une intervention est déjà en cours |

### Clôturer une intervention

```http
PATCH /api/v1/interventions/{intervention_id}/close
```

Clôture une intervention active et fait passer le statut de l’antenne à `UP`.

Cette route nécessite une clé API.

### Exemple

```http
PATCH /api/v1/interventions/{intervention_id}/close
```

### Réponse réussie

Code HTTP : `200 OK`

```json
{
  "antenna_id": 1,
  "description": "Panne du réseau principal",
  "technician_identity": "Technicien 1",
  "priority": "HIGH",
  "id": 1,
  "created_at": "2026-07-24T15:00:00Z",
  "ended_at": "2026-07-24T16:00:00Z"
}
```

### Erreurs possibles

| Code | Description |
|---|---|
| `401` ou `403` | Clé d'autorisation est invalide |
| `404` | Aucune intervention en cours |
| `409` | L’intervention est déjà clôturée |

## Tests

## Lancement des tests

Placez-vous dans le dossier du backend :

Lancez tous les tests :

```bash
pytest -v
```

Pour afficher un résultat plus court :

```bash
pytest -q
```

Les tests vérifient notamment :

- la validation des données d’une antenne ;
- la récupération de la liste des antennes ;
- le filtrage des antennes par ville et par statut ;
- la création d’une intervention ;
- l’interdiction de créer deux interventions actives pour une même antenne ;
- le refus d’une requête sans clé API ;
- la clôture d’une intervention.

Résultat attendu :

```text
10 passed
```