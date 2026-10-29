"""Tests unitaires existants (verts). Les tests d'intégration sont à écrire : test_integration.py."""

import pytest

from api import LONGUEUR_CODE, Depot, nouveau_code, url_valide


@pytest.mark.parametrize("url", ["https://technologia.com", "http://exemple.ca/a?b=1"])
def test_urls_valides(url):
    assert url_valide(url)


@pytest.mark.parametrize("url", ["ftp://x.ca", "javascript:alert(1)", "https://", "", None, 42, "https://a.ca/" + "x" * 3000])
def test_urls_invalides(url):
    assert not url_valide(url)


def test_code_de_6_caracteres_alphanumeriques():
    code = nouveau_code()
    assert len(code) == LONGUEUR_CODE and code.isalnum()


def test_depot_compte_les_visites():
    depot = Depot()
    code = depot.creer("https://exemple.ca")
    depot.visiter(code)
    depot.visiter(code)
    assert depot.stats(code)["clics"] == 2
    assert depot.visiter("inconnu") is None
