"""Tests unitaires du dépôt JSON."""

from taches.depot import Depot


def test_ajout_est_persistant_et_l_identifiant_suit_le_prochain_appel(tmp_path):
    fichier = tmp_path / "taches.json"

    premiere = Depot(fichier)
    assert premiere.ajouter("Première").id == 1

    seconde = Depot(fichier)
    assert [tache.id for tache in seconde.lister()] == [1]
    assert seconde.ajouter("Deuxième").id == 2


def test_supprimer_ne_reutilise_pas_l_identifiant_apres_rechargement(tmp_path):
    fichier = tmp_path / "taches.json"
    depot = Depot(fichier)
    depot.ajouter("À supprimer")
    depot.ajouter("À garder")

    assert depot.supprimer(1)
    assert Depot(fichier).ajouter("Après suppression").id == 3


def test_terminer_persiste_l_etat_et_reste_terminée_apres_rechargement(tmp_path):
    fichier = tmp_path / "taches.json"
    depot = Depot(fichier)
    depot.ajouter("À terminer")

    assert depot.terminer(1).terminee
    recharge = Depot(fichier)
    assert recharge.lister() == []
    assert recharge.lister(toutes=True)[0].terminee
