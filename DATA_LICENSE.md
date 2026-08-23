# Notice de droits sur les données bibliques

## Statut de vérification

Le fichier `data/bible-fr.json` indique la version `FRC97` et la mention `Publisher: French Bible Society`. Les sources publiques consultées identifient le Français courant de 1997 comme la version révisée en profondeur par la Nouvelle Français courant publiée en 2019 [1]. Elles ne fournissent toutefois pas, dans les pages consultées, une licence de redistribution explicite correspondant précisément au fichier `FRC97` utilisé par Bybl.

En conséquence, la présence de ce fichier dans le dépôt ne doit pas être interprétée comme une autorisation de reproduction, de redistribution ou d’exploitation commerciale. Le projet reste en **statut de diffusion à clarifier** pour le texte biblique.

## Règle de diffusion

Avant toute mise en production publique, redistribution du fichier JSON, exploitation commerciale ou exposition durable du texte par l’API, le responsable du projet doit obtenir une autorisation écrite couvrant explicitement : la traduction FRC97, le stockage numérique, le rendu HTML, l’exposition par API, la recherche plein texte, la mise en cache et la redistribution éventuelle.

La page officielle des éditions Bibli’O indique qu’une demande d’autorisation doit être adressée pour utiliser leurs versions ou traductions et précise que leurs contenus sont protégés [2]. Elle indique également une opposition aux opérations de moissonnage et de fouille de textes et de données, sauf accord spécifique formel [2]. Ces éléments justifient le maintien d’un contrôle humain avant publication et ne constituent pas une qualification juridique définitive de la licence FRC97.

## Procédure interne recommandée

Conserver dans un emplacement privé la demande adressée au titulaire des droits, la réponse reçue, le périmètre autorisé, la durée, les territoires, les obligations d’attribution et les éventuelles limites de volume. Lorsque l’autorisation ne couvre pas l’usage prévu, remplacer `data/bible-fr.json` par un texte dont la licence autorise explicitement l’usage, puis réexécuter `python manage.py load_bible`.

Ce fichier est une notice opérationnelle et non un avis juridique. Une validation par un professionnel du droit reste nécessaire avant une diffusion commerciale ou un usage à grande échelle.

## Sources publiques consultées

[1]: https://editionsbiblio.fr/collections/nouvelle-francais-courant "Éditions Bibli’O — Bibles en version Nouvelle Français courant"
[2]: https://editionsbiblio.fr/pages/obtenir-des-droits "Éditions Bibli’O — Obtenir des droits et utiliser nos traductions de la Bible"
