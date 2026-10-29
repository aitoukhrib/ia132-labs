# Instructions pour l’assistant de code (dépôt ia132-labs)

Ce fichier est lu automatiquement par GitHub Copilot (et peut être joint au contexte des autres assistants).
Il décrit les conventions de ce dépôt. Les labs 02, 07 et 11 s’en servent.

## Langue et style

- Code, noms et commentaires en **français**, sans accents dans les identifiants (`calculer_facture`, `dureeHeures`).
- Python : PEP 8, annotations de type, docstrings au format Google, `ruff` doit passer.
- TypeScript : mode `strict`, pas de `any`, fonctions exportées documentées en TSDoc.

## Règles de l’équipe

- Montants d’argent en **entiers (cents)**, jamais en nombres à virgule.
- Requêtes SQL **toujours paramétrées**.
- Aucun secret dans le code : variables d’environnement.
- Erreurs : lever une exception explicite (`ValueError` / `RangeError`), ne jamais l’avaler avec un `except` vide.
- Tout changement de comportement s’accompagne d’un test.

## Ce que l’assistant ne doit pas faire

- Modifier un test pour le faire passer.
- Ajouter une dépendance sans le signaler.
- Toucher aux fichiers hors du lab en cours.
