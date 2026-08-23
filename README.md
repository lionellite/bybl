# Bybl

Bybl est une Bible française en ligne, avec une interface de lecture Django et une API REST construite avec Django REST Framework.

## Installation locale

Le projet cible Python 3.11 ou supérieur. Créez un environnement virtuel, installez les dépendances, appliquez les migrations puis chargez les données bibliques :

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # puis adaptez les valeurs si nécessaire
python manage.py migrate
python manage.py load_bible
python manage.py runserver
```

L’application est ensuite disponible à l’adresse <http://127.0.0.1:8000/>. Les fichiers statiques de production peuvent être préparés avec `python manage.py collectstatic --noinput`.

## Configuration

Les paramètres sensibles et dépendants de l’environnement sont définis par variables : `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS` et `DJANGO_CSRF_TRUSTED_ORIGINS`. En production, utilisez une clé secrète aléatoire, désactivez le mode debug et renseignez les hôtes autorisés.

La base SQLite est adaptée au développement et aux petits déploiements. Pour PostgreSQL, installez les dépendances du projet puis définissez `DJANGO_DB_ENGINE=postgresql`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST` et `POSTGRES_PORT`. La recherche plein texte utilise alors le dictionnaire français et un index GIN; SQLite conserve un fallback compatible pour le développement local.

## API

Les ressources REST sont exposées sous `/api/` :

| Ressource | URL |
| --- | --- |
| Liste des livres | `/api/books/` |
| Détail d’un livre | `/api/books/<id>/` |
| Chapitres d’un livre | `/api/books/<book_id>/chapters/` |
| Détail d’un chapitre | `/api/chapters/<id>/` |
| Versets d’un chapitre | `/api/chapters/<chapter_id>/verses/` |
| Détail d’un verset | `/api/verses/<id>/` |

Les endpoints de liste sont paginés. La taille par défaut est de 50 éléments et peut être modifiée dans `REST_FRAMEWORK`.

## Tests et vérifications

```bash
python manage.py check
python manage.py test
python manage.py check --deploy
python manage.py makemigrations --check --dry-run
```

La CI GitHub exécute ces contrôles sur Python 3.11 et 3.12 avec SQLite, ainsi que sur PostgreSQL 16. Le fichier `data/bible-fr.json` est la source d’import. La commande `load_bible` vérifie le nombre de livres, utilise les noms canoniques définis dans le code, reconstruit les chapitres et versets dans une transaction atomique, puis signale le bilan de l’import.

## Droits sur les données

Le statut de redistribution de la traduction `FRC97` n’est pas considéré comme établi par le dépôt. Consultez `DATA_LICENSE.md` avant toute diffusion publique, commerciale ou exposition durable par API; cette notice contient la provenance, les sources publiques et la procédure de demande d’autorisation.
