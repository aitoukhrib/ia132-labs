"""Mesure le temps des 3 fonctions quand la taille de la liste double.

    python bench.py            # tailles 2 000, 4 000, 8 000
    python bench.py 50000      # une seule taille

Si le temps est multiplié par ~4 quand la taille double, l'algorithme est quadratique, O(n²).
"""

import random
import sys
import time

from analyse import communs, dedoublonner, top_domaines


def generer(n: int, graine: int = 42) -> list[str]:
    rnd = random.Random(graine)
    domaines = [f"domaine{i}.ca" for i in range(200)]
    return [f"  Personne{rnd.randrange(n // 2)}@{rnd.choice(domaines).upper()} " for _ in range(n)]


def chrono(f, *args) -> float:
    t0 = time.perf_counter()
    f(*args)
    return time.perf_counter() - t0


def main() -> None:
    tailles = [int(sys.argv[1])] if len(sys.argv) > 1 else [2_000, 4_000, 8_000]
    print(f"{'taille':>8} {'dedoublonner':>14} {'top_domaines':>14} {'communs':>10}")
    for n in tailles:
        a, b = generer(n, 1), generer(n, 2)
        print(
            f"{n:>8} {chrono(dedoublonner, a):>13.3f}s {chrono(top_domaines, a):>13.3f}s "
            f"{chrono(communs, a, b):>9.3f}s"
        )


if __name__ == "__main__":
    main()
