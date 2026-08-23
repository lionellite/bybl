# Notice de droits sur les données bibliques

## Statut de vérification

Le fichier `data/bible-fr.json` utilise désormais **Louis Segond 1910 (LSG1910)**. Le paquet JSON de Bible SuperSearch identifie cette édition comme `Louis Segond 1910`, indique l’année 1910 et porte la mention exacte `This Bible is in the Public Domain.` [1]. Le dépôt conserve ces métadonnées dans le JSON sous `License`, `SourceURL` et `SourceFile`.

Cette déclaration de domaine public est la base du choix de remplacement de FRC97. Elle ne doit toutefois pas être étendue automatiquement à d’éventuelles éditions révisées, aux notes, aux références Strong ou à d’autres fichiers provenant du même site. Bybl n’importe que le texte verset par verset de `FR-French/segond_1910.json`. Le responsable du projet doit encore vérifier la portée territoriale applicable à son déploiement et conserver une copie de la déclaration de source.

## Règle de diffusion

Pour la version LSG1910 retenue, la source consultée indique un usage et une redistribution possibles sans demande d’autorisation individuelle, car elle la marque comme domaine public [1]. Bybl n’ajoute aucune note, appareil critique ou contenu sous licence distincte. Toute redistribution doit néanmoins conserver cette notice, la provenance et les métadonnées de licence; elle ne doit pas présenter comme libres des éditions révisées ou des contenus additionnels non vérifiés.

La page de téléchargement précise aussi que chaque Bible possède sa propre déclaration de droits et recommande de consulter la mention de copyright correspondante [1]. Cette précaution est appliquée ici en figeant l’identifiant `segond_1910.json`, sa déclaration `Public Domain` et sa provenance, plutôt qu’en important indistinctement tout le catalogue.

## Procédure interne recommandée

Conserver dans le dépôt la provenance et la déclaration de licence correspondant exactement au fichier importé. Si la source change, exiger une nouvelle vérification de l’identifiant, de la version et de la déclaration de droits avant de remplacer `data/bible-fr.json`, puis réexécuter `python manage.py load_bible`.

Ce fichier est une notice opérationnelle et non un avis juridique. Une validation par un professionnel du droit reste nécessaire avant une diffusion commerciale ou un usage à grande échelle.

## Sources publiques consultées

[1]: https://www.biblesupersearch.com/bible-downloads/ "Bible SuperSearch — Bible Downloads et déclarations de droits"
[2]: https://downloads.biblesupersearch.com/bibles/json/bibles_json_6.0.zip "Bible SuperSearch — paquet JSON 6.0 contenant FR-French/segond_1910.json"
