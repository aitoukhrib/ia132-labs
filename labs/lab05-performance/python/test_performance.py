"""Budgets de temps : rouges au départ, verts une fois l'algorithme corrigé.

Les budgets sont larges (un algorithme linéaire tient en quelques millisecondes) :
si votre poste est très lent, lancez d'abord bench.py pour comparer.
"""

import time

from analyse import communs, dedoublonner
from bench import generer

N = 10_000
BUDGET_S = 0.25


def duree(f, *args) -> float:
    t0 = time.perf_counter()
    f(*args)
    return time.perf_counter() - t0


def test_dedoublonner_10_000_courriels_en_moins_de_250_ms():
    assert duree(dedoublonner, generer(N, 1)) < BUDGET_S


def test_communs_10_000_courriels_en_moins_de_250_ms():
    assert duree(communs, generer(N, 1), generer(N, 2)) < BUDGET_S
