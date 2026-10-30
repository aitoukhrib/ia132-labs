"""Lab 02 — Calcul d'une facture avec TPS et TVQ.

À générer avec votre assistant à partir de SPEC.md (voir README).
Tous les montants sont des entiers, en cents.
"""

SEUIL_ETE15_CENTS = 10_000
SEUIL_LIVRAISON_GRATUITE_CENTS = 7_500
FRAIS_LIVRAISON_CENTS = 999
TAUX_BIENVENUE10 = (10, 100)
TAUX_ETE15 = (15, 100)
TAUX_TPS = (5, 100)
TAUX_TVQ = (9_975, 100_000)


def _arrondir_pourcentage(montant: int, numerateur: int, denominateur: int) -> int:
    """Arrondit un pourcentage au cent le plus proche, avec les demis vers le haut."""
    return (2 * montant * numerateur + denominateur) // (2 * denominateur)


def _calculer_rabais(sous_total: int, code_promo: str | None) -> int:
    """Calcule le rabais applicable à partir du sous-total et du code promo."""
    if code_promo is not None and not isinstance(code_promo, str):
        raise ValueError("Le code promo doit être du texte.")
    code_normalise = code_promo.strip().upper() if code_promo is not None else ""

    if code_normalise == "BIENVENUE10":
        return _arrondir_pourcentage(sous_total, *TAUX_BIENVENUE10)
    if code_normalise == "ETE15":
        if sous_total >= SEUIL_ETE15_CENTS:
            return _arrondir_pourcentage(sous_total, *TAUX_ETE15)
        return 0
    if code_normalise == "":
        return 0
    raise ValueError("Code promo inconnu")


def calculer_facture(lignes: list[dict], code_promo: str | None = None) -> dict[str, int]:
    """Calcule une facture à partir de lignes contenant produit, prix et quantite.

    Args:
        lignes: Articles avec un produit textuel, un prix en cents et une quantite.
        code_promo: Code promotionnel facultatif.

    Returns:
        Les montants de la facture en cents.

    Raises:
        ValueError: Si la facture ou une ligne est invalide, ou si le code promo
            est inconnu.
    """
    if not lignes:
        raise ValueError("Facture vide")

    sous_total = 0
    for ligne in lignes:
        if not isinstance(ligne, dict):
            raise ValueError("Chaque ligne doit être un dictionnaire.")
        if not isinstance(ligne.get("produit"), str):
            raise ValueError("Le produit doit être du texte.")

        prix = ligne.get("prix")
        quantite = ligne.get("quantite")
        if isinstance(prix, bool) or not isinstance(prix, int) or prix < 0:
            raise ValueError("Le prix doit être un entier supérieur ou égal à zéro.")
        if isinstance(quantite, bool) or not isinstance(quantite, int) or quantite < 1:
            raise ValueError("La quantité doit être un entier supérieur ou égal à un.")
        sous_total += prix * quantite

    rabais = _calculer_rabais(sous_total, code_promo)
    livraison = 0 if sous_total - rabais >= SEUIL_LIVRAISON_GRATUITE_CENTS else FRAIS_LIVRAISON_CENTS
    base_taxable = sous_total - rabais + livraison
    tps = _arrondir_pourcentage(base_taxable, *TAUX_TPS)
    tvq = _arrondir_pourcentage(base_taxable, *TAUX_TVQ)
    total = base_taxable + tps + tvq

    return {
        "sous_total": sous_total,
        "rabais": rabais,
        "livraison": livraison,
        "tps": tps,
        "tvq": tvq,
        "total": total,
    }
