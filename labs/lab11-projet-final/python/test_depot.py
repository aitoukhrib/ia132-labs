"""Tests unitaires du dépôt JSON."""

from taches.depot import Depot


def test_ajout_est_persistant_et_l_identifiant_suit_le_prochain_appel(tmp_path):
    fichier = tmp_path / "taches.json"

    premiere = Depot(fichier)
    assert premiere.ajouter("Première").id == 1

    seconde = Depot(fichier)
    assert [tache.id for tache in seconde.lister()] == [1]
    assert seconde.ajouter("Deuxième").id == 2
