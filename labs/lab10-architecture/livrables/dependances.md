# Analyse des dépendances du prototype Cantine (2019)

## Méthode et limites

Les manifests inspectés sont `dependances/requirements-legacy.txt` et `dependances/package.json`. L’audit a été exécuté le **30 octobre 2026** avec :

- `python -m pip_audit --disable-pip --no-deps -r labs/lab10-architecture/dependances/requirements-legacy.txt`
- `npm audit --json` sur une copie temporaire de `package.json`, après génération d’un lockfile temporaire avec `npm install --package-lock-only --ignore-scripts --no-audit`.

Le dépôt ne fournit pas de `package-lock.json`. Le rapport npm est donc un audit de l’arbre résolu au moment de l’exécution, pas un SBOM reproductible du prototype. Les bases d’avis et versions évoluent : relancer les audits avant toute réutilisation et ajouter un lockfile maintenu au projet choisi.

### Vérification des identifiants CVE

**Identifiants CVE inventés par l’IA : aucun.** Aucun numéro CVE proposé par l’IA n’est repris dans ce rapport. Les résultats décrits ci-dessous proviennent des commandes d’audit ; leurs références sont des identifiants d’avis PYSEC et GHSA, et non des CVE générés par l’IA. Vérifier chaque référence dans la base de l’outil avant de la citer comme CVE.

La commande complète `python -m pip_audit -r ...` a aussi été tentée. Sur l’interpréteur Python 3.15 de cet environnement, la résolution échoue avant l’audit : la construction des métadonnées de Pillow 8.0.0 lève `KeyError: '__version__'`. Le tableau Python ci-dessous provient donc du mode `--no-deps`, qui audite les versions explicitement épinglées sans construire/résoudre leurs dépendances transitives ; il ne prétend pas couvrir les dépendances transitives. Pour un audit complet, relancer la commande dans un environnement Python pris en charge par ces anciennes versions, ou après migration vers des versions maintenues.

## Résultats Python

`pip-audit` a trouvé **235 avis connus pour les sept paquets épinglés**. Nombre de lignes d’avis affichées par paquet :

| Paquet épinglé | Avis signalés | Conclusion |
| --- | ---: | --- |
| Django 2.2.0 | 73 | Version ancienne et vulnérable ; ne pas exposer en production |
| requests 2.19.1 | 10 | Version vulnérable ; mettre à niveau et revoir l’usage |
| urllib3 1.24.1 | 25 | Version vulnérable, notamment comme dépendance déclarée/transitive |
| PyYAML 5.3 | 4 | Version vulnérable ; mettre à niveau et contrôler le chargement de YAML |
| Jinja2 2.10 | 12 | Version vulnérable ; mettre à niveau et examiner le rendu de contenu non fiable |
| Pillow 8.0.0 | 109 | Nombreux avis ; mettre à niveau et limiter le traitement d’images non fiables |
| Celery 4.3.0 | 2 | Version vulnérable et ancienne ; mettre à niveau ou retirer si inutilisée |

Les versions correctives affichées varient par avis. Une mise à niveau doit viser une version maintenue compatible, puis être verrouillée et retestée ; appliquer seulement le premier correctif d’un avis ne garantit pas que tous les autres soient corrigés.

## Résultats npm

`npm audit` a rapporté **15 vulnérabilités** dans l’arbre résolu : 2 critiques, 8 élevées, 2 modérées et 3 faibles. Parmi les dépendances directes déclarées, l’audit signale :

| Dépendance directe | Version déclarée | Résultat et action |
| --- | ---: | --- |
| axios | 0.21.0 | Avis élevés ; mettre à niveau vers une version maintenue |
| express | 4.16.0 | Avis élevés ; mise à niveau proposée vers Express 4.22.3 dans le rapport |
| jsonwebtoken | 8.5.1 | Avis élevés ; le correctif proposé change la version majeure, à traiter avec tests |
| lodash | 4.17.15 | Avis élevés ; mettre à niveau vers la version corrigée et remplacer les fonctions inutilisées |
| moment | 2.29.1 | Avis élevés ; bibliothèque en mode maintenance, envisager une alternative si justifié |
| request | 2.88.0 | Avis critiques ; paquet déprécié, le retirer et le remplacer plutôt que le conserver |

Le rapport mentionne également des vulnérabilités transitives, notamment dans `body-parser`, `cookie`, `form-data`, `path-to-regexp`, `qs`, `send`, `serve-static`, `tough-cookie` et `uuid`. Les corrections npm proposées doivent être vérifiées sur le lockfile réellement adopté ; pour `request`, l’audit ne propose pas de correction automatique.

## Recommandation

Ne pas réutiliser ces versions en production. Partir d’un manifeste minimal adapté au monolithe choisi, supprimer les dépendances inutilisées et remplacer `request`. Sélectionner des versions maintenues, générer et versionner un lockfile, relancer `pip-audit`/`npm audit`, corriger les avis, puis exécuter les tests fonctionnels, d’intégration et de compatibilité avant déploiement.
