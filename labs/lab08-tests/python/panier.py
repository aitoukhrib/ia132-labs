"""Lab 08 — Panier d'achat. Ce module n'a AUCUN test : à vous de les générer.

Les prix sont des entiers en cents.
"""

from dataclasses import dataclass, field

QUANTITE_MAX = 99
SEUIL_LIVRAISON_GRATUITE = 5_000
FRAIS_LIVRAISON = 799


class StockInsuffisant(Exception):
    """La quantité demandée dépasse le stock disponible."""


@dataclass
class Produit:
    sku: str
    nom: str
    prix: int
    stock: int


@dataclass
class Panier:
    lignes: dict[str, int] = field(default_factory=dict)
    catalogue: dict[str, Produit] = field(default_factory=dict)
    code_promo: str | None = None

    def ajouter(self, produit: Produit, quantite: int = 1) -> None:
        if quantite < 1:
            raise ValueError("quantité invalide")
        nouvelle = self.lignes.get(produit.sku, 0) + quantite
        if nouvelle > QUANTITE_MAX:
            raise ValueError(f"maximum {QUANTITE_MAX} par article")
        if nouvelle > produit.stock:
            raise StockInsuffisant(f"{produit.nom} : {produit.stock} en stock")
        self.catalogue[produit.sku] = produit
        self.lignes[produit.sku] = nouvelle

    def retirer(self, sku: str, quantite: int | None = None) -> None:
        if sku not in self.lignes:
            raise KeyError(sku)
        if quantite is None or quantite >= self.lignes[sku]:
            del self.lignes[sku]
        else:
            self.lignes[sku] -= quantite

    def appliquer_code(self, code: str) -> None:
        if code.upper() not in {"MOINS10", "LIVRAISON"}:
            raise ValueError("code inconnu")
        self.code_promo = code.upper()

    def sous_total(self) -> int:
        return sum(self.catalogue[sku].prix * q for sku, q in self.lignes.items())

    def rabais(self) -> int:
        if self.code_promo == "MOINS10":
            return self.sous_total() // 10
        return 0

    def livraison(self) -> int:
        if not self.lignes:
            return 0
        if self.code_promo == "LIVRAISON":
            return 0
        if self.sous_total() - self.rabais() >= SEUIL_LIVRAISON_GRATUITE:
            return 0
        return FRAIS_LIVRAISON

    def total(self) -> int:
        return self.sous_total() - self.rabais() + self.livraison()

    def nombre_articles(self) -> int:
        return sum(self.lignes.values())
