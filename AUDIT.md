# Audit technique et amélioration de Bybl

## Périmètre

L’audit a couvert la configuration Django, les modèles et migrations, les vues HTML, l’API REST, la commande d’import, les templates, les actifs statiques, les dépendances, la couverture de tests et les artefacts suivis par Git.

## Constats prioritaires

| Niveau | Constat | Impact | Correction |
| --- | --- | --- | --- |
| Critique | Plusieurs imports indispensables manquaient dans `bible/views.py`, `api/views.py` et `api/serializers.py`. | L’application et l’API ne pouvaient pas démarrer correctement. | Imports Django et DRF ajoutés, puis couverts par tests. |
| Élevé | `SECRET_KEY` était codée en dur, `DEBUG=True` et `ALLOWED_HOSTS` vide. | Risque de fuite de données et configuration inutilisable en production. | Configuration pilotée par variables d’environnement, protections HTTPS, cookies sécurisés et hôtes explicites. |
| Élevé | Le texte de recherche était rendu avec le filtre `safe`. | Une donnée non fiable pouvait produire une XSS persistante ou réfléchie. | Suppression de `safe` et test de non-régression dédié. |
| Moyen | Recherche et listes REST non paginées. | Réponses potentiellement lourdes et temps de réponse dégradé. | Recherche HTML limitée à 25 résultats par page et API paginée à 50 éléments. |
| Moyen | L’import déduisait le nom d’un livre du premier verset, supprimait les chapitres sans transaction et effectuait de nombreuses insertions unitaires. | Noms incorrects, import partiellement appliqué et durée inutilement longue. | Noms canoniques explicites, validation du JSON, transaction atomique et `bulk_create`. |
| Moyen | `db.sqlite3`, les fichiers `__pycache__` et les fichiers statiques d’administration étaient suivis par Git. | Dépôt volumineux, artefacts spécifiques à une machine et risque de divergence des données. | Nettoyage du dépôt et ajout d’un `.gitignore`; l’import reconstruit la base locale. |
| Faible | La documentation et les tests étaient quasi inexistants. | Installation et maintenance difficiles. | `README.md`, `.env.example`, dépendances déclarées et 8 tests de non-régression ajoutés. |

## Améliorations livrées

La configuration utilise désormais `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS` et `DJANGO_CSRF_TRUSTED_ORIGINS`. En mode production, les réglages HTTPS, HSTS et cookies sécurisés sont activés par défaut. `SECURE_PROXY_SSL_HEADER` permet aussi à Django de générer des URLs HTTPS correctes lorsqu’il est placé derrière un proxy qui transmet le protocole.

L’interface de lecture a été modernisée sans dépendance externe. Elle dispose maintenant d’un HTML sémantique, d’un viewport mobile, de labels accessibles, d’une navigation de chapitres plus claire, d’ancres vers chaque verset, d’une pagination de recherche et d’un respect de `prefers-reduced-motion`. Le contenu biblique reste échappé par défaut dans les templates.

L’API expose désormais `short_name` pour les livres et applique une pagination uniforme. Les requêtes de détail utilisent `select_related` lorsque cela évite des accès relationnels supplémentaires. Les modèles possèdent des contraintes explicites d’unicité et de positivité pour les livres, chapitres et versets.

La commande `load_bible` vérifie la structure générale et le nombre attendu de livres, associe les noms et abréviations canoniques, importe 66 livres dans une transaction atomique et signale le bilan. Une exécution locale avec LSG1910 a produit 66 livres, 1 189 chapitres et 31 102 versets.

## Vérifications réalisées

| Vérification | Résultat |
| --- | --- |
| `python manage.py check` | Réussi, aucun problème signalé. |
| `python manage.py check --deploy` | Réussi, aucun avertissement signalé. |
| `python manage.py test` | Réussi, 8 tests exécutés. |
| `python manage.py makemigrations --check --dry-run` | Réussi, aucune migration manquante. |
| `python -m compileall -q api bible bybl manage.py` | Réussi. |
| `git diff --check` | Réussi. |
| Import local `python manage.py load_bible` | Réussi avec LSG1910, 66 livres, 1 189 chapitres, 31 102 versets. |
| Vérification navigateur de l’accueil, de Genèse 1, de la recherche et de `/api/books/` | Réussie. |

## Recommandations appliquées

La recherche utilise désormais PostgreSQL Full Text Search avec `SearchVector`, une configuration française, `websearch` et un classement par pertinence. Une migration multi-base ajoute un index GIN sur `to_tsvector('french', text)` lorsque la base est PostgreSQL; SQLite conserve le fallback `icontains` pour le développement local. La configuration permet de sélectionner PostgreSQL avec `DJANGO_DB_ENGINE=postgresql` et les variables `POSTGRES_*`, tandis que SQLite reste le défaut sans configuration.

Une CI GitHub a été ajoutée dans `.github/workflows/ci.yml`. Elle exécute les contrôles Django, les migrations, les tests et la compilation sur Python 3.11 et 3.12 avec SQLite, ainsi qu’une vérification dédiée PostgreSQL 16 avec service de base de données. La feuille de route est ainsi réduite aux évolutions qui nécessitent un choix produit ou infrastructurel.

La provenance et le statut de diffusion de `data/bible-fr.json` sont documentés dans `DATA_LICENSE.md`. Le fichier utilise désormais Louis Segond 1910; la source retenue porte la déclaration exacte `This Bible is in the Public Domain.` [1]. Le dépôt conserve l’identifiant de fichier source, l’URL de provenance et la restriction de périmètre afin de ne pas confondre cette édition avec des révisions ou appareils critiques différents.

Le réglage `SECURE_PROXY_SSL_HEADER` reste documenté avec l’exigence opérationnelle que le proxy de production retire les en-têtes transférés non fiables avant d’ajouter `X-Forwarded-Proto`.

## Références

[1]: https://www.biblesupersearch.com/bible-downloads/ "Bible SuperSearch — Bible Downloads et déclarations de droits"
[2]: https://downloads.biblesupersearch.com/bibles/json/bibles_json_6.0.zip "Bible SuperSearch — paquet JSON 6.0 contenant FR-French/segond_1910.json"
