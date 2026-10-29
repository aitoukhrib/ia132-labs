# Spécification · `taches`, un gestionnaire de tâches en ligne de commande

Les tâches sont conservées dans un fichier JSON (par défaut `taches.json`). Chaque commande lit le fichier, agit, puis l’enregistre.

## Interface de programmation (pour les tests)

| Python | TypeScript |
| --- | --- |
| `main(argv: list[str], fichier: Path) -> tuple[int, str]` dans `taches/cli.py` | `main(argv: string[], fichier: string): { code: number; sortie: string }` dans `taches/cli.ts` |

`argv` ne contient pas le nom du programme. La fonction **retourne** le code de sortie et le texte affiché (elle n’appelle pas `sys.exit`).

## Commandes

| Commande | Effet | Sortie (code 0) |
| --- | --- | --- |
| `ajouter "<titre>" [--priorite haute\|normale\|basse] [--echeance AAAA-MM-JJ] [--etiquette X]…` | Crée une tâche. Priorité par défaut : `normale`. `--etiquette` est répétable. | `Tâche <id> ajoutée : <titre>` |
| `lister [--toutes] [--etiquette X] [--priorite P]` | Tâches **non terminées** (toutes avec `--toutes`), filtrées. | Une ligne par tâche, ou `Aucune tâche.` |
| `terminer <id>` | Marque la tâche terminée. | `Tâche <id> terminée` |
| `supprimer <id>` | Supprime la tâche. | `Tâche <id> supprimée` |
| `en-retard --aujourdhui AAAA-MM-JJ` | Tâches non terminées dont l’échéance est **strictement** avant la date. | Comme `lister` |
| `exporter --format json\|csv` | Toutes les tâches. | Le JSON ou le CSV |

## Règles

1. Les identifiants sont des entiers croissants à partir de 1, **jamais réutilisés** (même après suppression).
2. Ordre d’affichage : priorité (`haute`, `normale`, `basse`), puis échéance la plus proche (sans échéance en dernier), puis identifiant.
3. Format d’une ligne : `[ ] 3  haute    2026-11-05  Préparer la démo  #formation #ia` (`[x]` si terminée ; `—` si pas d’échéance).
4. Titre vide ou fait d’espaces : erreur.
5. Export JSON : liste d’objets `{id, titre, priorite, echeance, etiquettes, terminee}` (`echeance` : `null` si absente).
6. Export CSV : en-tête `id,titre,priorite,echeance,etiquettes,terminee` ; étiquettes séparées par `;` ; `terminee` vaut `oui`/`non`.

## Codes de sortie

| Code | Cas | Sortie |
| --- | --- | --- |
| 0 | Succès | voir ci-dessus |
| 1 | Tâche introuvable | `Erreur : tâche <id> introuvable` |
| 2 | Commande ou argument invalide (priorité, date, titre vide, commande inconnue) | `Erreur : …` |
