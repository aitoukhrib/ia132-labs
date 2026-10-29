# Lab 04 · Chasse aux bogues avec l’IA

| Module | Durée | Langages |
| --- | --- | --- |
| 3 · Débogage et optimisation avec l’IA | 25 min | Python ou TypeScript |

## Objectif

Déboguer **méthodiquement** avec un assistant : reproduire, faire expliquer, formuler des hypothèses, corriger, puis **prouver** la correction par un test de non-régression.

## Point de départ

- `rapport-incidents.md` : 5 tickets du support (symptômes, une trace d’erreur).
- `python/reservations.py` ou `typescript/reservations.ts` : le module en production.
- `test_reservations.py` / `reservations.test.ts` : 4 tests verts, 5 tests rouges (un par ticket).

```bash
pytest labs/lab04-debogage            # Python
npm run test:lab04                    # TypeScript
```

## Étapes

1. **Reproduire INC-101 (3 min)** — Lancez `python tableau_de_bord.py` (ou la version `.ts`). Vous obtenez la trace du rapport.
2. **Faire expliquer, pas corriger (5 min)** — Collez la trace **complète** dans le chat avec le fichier en contexte :
   > Voici une trace d’erreur et le code concerné. Explique la cause racine en 3 phrases, puis propose 2 corrections possibles avec leurs inconvénients. N’écris pas encore le code.

   Choisissez vous-même la correction, puis appliquez-la.
3. **Un ticket à la fois (12 min)** — Pour INC-102 à INC-104 : donnez au chat **le symptôme + le test rouge**, demandez une hypothèse, vérifiez-la (en lisant le code ou avec `print` / débogueur), corrigez, relancez **tous** les tests.
4. **Non-régression (5 min)** — Pour chaque correction, vérifiez qu’un test échoue si vous annulez la correction (`git stash` → test rouge → `git stash pop`).

## Livrable

- 9 tests au vert (INC-105 en bonus).
- Un commit par ticket : `fix(INC-10x): …`, avec la cause racine en une ligne dans le message.

## Pièges à observer

- L’IA propose `try/except ZeroDivisionError: return 0` partout : ça masque le symptôme au lieu de traiter la cause (pas de réservation → pas de jour).
- INC-104 : `round(x + 0.0001, 2)` « marche » sur ce cas… et échoue sur d’autres. Exigez une explication (représentation binaire des décimaux) et une correction de fond (`Decimal`, calcul en cents).
- Un test modifié pour devenir vert n’est pas une correction.

## Bonus

INC-105 : faites trouver la cause par l’IA **sans** lui montrer le test, seulement le ticket. A-t-elle vu le piège de `.seconds` / `getHours()` ?
