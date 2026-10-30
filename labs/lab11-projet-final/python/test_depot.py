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


def test_en_retard_exclut_la_date_du_jour_les_dates_futures_et_les_taches_terminees(tmp_path):
    depot = Depot(tmp_path / "taches.json")
    depot.ajouter("Hier", echeance="2026-11-01")
    depot.ajouter("Aujourd'hui", echeance="2026-11-02")
    depot.ajouter("Demain", echeance="2026-11-03")
    depot.ajouter("Terminée", echeance="2026-11-01")
    depot.terminer(4)

    assert [tache.id for tache in depot.en_retard("2026-11-02")] == [1]
