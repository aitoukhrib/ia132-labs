"""Vos tests du panier. Remplacez ce test par les vôtres (voir README).

    pytest labs/lab08-tests --cov=panier --cov-branch --cov-report=term-missing
    python labs/lab08-tests/python/mutants.py
"""

from panier import Panier, Produit

CLAVIER = Produit("KB-01", "Clavier", 4_999, stock=10)


def test_panier_vide():
    assert Panier().total() == 0


def test_ajouter_un_article():
    panier = Panier()
    panier.ajouter(CLAVIER)
    assert panier.nombre_articles() == 1
