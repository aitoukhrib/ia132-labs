# Lab 08 · Générer des tests unitaires qui servent vraiment

| Module | Durée | Langages |
| --- | --- | --- |
| 5 · Génération de tests et assurance qualité | 30 min | Python ou TypeScript |

## Objectif

Faire générer une suite de tests par l’IA (cas nominaux, limites, erreurs), puis la juger avec deux **mesures objectives** : la couverture des branches et le **score de mutation**.

## Point de départ

- `panier.py` / `panier.ts` : un panier d’achat (ajout, retrait, codes promo, livraison) sans tests.
- `test_panier.py` / `panier.test.ts` : 2 tests de départ.
- `mutants.py` / `mutants.ts` : introduit 8 bogues un par un et vérifie que vos tests les détectent.

```bash
# Python
pytest labs/lab08-tests --cov=panier --cov-branch --cov-report=term-missing
python labs/lab08-tests/python/mutants.py
# TypeScript
npm run cov:lab08
node labs/lab08-tests/typescript/mutants.ts
```

Au départ : couverture ≈ 40 %, score de mutation **1/8**.

## Étapes

1. **Lister les comportements d’abord (5 min)** — Demandez :
   > Liste les comportements de cette classe à tester : cas nominaux, valeurs limites, erreurs. Un comportement par ligne, sans code.

   Ajoutez-en un que l’IA a oublié.
2. **Générer (10 min)** — Faites générer les tests (`/tests` dans Copilot, *Generate tests* dans JetBrains, ou le chat), **avec** : fixtures, `pytest.mark.parametrize` / boucles de `test`, noms de tests en phrases.
3. **Mesurer (5 min)** — Couverture des branches, puis mutants. Pour chaque mutant **survivant**, demandez à l’IA le test qui le tuerait.
4. **Relire (5 min)** — Chaque test vérifie-t-il quelque chose ? Supprimez ceux qui ne font qu’exécuter du code (`assert panier is not None`).
5. **Valeurs limites (5 min)** — Vérifiez qu’il existe un test **exactement au seuil** (99 articles, 50,00 $ de livraison gratuite, stock exact).

## Livrable

- Couverture des branches **≥ 95 %**.
- Score de mutation **8/8**.
- Tous les tests au vert, en moins d’une seconde.

## Pièges à observer

- 100 % de couverture et 3/8 mutants tués : la couverture mesure ce qui **s’exécute**, pas ce qui est **vérifié**.
- L’IA calcule l’attendu avec la même formule que le code (`assert total == sous_total - sous_total // 10`) : le test recopie le bogue. Écrivez des valeurs littérales (`9_998 - 999`).
- Les tests qui dépendent les uns des autres (panier partagé, sans fixture).

## Bonus

Demandez des tests **par propriétés** (`hypothesis` en Python, `fast-check` en TypeScript) : « le total n’est jamais négatif », « ajouter puis retirer laisse le panier inchangé ».
