"""Deux familles de tests.

1. Comportement : verts au départ, ils doivent le rester (documenter ne change pas le code).
2. Documentation : rouges au départ. Chaque fonction publique doit avoir une docstring
   au format Google (Args:, Returns:, et Raises: si elle lève une exception) avec au moins
   un exemple exécutable (>>>), et ces exemples doivent être justes.
"""

import doctest
import inspect

import pytest

import geo
from geo import Point, dans_le_rayon, distance_km, format_coordonnees, plus_proche

MTL = Point("Montréal", 45.5019, -73.5674)
QC = Point("Québec", 46.8139, -71.2080)
OTT = Point("Ottawa", 45.4215, -75.6972)
TR = Point("Trois-Rivières", 46.3430, -72.5477)
SH = Point("Sherbrooke", 45.4042, -71.8929)
FONCTIONS = [distance_km, dans_le_rayon, plus_proche, format_coordonnees]


# ── 1. Comportement ────────────────────────────────────────────────────────
def test_distances():
    assert distance_km(MTL, QC) == 233.0
    assert distance_km(MTL, OTT) == 166.3


def test_dans_le_rayon_trie_par_distance():
    assert [p.nom for p in dans_le_rayon(MTL, [QC, OTT, TR, SH], 150)] == ["Trois-Rivières", "Sherbrooke"]


def test_plus_proche_ignore_l_origine():
    assert plus_proche(MTL, [MTL, QC, OTT, TR, SH]) == TR
    assert plus_proche(MTL, [MTL]) is None


def test_format():
    assert format_coordonnees(MTL) == "45.5019° N, 73.5674° O"


# ── 2. Documentation ───────────────────────────────────────────────────────
def test_le_module_est_documente():
    assert geo.__doc__ and len(geo.__doc__.strip()) > 40, "ajoutez une docstring de module"


def test_la_classe_point_est_documentee():
    assert Point.__doc__ and "Attributes:" in Point.__doc__


@pytest.mark.parametrize("fonction", FONCTIONS, ids=lambda f: f.__name__)
def test_docstring_google(fonction):
    doc = inspect.getdoc(fonction) or ""
    assert doc, f"{fonction.__name__} n'a pas de docstring"
    assert "Args:" in doc and "Returns:" in doc, "sections Args: et Returns: attendues"
    assert ">>>" in doc, "au moins un exemple exécutable (>>>) attendu"
    if "raise " in inspect.getsource(fonction):
        assert "Raises:" in doc, "la fonction lève une exception : section Raises: attendue"


def test_les_exemples_sont_justes():
    resultat = doctest.testmod(geo, optionflags=doctest.NORMALIZE_WHITESPACE)
    assert resultat.attempted >= len(FONCTIONS), "pas assez d'exemples (>>>)"
    assert resultat.failed == 0, "un exemple de la documentation est faux : lancez python -m doctest -v geo.py"
