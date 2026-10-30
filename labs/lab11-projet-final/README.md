# Lab 11 · Projet final : un outil complet, de la spécification à la PR

| Module | Durée | Langages |
| --- | --- | --- |
| 7 · Ateliers pratiques | 55 min | Python ou TypeScript |

## Objectif

Développer **de bout en bout** un petit outil avec un agent de codage — plan, code, tests, documentation, CI, pull request revue — en appliquant le flux de travail d’une équipe : instructions de projet, petits commits, revue humaine.

## Contenu du lab

- `SPEC.md` : `taches`, un gestionnaire de tâches en ligne de commande (6 commandes, règles, codes de sortie).
- `python/test_acceptation.py` / `typescript/acceptation.test.ts` : tests d’acceptation à préserver, complétés par des tests unitaires dédiés.
- `python/taches/` : implémentation Python répartie entre modèle, dépôt JSON et CLI.
- `AGENTS.md` : conventions, commandes et règles spécifiques à l’agent du projet.

```bash
pytest labs/lab11-projet-final          # ou : npm run test:lab11
cd labs/lab11-projet-final/python && python -m taches lister     # ou : npm run taches -- lister
```

## Utiliser l’outil Python `taches`

### Installation

Python 3.10 ou plus récent suffit ; aucune dépendance externe n’est requise.
Depuis la racine du dépôt, lancez les commandes dans
`labs/lab11-projet-final/python`. Les tâches sont conservées dans `taches.json`
dans le répertoire courant.

```bash
cd labs/lab11-projet-final/python
python -m taches lister
```

### Exemples des commandes

Les exemples ci-dessous s’exécutent dans l’ordre et utilisent une date fixe pour
garder les résultats prévisibles.

**Ajouter** une tâche ; priorité normale par défaut et étiquettes répétables :

```bash
python -m taches ajouter "Préparer la démo" --priorite haute --echeance 2026-10-29 --etiquette ia --etiquette formation
# Tâche 1 ajoutée : Préparer la démo
python -m taches ajouter "Envoyer le compte rendu" --echeance 2026-11-05
# Tâche 2 ajoutée : Envoyer le compte rendu
```

**Lister** toutes les tâches actives ou appliquer les filtres :

```bash
python -m taches lister
# [ ] 1  haute    2026-10-29  Préparer la démo  #ia #formation
# [ ] 2  normale  2026-11-05  Envoyer le compte rendu
python -m taches lister --etiquette ia
python -m taches lister --priorite haute
python -m taches lister --toutes
```

**Terminer** une tâche la masque de la liste par défaut ; `--toutes` l’inclut :

```bash
python -m taches terminer 2
# Tâche 2 terminée
python -m taches lister --toutes
# affiche également la tâche 2 avec [x]
```

**Supprimer** une tâche ; son identifiant ne sera jamais réutilisé :

```bash
python -m taches supprimer 2
# Tâche 2 supprimée
```

**Repérer les tâches en retard** (échéance strictement antérieure au jour donné) :

```bash
python -m taches en-retard --aujourdhui 2026-10-30
# [ ] 1  haute    2026-10-29  Préparer la démo  #ia #formation
```

**Exporter** toutes les tâches présentes, terminées ou non, triées comme la liste :

```bash
python -m taches exporter --format json
# [{"id": 1, "titre": "Préparer la démo", "priorite": "haute", "echeance": "2026-10-29", "etiquettes": ["ia", "formation"], "terminee": false}]
python -m taches exporter --format csv
# id,titre,priorite,echeance,etiquettes,terminee
# 1,Préparer la démo,haute,2026-10-29,ia;formation,non
```

### Codes de sortie

| Code | Signification | Exemple |
| ---: | --- | --- |
| `0` | Succès | Ajout, liste ou export |
| `1` | Tâche introuvable | `python -m taches terminer 42` |
| `2` | Commande ou argument invalide | Priorité/date invalide, titre vide ou commande inconnue |

`main(argv, fichier)` retourne ce code et le texte de sortie ; le module
`python -m taches` affiche le texte puis termine avec le code retourné.

Depuis la racine du dépôt, exécutez les tests et le lint :

```bash
python -m pytest labs/lab11-projet-final
python -m ruff check labs/lab11-projet-final/python
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
