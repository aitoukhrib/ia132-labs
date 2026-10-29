# Spécification · Calcul d’une facture (boutique en ligne québécoise)

Tous les montants sont des **entiers, en cents** (1 999 = 19,99 $). Jamais de nombres à virgule.

## Entrée

- `lignes` : liste de lignes `{ produit: texte, prix: entier ≥ 0, quantite: entier ≥ 1 }`.
- `code_promo` (facultatif) : texte, **insensible à la casse et aux espaces autour**.

## Règles, dans l’ordre

1. **Sous-total** = somme de `prix × quantite`.
2. **Rabais** selon le code promo :
   - aucun code → 0 ;
   - `BIENVENUE10` → 10 % du sous-total ;
   - `ETE15` → 15 % du sous-total, **seulement si le sous-total atteint 100,00 $** (10 000 cents), sinon 0 ;
   - tout autre code → erreur « Code promo inconnu ».
3. **Livraison** : gratuite si *sous-total − rabais* ≥ 75,00 $ (7 500 cents), sinon 9,99 $ (999 cents).
4. **Base taxable** = sous-total − rabais + livraison.
5. **TPS** = 5 % de la base taxable · **TVQ** = 9,975 % de la base taxable (calculées chacune sur la base, pas en cascade).
6. **Total** = base taxable + TPS + TVQ.

## Arrondi

Chaque montant calculé par pourcentage (rabais, TPS, TVQ) est arrondi **au cent le plus proche, la moitié vers le haut** (50,5 → 51). Attention : l’arrondi par défaut de Python (`round`) arrondit la moitié au pair (50,5 → 50).

## Erreurs

- Liste de lignes vide → erreur « Facture vide ».
- Quantité < 1 ou prix < 0 → erreur.
- Python : `ValueError` · TypeScript : `RangeError`.

## Sortie

| Python | TypeScript |
| --- | --- |
| `{"sous_total", "rabais", "livraison", "tps", "tvq", "total"}` | `{ sousTotal, rabais, livraison, tps, tvq, total }` |
