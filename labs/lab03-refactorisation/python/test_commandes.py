"""Tests de caractérisation (« golden master ») : ils figent le comportement ACTUEL.

Ils sont verts au départ et doivent le rester après CHAQUE étape de refactorisation.
Le fichier donnees/attendu.json a été produit en exécutant le code hérité.
"""

import json
from pathlib import Path

import pytest

from commandes import traiter

DONNEES = Path(__file__).resolve().parent.parent / "donnees"
COMMANDES = json.loads((DONNEES / "commandes.json").read_text(encoding="utf-8"))
ATTENDU = json.loads((DONNEES / "attendu.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("cas", sorted(ATTENDU))
def test_golden_master(cas):
    region, formule = cas.split("-")
    assert traiter(COMMANDES, region, formule == "premium") == ATTENDU[cas]


def test_commande_simple_au_quebec():
    commande = {"id": "X", "statut": "payee", "poids": 1, "lignes": [{"prix": 20, "qte": 2}]}
    assert traiter([commande], "QC", False) == [{"id": "X", "total": 48, "livraison": 8, "priorite": "basse"}]


def test_premium_livraison_offerte_au_dela_de_100():
    commande = {"id": "X", "statut": "payee", "poids": 5, "lignes": [{"prix": 150, "qte": 1}]}
    assert traiter([commande], "ON", True)[0]["livraison"] == 0


def test_commandes_annulees_et_poids_invalides_ignorees():
    commandes = [
        {"id": "A", "statut": "annulee", "poids": 1, "lignes": []},
        {"id": "B", "statut": "payee", "poids": 0, "lignes": []},
    ]
    assert traiter(commandes, "QC", False) == []
