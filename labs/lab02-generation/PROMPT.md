# Prompt — Calculer une facture

## CONTEXTE

Je travaille dans le dépôt `ia132-labs`. Choisis **un seul** langage et complète le fichier correspondant :

- Python 3.10+ : `labs/lab02-generation/python/facture.py`, fonction `calculer_facture`.
- TypeScript strict, Node.js 22.18+ : `labs/lab02-generation/typescript/facture.ts`, fonction `calculerFacture`.

Respecte les conventions du projet : noms en français sans accents dans les identifiants. En Python, utilise les annotations de type, le style PEP 8 et une docstring Google. En TypeScript, n’utilise pas `any` et documente la fonction exportée avec TSDoc.

## TÂCHE

Implémente la fonction pour calculer la facture selon toutes les règles de [SPEC.md](./SPEC.md). Lis la spécification au complet et suis l’ordre de calcul indiqué.

## CONTRAINTES

- Tous les montants sont des entiers en cents : n’utilise pas de nombres à virgule flottante.
- Pour chaque pourcentage (rabais, TPS et TVQ), arrondis au cent le plus proche, avec les demis vers le haut. N’utilise pas directement `round()` en Python.
- Calcule la TPS et la TVQ chacune sur la base taxable, pas en cascade.
- Le seuil de livraison gratuite s’évalue après le rabais. Le seuil de `ETE15` s’évalue sur le sous-total avant rabais.
- Normalise le code promo en ignorant la casse et les espaces autour.
- Respecte les erreurs et les types d’exception précisés dans `SPEC.md`.
- N’ajoute aucune dépendance et ne modifie aucun test ni autre fichier.

## FORMAT

Modifie uniquement le fichier d’implémentation du langage choisi. Garde la fonction publique existante et ajoute seulement les fonctions privées nécessaires. Retourne exactement la structure de facture définie dans `SPEC.md`.

## EXEMPLES

1. Une ligne à 4 999 ¢, sans code promo, donne : sous-total 4 999 ¢, livraison 999 ¢, TPS 300 ¢, TVQ 598 ¢ et total 6 896 ¢.
2. Deux articles à 4 000 ¢ avec le code `BIENVENUE10` donnent un rabais de 800 ¢. Le montant après rabais est 7 200 ¢, donc la livraison coûte 999 ¢ et le total est 9 427 ¢.
