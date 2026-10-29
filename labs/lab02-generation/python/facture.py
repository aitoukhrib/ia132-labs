"""Lab 02 — Calcul d'une facture avec TPS et TVQ.

À générer avec votre assistant à partir de SPEC.md (voir README).
Tous les montants sont des entiers, en cents.
"""


def calculer_facture(lignes: list[dict], code_promo: str | None = None) -> dict[str, int]:
    """Calcule une facture à partir de lignes {"produit", "prix", "quantite"}.

    Retourne {"sous_total", "rabais", "livraison", "tps", "tvq", "total"}, en cents.
    Les règles complètes sont dans SPEC.md.
    """
    raise NotImplementedError
