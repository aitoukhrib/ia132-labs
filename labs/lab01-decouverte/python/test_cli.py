"""Étape 4 (mode agent) : ces tests échouent tant que la fonction main() n'existe pas."""

import convertisseur


def test_cli_conversion():
    assert convertisseur.main(["100", "C", "F"]) == "212.00 F"
    assert convertisseur.main(["42.195", "km", "mi"]) == "26.22 mi"


def test_cli_valeur_invalide():
    assert convertisseur.main(["abc", "C", "F"]).startswith("Erreur")


def test_cli_arguments_manquants():
    assert convertisseur.main(["100"]).startswith("Usage")
