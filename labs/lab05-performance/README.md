# Lab 05 · Optimiser avec l’IA… et le prouver par la mesure

| Module | Durée | Langages |
| --- | --- | --- |
| 3 · Débogage et optimisation avec l’IA | 20 min | Python ou TypeScript |

## Objectif

Faire analyser la **complexité** d’un code par l’IA, appliquer l’optimisation proposée, puis **mesurer** le gain sans changer le comportement.

## Point de départ

- `analyse.py` / `analyse.ts` : 3 fonctions correctes mais quadratiques (`in` sur une liste, `count` dans une boucle).
- `test_analyse.py` / `analyse.test.ts` : le comportement à préserver (verts).
- `test_performance.py` / fin de `analyse.test.ts` : 2 budgets de temps (rouges).
- `bench.py` / `bench.ts` : chronomètre les fonctions quand la taille double.

```bash
python labs/lab05-performance/python/bench.py     # ou : npm run bench:lab05
pytest labs/lab05-performance                     # ou : npm run test:lab05
```

## Étapes

1. **Mesurer d’abord (3 min)** — Lancez le banc d’essai. Quand la taille double, le temps est-il ×2 ou ×4 ? Notez les chiffres.
2. **Faire analyser (5 min)** — Demandez :
   > Donne la complexité en temps de chaque fonction de ce fichier, en expliquant la ligne responsable. Propose une version O(n) qui garde exactement le même résultat, y compris l’ordre des éléments.
3. **Appliquer et vérifier (7 min)** — Appliquez une fonction à la fois, relancez **les tests de comportement** après chacune.
4. **Mesurer après (5 min)** — Relancez le banc d’essai, puis `bench.py 200000`. Les budgets de temps passent-ils ?

## Livrable

- Tous les tests au vert, dont les 2 budgets de temps.
- Un tableau avant / après dans `NOTES.md` (3 tailles × 3 fonctions).

## Pièges à observer

- `list(set(courriels))` est rapide… mais **perd l’ordre** : un test le détecte.
- `Counter.most_common()` départage les égalités par ordre d’apparition, pas alphabétique.
- « C’est plus rapide » sans mesure n’est pas une preuve. Une micro-optimisation (compréhension de liste au lieu d’une boucle) ne change pas un O(n²).

## Bonus

Demandez à l’IA un profil d’exécution (`python -m cProfile -s cumtime bench.py`, ou `node --cpu-prof`) et faites-lui interpréter le résultat.
