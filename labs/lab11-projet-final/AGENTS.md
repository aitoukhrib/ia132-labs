# Instructions de l’agent — projet `taches`

## Source de vérité

- Suivre `SPEC.md` pour les comportements, formats de sortie et codes de retour.
- Implémenter la variante Python du projet, sauf demande explicite contraire.
- Avant toute implémentation, proposer un plan découpé en `modele.py`, `depot.py` et `cli.py`, puis attendre sa validation.

## Architecture

- `python/taches/modele.py` : tâche, validations, ordre de tri et règles métier.
- `python/taches/depot.py` : lecture et écriture JSON, persistance des identifiants.
- `python/taches/cli.py` : commandes et fonction `main(argv, fichier)` sans appel à `sys.exit`.
- Garder la logique métier testable sans interface de commande ni accès direct aux fichiers.

## Conventions

- Code, noms et commentaires en français ; identifiants sans accents.
- Python 3.10+, annotations de type, style PEP 8, docstrings Google et Ruff.
- Utiliser uniquement la bibliothèque standard ; JSON UTF-8 et dates ISO `AAAA-MM-JJ`.
- Lever ou convertir explicitement les erreurs de saisie conformément aux codes et textes de `SPEC.md` ; ne pas avaler les exceptions.
- Préserver l’ordre de tri spécifié, les identifiants croissants jamais réutilisés et les formats d’export exacts.
- Ajouter un test unitaire à chaque comportement ou correction ; les exemples de README doivent être exécutables.

## Commandes

Depuis la racine du dépôt :

- Tests d’acceptation : `python -m pytest labs/lab11-projet-final/python/test_acceptation.py`
- Tests du lab : `python -m pytest labs/lab11-projet-final`
- Tests et couverture (si pytest-cov est installé) : `python -m pytest labs/lab11-projet-final/python --cov=labs/lab11-projet-final/python/taches --cov-branch`
- Lint : `python -m ruff check labs/lab11-projet-final/python`
- Lancer l’outil : `python -m taches <commande>` depuis `labs/lab11-projet-final/python`

Après chaque incrément, lancer les tests ciblés, relire le diff, puis créer un commit `feat: ...` seulement si les tests passent.

## Règles strictes — ne pas faire

- Ne jamais modifier `python/test_acceptation.py` ni `typescript/acceptation.test.ts`.
- Ne pas modifier de fichiers hors de `labs/lab11-projet-final/`.
- Ne pas ajouter de dépendance externe.
- Ne pas implémenter avant validation explicite du plan.
- Ne pas appeler `sys.exit` depuis `main`, ne pas réutiliser un identifiant supprimé et ne pas changer les sorties spécifiées.
- Si un test échoue, s’arrêter, diagnostiquer et corriger l’implémentation avant de poursuivre.

## Avant de terminer

- [ ] Tests du lab verts et Ruff sans erreur.
- [ ] Au moins cinq tests unitaires dédiés couvrent modèle, tri et dates invalides.
- [ ] Chaque exemple et chaque commande du README ont été exécutés.
- [ ] Diff relu ; aucun fichier hors du lab modifié.
