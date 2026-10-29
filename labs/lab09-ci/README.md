# Lab 09 · Tests d’intégration, charge et pipeline CI/CD

| Module | Durée | Langages |
| --- | --- | --- |
| 5 · Génération de tests et assurance qualité | 35 min | Python et/ou TypeScript + GitHub Actions |

## Objectif

Faire écrire par l’IA des **tests d’intégration** sur une vraie API, simuler une **charge** avec un objectif de service, puis brancher le tout dans un **pipeline GitHub Actions** qui bloque une PR fautive.

## Point de départ

- `api.py` / `api.ts` : une mini-API de liens courts (création, redirection, statistiques), sans dépendance.
- Tests unitaires existants (verts) ; `test_integration.py` / `integration.test.ts` : un seul test (`/sante`).
- `charge.py` / `charge.ts` : test de charge (80 % de lectures) avec objectif p95 < 50 ms et < 1 % d’erreurs.
- `ci-a-completer.yml` : un pipeline à trous ; `python/test_workflow.py` : ses critères d’acceptation (rouges).

```bash
pytest labs/lab09-ci                               # ou : npm run test:lab09
python labs/lab09-ci/python/charge.py              # ou : node labs/lab09-ci/typescript/charge.ts
```

## Étapes

1. **Scénarios d’intégration (10 min)** — Demandez :
   > Voici une API HTTP (api.py) et la fixture de test qui démarre un vrai serveur. Liste les scénarios d’intégration à couvrir (nominal, erreurs 4xx, concurrence), puis écris-les en réutilisant requete().

   Visez au moins 6 scénarios, dont **200 créations concurrentes** qui doivent donner 200 codes uniques.
2. **Couverture (3 min)** — `pytest labs/lab09-ci/python --cov=api --cov-report=term-missing` : ≥ 80 % ?
3. **Charge (7 min)** — Lancez `charge.py`, puis `charge.py 5000 100`. Faites **interpréter** les chiffres à l’IA (p50 vs p99, débit, erreurs). Demandez-lui un second scénario « pic » (100 % de créations) et comparez.
4. **Pipeline (12 min)** — Copiez `ci-a-completer.yml` dans `.github/workflows/ci.yml` et faites compléter les 6 TODO par l’IA. Validez localement :
   ```bash
   pytest labs/lab09-ci/python/test_workflow.py
   ```
5. **Le voir bloquer (3 min)** — Poussez sur votre fork, ouvrez une PR qui casse un test (ex. `LONGUEUR_CODE = 5`) : le pipeline doit passer **au rouge**. Fermez la PR.

## Livrable

- Tests d’intégration verts, couverture ≥ 80 %.
- `.github/workflows/ci.yml` : critères de `test_workflow.py` au vert, exécution verte sur GitHub (onglet *Actions*).
- Une phrase dans `NOTES.md` : « l’objectif de service est / n’est pas respecté parce que… ».

## Pièges à observer

- Des tests d’intégration qui appellent les fonctions en mémoire (`Depot()`) : ce sont des tests unitaires déguisés.
- Un port fixe (8009) dans les tests : échecs aléatoires en CI. Utilisez le port 0.
- L’IA invente des actions (`actions/setup-python@v9`) ou des options : vérifiez sur la page de l’action.
- Des secrets écrits dans le YAML : utilisez `${{ secrets.NOM }}`.

## Bonus

Ajoutez au pipeline une étape qui lance `charge.py 1000 10` et échoue si l’objectif de service n’est pas respecté.
