# Lab 02 · Générer du code à partir d’une spécification

| Module | Durée | Langages |
| --- | --- | --- |
| 2 · Génération et réécriture de code | 25 min | Python ou TypeScript |

## Objectif

Rédiger un **prompt structuré** (contexte, tâche, contraintes, format, exemples) et utiliser des **tests existants comme critère d’acceptation** du code généré.

## Point de départ

- `SPEC.md` : les règles métier (TPS, TVQ, rabais, livraison, arrondi).
- `python/facture.py` ou `typescript/facture.ts` : la signature seule.
- `test_facture.py` / `facture.test.ts` : 12 tests d’acceptation, tous en échec. **Ne les modifiez pas.**

## Étapes

1. **Lisez** `SPEC.md` (3 min). Repérez les 2 règles les plus piégeuses.
2. **Rédigez votre prompt** dans un fichier `PROMPT.md` en suivant le canevas :
   ```text
   CONTEXTE    : langage, version, fichier, conventions du projet
   TÂCHE       : ce que la fonction doit faire (renvoyer à SPEC.md avec #file / @SPEC.md)
   CONTRAINTES : entiers en cents, arrondi demi vers le haut, pas de dépendance, exceptions…
   FORMAT      : une seule fonction + fonctions privées, sans modifier les tests
   EXEMPLES    : 1 ou 2 cas chiffrés tirés de SPEC.md
   ```
3. **Générez** l’implémentation (chat ou édition), en joignant `SPEC.md` et le fichier de tests au contexte.
4. **Lancez les tests**. S’il en reste en échec : copiez **le message d’échec** dans le chat plutôt que de demander « corrige ».
5. **Relisez** le code : chaque règle de `SPEC.md` est-elle visible et nommée (constantes, petites fonctions) ?

```bash
pytest labs/lab02-generation       # Python
npm run test:lab02                 # TypeScript
```

## Livrable

- 12 tests au vert, sans modification des tests.
- `PROMPT.md` : votre prompt final + le nombre d’itérations nécessaires.

## Pièges à observer

- `round()` en Python arrondit 50,5 à 50 : le test d’arrondi le détecte.
- Des montants en `float` (`0.05 * base`) : refusez-les, la spécification impose des entiers.
- L’assistant qui « corrige » un test pour le faire passer.

## Bonus

Demandez à l’assistant 5 cas limites **absents** des tests (ex. code `ETE15` à exactement 100,00 $). Ajoutez ceux qui sont justes… après avoir vérifié le calcul à la main.
