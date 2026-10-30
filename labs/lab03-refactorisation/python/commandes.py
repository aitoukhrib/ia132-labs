from typing import TypedDict


POIDS_PALIER_1 = 2
POIDS_PALIER_2 = 10
SEUIL_LIVRAISON_GRATUITE = 100
SEUIL_PRIORITE_NORMALE = 100
SEUIL_PRIORITE_HAUTE = 500
TARIFS_REGIONAUX = {
    "QC": (8, 15, 1.5),
    "ON": (10, 18, 1.75),
}
TARIF_PAR_DEFAUT = (14, 25, 2.5)


class LigneCommande(TypedDict):
    prix: int | float
    qte: int


class Commande(TypedDict):
    id: str
    statut: str
    poids: int | float
    lignes: list[LigneCommande]


class ResultatCommande(TypedDict):
    id: str
    total: float
    livraison: float
    priorite: str


def calculer_sous_total(lignes: list[LigneCommande]) -> float:
    """Calcule le sous-total des lignes d'une commande."""
    sous_total = 0
    for ligne in lignes:
        sous_total += ligne["prix"] * ligne["qte"]
    return sous_total


def frais_livraison(poids: int | float, region: str, sous_total: float, client_premium: bool) -> float:
    """Calcule les frais de livraison selon le poids, la region et le statut client."""
    tarif_palier_1, tarif_palier_2, tarif_kilo_sup = TARIFS_REGIONAUX.get(region, TARIF_PAR_DEFAUT)

    if poids <= POIDS_PALIER_1:
        frais = tarif_palier_1
    elif poids <= POIDS_PALIER_2:
        frais = tarif_palier_2
    else:
        frais = tarif_palier_2 + (poids - POIDS_PALIER_2) * tarif_kilo_sup

    if client_premium:
        if sous_total > SEUIL_LIVRAISON_GRATUITE:
            frais = 0
        else:
            frais = frais / 2
    return frais


def priorite(sous_total: float) -> str:
    """Determine la priorite d'une commande selon son sous-total."""
    if sous_total > SEUIL_PRIORITE_HAUTE:
        return "haute"
    if sous_total > SEUIL_PRIORITE_NORMALE:
        return "normale"
    return "basse"


def traiter(commandes: list[Commande], region: str, client_premium: bool) -> list[ResultatCommande]:
    """Calcule le total, la livraison et la priorite des commandes valides."""
    resultats = []
    for commande in commandes:
        if commande["statut"] == "annulee":
            continue
        if commande["poids"] <= 0:
            print("poids invalide " + str(commande["id"]))
            continue

        sous_total = calculer_sous_total(commande["lignes"])
        frais = frais_livraison(commande["poids"], region, sous_total, client_premium)
        resultats.append(
            {
                "id": commande["id"],
                "total": round(sous_total + frais, 2),
                "livraison": round(frais, 2),
                "priorite": priorite(sous_total),
            }
        )
    return resultats
