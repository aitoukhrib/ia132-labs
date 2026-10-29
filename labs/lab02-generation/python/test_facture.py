"""Tests d'acceptation : ils décrivent SPEC.md. Ne les modifiez pas, faites-les passer."""

import pytest

from facture import calculer_facture


def lignes(*articles):
    return [{"produit": f"article {i}", "prix": p, "quantite": q} for i, (p, q) in enumerate(articles)]


PANIER = lignes((18_999, 1), (1_299, 2))  # écran + 2 câbles = 215,97 $


def test_petite_commande_avec_livraison():
    assert calculer_facture(lignes((4_999, 1))) == {
        "sous_total": 4_999, "rabais": 0, "livraison": 999, "tps": 300, "tvq": 598, "total": 6_896,
    }


def test_livraison_gratuite_des_75_dollars():
    assert calculer_facture(PANIER) == {
        "sous_total": 21_597, "rabais": 0, "livraison": 0, "tps": 1_080, "tvq": 2_154, "total": 24_831,
    }


def test_code_bienvenue10():
    assert calculer_facture(PANIER, "BIENVENUE10") == {
        "sous_total": 21_597, "rabais": 2_160, "livraison": 0, "tps": 972, "tvq": 1_939, "total": 22_348,
    }


def test_le_rabais_peut_faire_perdre_la_livraison_gratuite():
    facture = calculer_facture(lignes((4_000, 2)), "BIENVENUE10")
    assert facture["rabais"] == 800
    assert facture["livraison"] == 999
    assert facture["total"] == 9_427


def test_ete15_sous_le_seuil_ne_donne_rien():
    facture = calculer_facture(lignes((4_000, 2)), "ETE15")
    assert facture["rabais"] == 0
    assert facture["total"] == 9_198


def test_ete15_au_dessus_du_seuil():
    assert calculer_facture(PANIER, "ETE15")["rabais"] == 3_240
    assert calculer_facture(PANIER, "ETE15")["total"] == 21_106


def test_code_insensible_a_la_casse_et_aux_espaces():
    assert calculer_facture(PANIER, "  bienvenue10 ") == calculer_facture(PANIER, "BIENVENUE10")


def test_arrondi_de_la_moitie_vers_le_haut():
    # base taxable 1 010 ¢ : TPS = 50,5 ¢ → 51 ¢ (et non 50 ¢ comme avec round())
    facture = calculer_facture(lignes((11, 1)))
    assert facture["tps"] == 51
    assert facture["total"] == 1_162


def test_code_promo_inconnu():
    with pytest.raises(ValueError, match="(?i)code promo"):
        calculer_facture(PANIER, "GRATUIT100")


@pytest.mark.parametrize(
    "mauvaises_lignes",
    [[], lignes((1_000, 0)), lignes((-1, 1))],
    ids=["facture vide", "quantité nulle", "prix négatif"],
)
def test_entrees_invalides(mauvaises_lignes):
    with pytest.raises(ValueError):
        calculer_facture(mauvaises_lignes)
