# Lab 11 · Projet final : un outil complet, de la spécification à la PR

| Module | Durée | Langages |
| --- | --- | --- |
| 7 · Ateliers pratiques | 55 min | Python ou TypeScript |

## Objectif

Développer **de bout en bout** un petit outil avec un agent de codage — plan, code, tests, documentation, CI, pull request revue — en appliquant le flux de travail d’une équipe : instructions de projet, petits commits, revue humaine.

## Point de départ

- `SPEC.md` : `taches`, un gestionnaire de tâches en ligne de commande (6 commandes, règles, codes de sortie).
- `test_acceptation.py` / `acceptation.test.ts` : 16 (Python) ou 11 (TypeScript) tests d’acceptation, tous rouges. **Ne les modifiez pas.**
- `taches/cli.py` / `taches/cli.ts` : la signature de `main()`, rien d’autre.
- `AGENTS.md` : un gabarit d’instructions pour l’agent, à compléter.

```bash
pytest labs/lab11-projet-final          # ou : npm run test:lab11
cd labs/lab11-projet-final/python && python -m taches lister     # ou : npm run taches -- lister
```

## Étapes (points d’étape toutes les 15 minutes)

1. **Préparer l’agent (5 min)** — Créez une branche `lab11`. Complétez `AGENTS.md` avec l’IA : conventions, commandes de test, ce qu’il ne doit pas faire. C’est ce fichier qui rend le travail reproductible pour toute une équipe.
2. **Plan avant le code (5 min)** — En mode agent ou plan :
   > Lis SPEC.md, AGENTS.md et les tests d’acceptation. Propose un plan d’implémentation en étapes, avec les fichiers à créer. N’écris pas de code tant que je n’ai pas validé le plan.

   Corrigez le plan (découpage `modele` / `depot` / `cli`), puis validez.
3. **Implémenter par incréments (25 min)** — Une commande à la fois : `ajouter` + `lister`, puis `terminer` / `supprimer`, puis `en-retard`, puis `exporter`. Après chaque incrément : tests verts → relecture du diff → commit `feat: …`. Ajoutez au moins **5 tests unitaires à vous** (modèle, ordre de tri, dates invalides).
4. **Documenter (5 min)** — Faites générer un `README.md` d’utilisation (installation, exemples de chaque commande, codes de sortie) et vérifiez chaque exemple en le lançant.
5. **Pull request (10 min)** — Poussez la branche, ouvrez une PR vers `main` de **votre fork**. Description générée par l’IA, puis **relue** par vous. Demandez une revue IA (Copilot *Reviewers*, ou collez le diff dans le chat avec `grille-revue.md` du lab 07). Traitez les commentaires utiles, répondez aux autres.
6. **Rétrospective (5 min)** — Dans `NOTES.md` : temps passé, ce que l’agent a bien fait, 2 erreurs qu’il a commises et comment vous les avez détectées.

## Livrable

- Tous les tests d’acceptation au vert + vos tests unitaires.
- `README.md`, `AGENTS.md`, `NOTES.md` complétés.
- Une PR sur votre fork, avec la revue et vos réponses.
- **Présentation : partage d’écran de 2 à 3 minutes** (démo de l’outil + une leçon apprise).

## Pièges à observer

- L’agent écrit tout d’un coup, 400 lignes, sans plan : arrêtez-le et revenez à l’étape 2.
- `argparse` qui appelle `sys.exit()` sur une erreur : la spécification exige un **code retourné** (2).
- Les identifiants réutilisés après suppression : un test le vérifie.
- Une PR « générée et fusionnée » sans relecture : c’est vous qui en répondez.

## Bonus

- Ajoutez la commande `modifier <id> [--titre] [--priorite] [--echeance]`, avec ses tests d’acceptation écrits **avant** le code.
- Ajoutez le job du lab 11 au pipeline CI du lab 09.
