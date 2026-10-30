"""Tests de comportement du panier : cas nominaux, limites et erreurs."""

import pytest

from panier import (
    FRAIS_LIVRAISON,
    QUANTITE_MAX,
    SEUIL_LIVRAISON_GRATUITE,
    Panier,
    Produit,
    StockInsuffisant,
)


@pytest.fixture
def panier():
    """Fournit un panier neuf pour chaque test."""
    return Panier()


@pytest.fixture
def clavier():
    """Fournit un produit dont le stock permet de tester la limite du panier."""
    return Produit("KB-01", "Clavier", 4_999, stock=200)


def test_un_panier_vide_a_tous_ses_montants_et_compteurs_a_zero(panier):
    assert panier.sous_total() == 0
    assert panier.rabais() == 0
    assert panier.livraison() == 0
    assert panier.total() == 0
    assert panier.nombre_articles() == 0


def test_ajouter_un_produit_enregistre_le_produit_et_sa_quantite(panier, clavier):
    panier.ajouter(clavier)

    assert panier.lignes == {clavier.sku: 1}
    assert panier.catalogue == {clavier.sku: clavier}
    assert panier.nombre_articles() == 1


def test_ajouter_plusieurs_fois_le_meme_sku_cumule_les_quantites(panier, clavier):
    panier.ajouter(clavier, 2)
    panier.ajouter(clavier, 3)

    assert panier.lignes[clavier.sku] == 5
    assert panier.nombre_articles() == 5


@pytest.mark.parametrize("quantite", [0, -1, -10])
def test_ajouter_une_quantite_inferieure_a_un_leve_value_error(panier, clavier, quantite):
    with pytest.raises(ValueError):
        panier.ajouter(clavier, quantite)

    assert panier.lignes == {}


def test_ajouter_exactement_la_quantite_maximale_est_permis(panier, clavier):
    panier.ajouter(clavier, QUANTITE_MAX)

    assert panier.lignes[clavier.sku] == QUANTITE_MAX


def test_ajouter_au_dela_de_la_quantite_maximale_leve_value_error(panier, clavier):
    panier.ajouter(clavier, QUANTITE_MAX)

    with pytest.raises(ValueError):
        panier.ajouter(clavier)

    assert panier.lignes[clavier.sku] == QUANTITE_MAX


def test_ajouter_exactement_le_stock_disponible_est_permis(panier):
    produit = Produit("ST-01", "Stylo", 250, stock=3)

    panier.ajouter(produit, 3)

    assert panier.lignes[produit.sku] == 3


def test_ajouter_plus_que_le_stock_disponible_leve_stock_insuffisant(panier):
    produit = Produit("ST-01", "Stylo", 250, stock=3)
    panier.ajouter(produit, 2)

    with pytest.raises(StockInsuffisant):
        panier.ajouter(produit, 2)

    assert panier.lignes[produit.sku] == 2


def test_retirer_un_sku_absent_leve_key_error(panier):
    with pytest.raises(KeyError):
        panier.retirer("INCONNU")


@pytest.mark.parametrize("quantite", [None, 3])
def test_retirer_toute_la_quantite_supprime_la_ligne(panier, clavier, quantite):
    panier.ajouter(clavier, 3)

    panier.retirer(clavier.sku, quantite)

    assert clavier.sku not in panier.lignes
    assert panier.nombre_articles() == 0


def test_retirer_une_partie_de_la_quantite_diminue_la_ligne(panier, clavier):
    panier.ajouter(clavier, 5)

    panier.retirer(clavier.sku, 2)

    assert panier.lignes[clavier.sku] == 3


@pytest.mark.parametrize(
    ("code", "code_attendu"),
    [("moins10", "MOINS10"), ("Moins10", "MOINS10"), ("livraison", "LIVRAISON")],
)
def test_appliquer_un_code_promo_ignore_la_casse(panier, code, code_attendu):
    panier.appliquer_code(code)

    assert panier.code_promo == code_attendu


def test_appliquer_un_code_inconnu_leve_value_error_sans_remplacer_le_code(panier):
    panier.appliquer_code("MOINS10")

    with pytest.raises(ValueError):
        panier.appliquer_code("INCONNU")

    assert panier.code_promo == "MOINS10"


@pytest.mark.parametrize(
    ("prix", "rabais_attendu"),
    [(9_999, 999), (10_001, 1_000)],
)
def test_code_moins10_calcule_dix_pourcent_arrondis_en_cents(
    panier, prix, rabais_attendu
):
    panier.ajouter(Produit("PR-01", "Produit", prix, stock=1))
    panier.appliquer_code("MOINS10")

    assert panier.rabais() == rabais_attendu


def test_un_code_livraison_donne_la_livraison_gratuite(panier):
    panier.ajouter(Produit("PR-01", "Produit", 1, stock=1))
    panier.appliquer_code("LIVRAISON")

    assert panier.livraison() == 0


def test_un_panier_sous_le_seuil_paie_les_frais_de_livraison(panier):
    panier.ajouter(Produit("PR-01", "Produit", SEUIL_LIVRAISON_GRATUITE - 1, stock=1))

    assert panier.livraison() == FRAIS_LIVRAISON


def test_un_panier_au_seuil_exact_a_la_livraison_gratuite(panier):
    panier.ajouter(Produit("PR-01", "Produit", SEUIL_LIVRAISON_GRATUITE, stock=1))

    assert panier.livraison() == 0


def test_le_seuil_de_livraison_est_evalue_apres_le_rabais(panier):
    panier.ajouter(Produit("PR-01", "Produit", 5_500, stock=1))
    panier.appliquer_code("MOINS10")

    assert panier.sous_total() - panier.rabais() == SEUIL_LIVRAISON_GRATUITE - 50
    assert panier.livraison() == FRAIS_LIVRAISON


def test_le_sous_total_et_le_nombre_d_articles_cumulent_plusieurs_produits(panier):
    panier.ajouter(Produit("PR-01", "Produit A", 125, stock=10), 2)
    panier.ajouter(Produit("PR-02", "Produit B", 300, stock=10), 3)

    assert panier.sous_total() == 1_150
    assert panier.nombre_articles() == 5


def test_le_total_soustrait_le_rabais_et_ajoute_la_livraison(panier):
    panier.ajouter(Produit("PR-01", "Produit", 4_000, stock=1))
    panier.appliquer_code("MOINS10")

    assert panier.total() == 4_000 - 400 + FRAIS_LIVRAISON
