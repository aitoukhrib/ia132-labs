"""Commandes de la ligne de commande du gestionnaire de tâches."""

from pathlib import Path

from taches.depot import Depot
from taches.modele import PRIORITES


def _options_ajouter(arguments: list[str]) -> tuple[str, str, str | None, list[str]]:
    if not arguments or arguments[0].startswith("--"):
        raise ValueError("titre requis")
    titre = arguments[0]
    priorite = "normale"
    echeance = None
    etiquettes = []
    index = 1
    while index < len(arguments):
        option = arguments[index]
        if option not in {"--priorite", "--echeance", "--etiquette"}:
            raise ValueError(f"option inconnue : {option}")
        if index + 1 >= len(arguments) or arguments[index + 1].startswith("--"):
            raise ValueError(f"valeur manquante pour {option}")
        valeur = arguments[index + 1]
        if option == "--priorite":
            priorite = valeur
        elif option == "--echeance":
            echeance = valeur
        else:
            etiquettes.append(valeur)
        index += 2
    if priorite not in PRIORITES:
        raise ValueError("priorité invalide")
    return titre, priorite, echeance, etiquettes


def _lire_option(
    arguments: list[str],
    index: int,
    correspondances: dict[str, str],
) -> tuple[str, str, int]:
    option = arguments[index]
    nom = correspondances.get(option)
    if nom is None:
        raise ValueError(f"option inconnue : {option}")
    if index + 1 >= len(arguments) or arguments[index + 1].startswith("--"):
        raise ValueError(f"valeur manquante pour {option}")
    return nom, arguments[index + 1], index + 2


def _options_lister(arguments: list[str]) -> tuple[bool, str | None, str | None]:
    toutes = False
    etiquette = None
    priorite = None
    index = 0
    options = {"--etiquette": "etiquette", "--priorite": "priorite"}
    while index < len(arguments):
        option = arguments[index]
        if option == "--toutes" and not toutes:
            toutes = True
            index += 1
            continue
        nom, valeur, index = _lire_option(arguments, index, options)
        if nom == "etiquette":
            if etiquette is not None:
                raise ValueError("option --etiquette répétée")
            etiquette = valeur
        else:
            if priorite is not None:
                raise ValueError("option --priorite répétée")
            if valeur not in PRIORITES:
                raise ValueError("priorité invalide")
            priorite = valeur
    return toutes, etiquette, priorite


def main(argv: list[str], fichier: Path) -> tuple[int, str]:
    """Exécute une commande et retourne (code de sortie, texte à afficher)."""
    if not argv:
        return 2, "Erreur : commande manquante"
    commande, *arguments = argv
    try:
        depot = Depot(fichier)
        if commande == "ajouter":
            titre, priorite, echeance, etiquettes = _options_ajouter(arguments)
            tache = depot.ajouter(titre, priorite, echeance, etiquettes)
            return 0, f"Tâche {tache.id} ajoutée : {tache.titre}"
        if commande == "lister":
            toutes, etiquette, priorite = _options_lister(arguments)
            taches = depot.lister(toutes, etiquette, priorite)
            if not taches:
                return 0, "Aucune tâche."
            return 0, "\n".join(tache.formater() for tache in taches)
        return 2, f"Erreur : commande inconnue : {commande}"
    except ValueError as erreur:
        return 2, f"Erreur : {erreur}"
