"""Outils de calcul de distances et de filtrage pour des points géographiques.

Les distances sont calculées en kilomètres en supposant une Terre sphérique.
"""

from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt

RAYON_TERRE_KM = 6371.0


@dataclass(frozen=True)
class Point:
    """Représente un lieu par son nom et ses coordonnées géographiques.

    Attributes:
        nom: Nom du lieu.
        lat: Latitude en degrés.
        lon: Longitude en degrés.
    """

    nom: str
    lat: float
    lon: float


def distance_km(a: Point, b: Point) -> float:
    """Calcule la distance sphérique entre deux points, arrondie au dixième.

    Le calcul utilise la formule de Haversine et un rayon terrestre de 6 371 km.

    Args:
        a: Premier point.
        b: Second point.

    Returns:
        Distance entre les points, en kilomètres.

    Examples:
        >>> distance_km(Point("Montréal", 45.5019, -73.5674), Point("Québec", 46.8139, -71.2080))
        233.0
    """
    dlat = radians(b.lat - a.lat)
    dlon = radians(b.lon - a.lon)
    h = sin(dlat / 2) ** 2 + cos(radians(a.lat)) * cos(radians(b.lat)) * sin(dlon / 2) ** 2
    return round(2 * RAYON_TERRE_KM * asin(sqrt(h)), 1)


def dans_le_rayon(centre: Point, points: list[Point], rayon_km: float) -> list[Point]:
    """Renvoie les points situés dans un rayon, triés par distance croissante.

    La limite du rayon est incluse. En cas d'égalité, l'ordre d'entrée est conservé.

    Args:
        centre: Point servant de centre de recherche.
        points: Points à examiner.
        rayon_km: Rayon de recherche, en kilomètres.

    Returns:
        Points dont la distance au centre est inférieure ou égale au rayon,
        triés du plus proche au plus éloigné.

    Raises:
        ValueError: Si le rayon est négatif.

    Examples:
        >>> centre = Point("Centre", 0, 0)
        >>> dans_le_rayon(centre, [Point("Ailleurs", 0, 1)], 0)
        []
    """
    if rayon_km < 0:
        raise ValueError("rayon négatif")
    return sorted((p for p in points if distance_km(centre, p) <= rayon_km), key=lambda p: distance_km(centre, p))


def plus_proche(origine: Point, points: list[Point]) -> Point | None:
    """Trouve le point le plus proche, en excluant l'origine elle-même.

    Args:
        origine: Point depuis lequel calculer les distances.
        points: Points candidats.

    Returns:
        Le candidat le plus proche, ou ``None`` si aucun candidat ne reste.

    Examples:
        >>> origine = Point("Départ", 0, 0)
        >>> plus_proche(origine, [origine]) is None
        True
    """
    candidats = [p for p in points if p != origine]
    return min(candidats, key=lambda p: distance_km(origine, p), default=None)


def format_coordonnees(p: Point) -> str:
    """Formate les coordonnées d'un point avec les directions cardinales.

    Args:
        p: Point dont les coordonnées doivent être formatées.

    Returns:
        Les latitudes et longitudes absolues, suivies de leur direction.

    Examples:
        >>> format_coordonnees(Point("Montréal", 45.5019, -73.5674))
        '45.5019° N, 73.5674° O'
    """
    ns = "N" if p.lat >= 0 else "S"
    eo = "E" if p.lon >= 0 else "O"
    return f"{abs(p.lat):.4f}° {ns}, {abs(p.lon):.4f}° {eo}"
