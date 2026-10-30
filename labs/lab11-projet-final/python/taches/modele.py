"""Modèle et règles métier du gestionnaire de tâches."""

from dataclasses import dataclass, field
from datetime import date

PRIORITES = ("haute", "normale", "basse")
_ORDRE_PRIORITES = {priorite: rang for rang, priorite in enumerate(PRIORITES)}


def valider_date(valeur: str | None) -> date | None:
    """Convertit une date ISO stricte ou lève une erreur de validation."""
    if valeur is None:
        return None
    try:
        resultat = date.fromisoformat(valeur)
    except (TypeError, ValueError) as erreur:
        raise ValueError("date invalide : format AAAA-MM-JJ attendu") from erreur
    if resultat.isoformat() != valeur:
        raise ValueError("date invalide : format AAAA-MM-JJ attendu")
    return resultat


@dataclass
class Tache:
    """Représente une tâche persistée."""

    id: int
    titre: str
    priorite: str = "normale"
    echeance: date | None = None
    etiquettes: list[str] = field(default_factory=list)
    terminee: bool = False

    def __post_init__(self) -> None:
        if not self.titre.strip():
            raise ValueError("titre vide")
        if self.priorite not in PRIORITES:
            raise ValueError("priorité invalide")
        if self.id < 1:
            raise ValueError("identifiant invalide")
        if self.echeance is not None and not isinstance(self.echeance, date):
            raise ValueError("date invalide : format AAAA-MM-JJ attendu")

    def cle_tri(self) -> tuple[int, date, int]:
        """Retourne la clé de tri : priorité, échéance puis identifiant."""
        return (
            _ORDRE_PRIORITES[self.priorite],
            self.echeance or date.max,
            self.id,
        )

    def vers_dict(self) -> dict[str, object]:
        """Sérialise la tâche au format public spécifié."""
        return {
            "id": self.id,
            "titre": self.titre,
            "priorite": self.priorite,
            "echeance": self.echeance.isoformat() if self.echeance else None,
            "etiquettes": list(self.etiquettes),
            "terminee": self.terminee,
        }

    def formater(self) -> str:
        """Formate la tâche sur une ligne pour les commandes de liste."""
        etat = "x" if self.terminee else " "
        echeance = self.echeance.isoformat() if self.echeance else "—"
        ligne = f"[{etat}] {self.id}  {self.priorite:<9}{echeance:<10}  {self.titre}"
        if self.etiquettes:
            ligne += "  " + " ".join(f"#{etiquette}" for etiquette in self.etiquettes)
        return ligne


def trier_taches(taches: list[Tache]) -> list[Tache]:
    """Trie les tâches selon les règles de la spécification."""
    return sorted(taches, key=Tache.cle_tri)
