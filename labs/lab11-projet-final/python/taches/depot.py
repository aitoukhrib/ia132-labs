"""Persistance JSON et opérations sur les tâches."""

import json
from pathlib import Path

from taches.modele import Tache, trier_taches, valider_date


class Depot:
    """Charge et enregistre les tâches dans un fichier JSON."""

    def __init__(self, fichier: Path):
        self.fichier = fichier
        self.prochain_id = 1
        self.taches: list[Tache] = []
        self._charger()

    def _charger(self) -> None:
        if not self.fichier.exists():
            return
        donnees = json.loads(self.fichier.read_text(encoding="utf-8"))
        if not isinstance(donnees, dict) or not isinstance(donnees.get("taches"), list):
            raise ValueError("fichier de tâches invalide")
        self.taches = [
            Tache(
                id=int(element["id"]),
                titre=element["titre"],
                priorite=element["priorite"],
                echeance=valider_date(element.get("echeance")),
                etiquettes=element.get("etiquettes", []),
                terminee=element.get("terminee", False),
            )
            for element in donnees["taches"]
        ]
        minimum = max((tache.id for tache in self.taches), default=0) + 1
        self.prochain_id = max(int(donnees.get("prochain_id", minimum)), minimum)

    def _enregistrer(self) -> None:
        donnees = {
            "prochain_id": self.prochain_id,
            "taches": [tache.vers_dict() for tache in self.taches],
        }
        self.fichier.parent.mkdir(parents=True, exist_ok=True)
        self.fichier.write_text(
            json.dumps(donnees, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def ajouter(
        self,
        titre: str,
        priorite: str = "normale",
        echeance: str | None = None,
        etiquettes: list[str] | None = None,
    ) -> Tache:
        """Crée une tâche et réserve définitivement son identifiant."""
        tache = Tache(
            id=self.prochain_id,
            titre=titre,
            priorite=priorite,
            echeance=valider_date(echeance),
            etiquettes=etiquettes or [],
        )
        self.prochain_id += 1
        self.taches.append(tache)
        self._enregistrer()
        return tache

    def lister(
        self,
        toutes: bool = False,
        etiquette: str | None = None,
        priorite: str | None = None,
    ) -> list[Tache]:
        """Retourne les tâches filtrées et triées."""
        resultat = [
            tache
            for tache in self.taches
            if (toutes or not tache.terminee)
            and (etiquette is None or etiquette in (tache.etiquettes or []))
            and (priorite is None or tache.priorite == priorite)
        ]
        return trier_taches(resultat)

    def terminer(self, identifiant: int) -> Tache | None:
        """Marque une tâche comme terminée, ou renvoie None si elle est absente."""
        tache = next((element for element in self.taches if element.id == identifiant), None)
        if tache is None:
            return None
        tache.terminee = True
        self._enregistrer()
        return tache

    def supprimer(self, identifiant: int) -> bool:
        """Supprime une tâche sans réutiliser son identifiant."""
        for index, tache in enumerate(self.taches):
            if tache.id == identifiant:
                del self.taches[index]
                self._enregistrer()
                return True
        return False
