"""Tests unitaires des validations et règles de tri du modèle."""

from datetime import date

import pytest

from taches.modele import Tache, trier_taches, valider_date


def test_le_modele_refuse_un_titre_vide_ou_blanc():
    with pytest.raises(ValueError, match="titre vide"):
        Tache(1, "   ")


@pytest.mark.parametrize("valeur", ["2026-13-01", "2026-02-30", "2026-1-01", "demain"])
def test_la_date_doit_etre_une_date_iso_valide(valeur):
    with pytest.raises(ValueError, match="date invalide"):
        valider_date(valeur)


def test_la_date_absente_est_conservee_comme_absente():
    assert valider_date(None) is None


def test_le_tri_priorise_puis_trie_par_echeance_et_identifiant():
    taches = [
        Tache(4, "sans date"),
        Tache(3, "tard", echeance=date(2026, 12, 1)),
        Tache(2, "tôt", echeance=date(2026, 11, 1)),
        Tache(1, "haute", priorite="haute"),
        Tache(5, "même date", echeance=date(2026, 11, 1)),
    ]

    assert [tache.id for tache in trier_taches(taches)] == [1, 2, 5, 3, 4]


def test_le_modele_rejette_une_priorite_inconnue():
    with pytest.raises(ValueError, match="priorité invalide"):
        Tache(1, "Valide", priorite="urgente")
