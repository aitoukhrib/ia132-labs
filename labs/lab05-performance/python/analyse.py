"""Lab 05 — Analyse d'une liste de diffusion.

Correct, testé… et beaucoup trop lent sur les 200 000 abonnés de la vraie liste.
"""


def normaliser(courriel: str) -> str:
    return courriel.strip().lower()


def dedoublonner(courriels: list[str]) -> list[str]:
    """Courriels uniques, normalisés, dans l'ordre de leur PREMIÈRE apparition."""
    resultat = []
    for c in courriels:
        c = normaliser(c)
        if c not in resultat:
            resultat.append(c)
    return resultat


def top_domaines(courriels: list[str], n: int = 3) -> list[tuple[str, int]]:
    """Les n domaines les plus fréquents : (domaine, nombre), par nombre décroissant puis par nom."""
    domaines = [normaliser(c).split("@")[1] for c in courriels]
    comptes = []
    for d in dedoublonner(domaines):
        comptes.append((d, domaines.count(d)))
    comptes.sort(key=lambda x: (-x[1], x[0]))
    return comptes[:n]


def communs(liste_a: list[str], liste_b: list[str]) -> list[str]:
    """Courriels présents dans les deux listes, sans doublon, dans l'ordre de liste_a."""
    b = [normaliser(c) for c in liste_b]
    return [c for c in dedoublonner(liste_a) if c in b]
