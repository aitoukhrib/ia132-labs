from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt

RAYON_TERRE_KM = 6371.0


@dataclass(frozen=True)
class Point:
    nom: str
    lat: float
    lon: float


def distance_km(a: Point, b: Point) -> float:
    dlat = radians(b.lat - a.lat)
    dlon = radians(b.lon - a.lon)
    h = sin(dlat / 2) ** 2 + cos(radians(a.lat)) * cos(radians(b.lat)) * sin(dlon / 2) ** 2
    return round(2 * RAYON_TERRE_KM * asin(sqrt(h)), 1)


def dans_le_rayon(centre: Point, points: list[Point], rayon_km: float) -> list[Point]:
    if rayon_km < 0:
        raise ValueError("rayon négatif")
    return sorted((p for p in points if distance_km(centre, p) <= rayon_km), key=lambda p: distance_km(centre, p))


def plus_proche(origine: Point, points: list[Point]) -> Point | None:
    candidats = [p for p in points if p != origine]
    return min(candidats, key=lambda p: distance_km(origine, p), default=None)


def format_coordonnees(p: Point) -> str:
    ns = "N" if p.lat >= 0 else "S"
    eo = "E" if p.lon >= 0 else "O"
    return f"{abs(p.lat):.4f}° {ns}, {abs(p.lon):.4f}° {eo}"
