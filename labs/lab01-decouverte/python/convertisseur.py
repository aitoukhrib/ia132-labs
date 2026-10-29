"""Lab 01 — Convertisseur d'unités.

Complétez chaque fonction avec votre assistant, en suivant les 4 étapes du README :
complétion en ligne, chat, édition, agent.
"""

ZERO_ABSOLU_C = -273.15
KM_PAR_MILE = 1.609344


def celsius_vers_fahrenheit(c: float) -> float:
    """Convertit des degrés Celsius en degrés Fahrenheit.

    Lève ValueError si la température est sous le zéro absolu.
    """
    raise NotImplementedError


def fahrenheit_vers_celsius(f: float) -> float:
    """Convertit des degrés Fahrenheit en degrés Celsius.

    Lève ValueError si le résultat est sous le zéro absolu.
    """
    raise NotImplementedError


def km_vers_miles(km: float) -> float:
    """Convertit des kilomètres en miles. Lève ValueError si la distance est négative."""
    raise NotImplementedError


def miles_vers_km(miles: float) -> float:
    """Convertit des miles en kilomètres. Lève ValueError si la distance est négative."""
    raise NotImplementedError


def convertir(valeur: float, de: str, vers: str) -> float:
    """Convertit `valeur` de l'unité `de` vers l'unité `vers`.

    Unités prises en charge : "C", "F", "km", "mi".
    Même unité des deux côtés : la valeur est retournée telle quelle.
    Paire non prise en charge (ex. "C" vers "km") : ValueError.
    """
    raise NotImplementedError
