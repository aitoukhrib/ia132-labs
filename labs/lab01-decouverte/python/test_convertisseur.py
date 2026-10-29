"""Étapes 1 à 3 : ces tests doivent tous passer."""

import pytest

from convertisseur import (
    celsius_vers_fahrenheit,
    convertir,
    fahrenheit_vers_celsius,
    km_vers_miles,
    miles_vers_km,
)


@pytest.mark.parametrize(("c", "f"), [(0, 32), (100, 212), (-40, -40), (37, 98.6)])
def test_celsius_vers_fahrenheit(c, f):
    assert celsius_vers_fahrenheit(c) == pytest.approx(f)


@pytest.mark.parametrize(("f", "c"), [(32, 0), (212, 100), (-40, -40)])
def test_fahrenheit_vers_celsius(f, c):
    assert fahrenheit_vers_celsius(f) == pytest.approx(c)


def test_sous_le_zero_absolu():
    with pytest.raises(ValueError):
        celsius_vers_fahrenheit(-300)
    with pytest.raises(ValueError):
        fahrenheit_vers_celsius(-500)


def test_distances():
    assert km_vers_miles(1.609344) == pytest.approx(1)
    assert miles_vers_km(26.2) == pytest.approx(42.165, abs=1e-3)


def test_distance_negative():
    with pytest.raises(ValueError):
        km_vers_miles(-1)
    with pytest.raises(ValueError):
        miles_vers_km(-0.5)


def test_convertir_aiguille():
    assert convertir(100, "C", "F") == pytest.approx(212)
    assert convertir(10, "km", "mi") == pytest.approx(6.2137, abs=1e-4)
    assert convertir(5, "mi", "mi") == 5


def test_convertir_paire_invalide():
    with pytest.raises(ValueError):
        convertir(1, "C", "km")
