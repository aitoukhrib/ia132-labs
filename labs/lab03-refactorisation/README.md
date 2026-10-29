# Lab 03 · Refactoriser du code hérité, sans rien casser

| Module | Durée | Langages |
| --- | --- | --- |
| 2 · Génération et réécriture de code | 25 min | Python ou TypeScript |

## Objectif

Refactoriser un module hérité **par petites étapes vérifiées** : l’IA propose, les tests de caractérisation protègent, Git garde chaque étape.

## Point de départ

- `python/commandes.py` ou `typescript/commandes.ts` : une fonction `traiter(c, r, p)` de 50 lignes — noms d’une lettre, `if` imbriqués sur 4 niveaux, nombres magiques, code dupliqué par région.
- `test_commandes.py` / `commandes.test.ts` : **tests de caractérisation**, verts au départ. Ils figent le comportement actuel (fichier `donnees/attendu.json`).

```bash
pytest labs/lab03-refactorisation                          # Python
ruff check --select C901 labs/lab03-refactorisation        # complexité (Python)
npm run test:lab03                                         # TypeScript
```

## Étapes

1. **Diagnostic (5 min)** — Demandez au chat :
   > Liste les problèmes de lisibilité et de maintenabilité de traiter(), du plus coûteux au moins coûteux. Ne propose pas encore de code.

   Notez la complexité de départ (`ruff check --select C901` signale `traiter` comme trop complexe).
2. **Plan (3 min)** — Demandez un **plan de refactorisation en 5 étapes maximum**, chacune ne changeant pas le comportement. Validez ou réordonnez le plan vous-même.
3. **Exécution pas à pas (15 min)** — Pour chaque étape : demandez **cette étape seulement** → relisez le diff → lancez les tests → `git commit -m "refactor: …"`. Si un test casse : `git restore .` et reformulez.
   Pistes : noms explicites, constantes nommées, grille de tarifs par région (dictionnaire / dataclass), fonctions `frais_livraison`, `priorite`, retours anticipés (`continue`) au lieu des `if` imbriqués, types.
4. **Bilan (2 min)** — Relancez `ruff check --select C901` : `traiter` ne doit plus apparaître.

## Livrable

- Tests de caractérisation **toujours verts**, sans les avoir modifiés.
- 3 à 5 commits `refactor: …`, chacun vert.
- `traiter` sous le seuil de complexité (8).

## Pièges à observer

- « J’en ai profité pour corriger un bogue » : en refactorisation, **aucun** changement de comportement. Les arrondis (`round(t + f, 2)`) et les seuils stricts (`> 100`) doivent rester identiques.
- L’IA remplace le `print` par une exception : c’est un changement de comportement. Un `logging.warning` est acceptable ; discutez-en.
- Une grosse réécriture d’un seul coup : impossible à relire, impossible à annuler proprement.

## Bonus

Demandez à l’assistant d’ajouter des **types** (`TypedDict`/`dataclass` en Python, `type Commande` en TypeScript) et vérifiez que les tests passent encore.
