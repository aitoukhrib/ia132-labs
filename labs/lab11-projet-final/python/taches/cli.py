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


def _lire_identifiant(arguments: list[str]) -> int:
    if len(arguments) != 1:
        raise ValueError("un identifiant de tâche est requis")
    try:
        identifiant = int(arguments[0])
    except ValueError as erreur:
        raise ValueError("identifiant invalide") from erreur
    if identifiant < 1:
        raise ValueError("identifiant invalide")
    return identifiant


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


def _ajouter(arguments: list[str], depot: Depot) -> tuple[int, str]:
    titre, priorite, echeance, etiquettes = _options_ajouter(arguments)
    tache = depot.ajouter(titre, priorite, echeance, etiquettes)
    return 0, f"Tâche {tache.id} ajoutée : {tache.titre}"


def _lister(arguments: list[str], depot: Depot) -> tuple[int, str]:
    toutes, etiquette, priorite = _options_lister(arguments)
    taches = depot.lister(toutes, etiquette, priorite)
    if not taches:
        return 0, "Aucune tâche."
    return 0, "\n".join(tache.formater() for tache in taches)


def _terminer_ou_supprimer(
    commande: str,
    arguments: list[str],
    depot: Depot,
) -> tuple[int, str]:
    identifiant = _lire_identifiant(arguments)
    if commande == "terminer":
        tache = depot.terminer(identifiant)
        if tache is None:
            return 1, f"Erreur : tâche {identifiant} introuvable"
        return 0, f"Tâche {identifiant} terminée"
    if not depot.supprimer(identifiant):
        return 1, f"Erreur : tâche {identifiant} introuvable"
    return 0, f"Tâche {identifiant} supprimée"


def _executer(commande: str, arguments: list[str], depot: Depot) -> tuple[int, str]:
    if commande == "ajouter":
        return _ajouter(arguments, depot)
    if commande == "lister":
        return _lister(arguments, depot)
    if commande in {"terminer", "supprimer"}:
        return _terminer_ou_supprimer(commande, arguments, depot)
    return 2, f"Erreur : commande inconnue : {commande}"


def main(argv: list[str], fichier: Path) -> tuple[int, str]:
    """Exécute une commande et retourne (code de sortie, texte à afficher)."""
    if not argv:
        return 2, "Erreur : commande manquante"
    commande, *arguments = argv
    try:
        depot = Depot(fichier)
        return _executer(commande, arguments, depot)
    except ValueError as erreur:
        return 2, f"Erreur : {erreur}"
