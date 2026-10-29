"""Test de mutation simplifié : vos tests détectent-ils ces 8 bogues ?

    python labs/lab08-tests/python/mutants.py

Chaque mutant modifie une ligne de panier.py dans une copie temporaire, puis relance vos tests.
Un mutant « tué » (vos tests échouent) est une bonne nouvelle ; un mutant « survivant »
révèle un comportement que vos tests ne vérifient pas.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ICI = Path(__file__).resolve().parent

MUTANTS = [
    ("quantité 0 acceptée", "if quantite < 1:", "if quantite < 0:"),
    ("maximum 99 décalé", "if nouvelle > QUANTITE_MAX:", "if nouvelle >= QUANTITE_MAX:"),
    ("stock non vérifié", "if nouvelle > produit.stock:", "if nouvelle > produit.stock + 1:"),
    ("retrait partiel faux", "quantite >= self.lignes[sku]", "quantite > self.lignes[sku]"),
    ("code sensible à la casse", 'if code.upper() not in', 'if code not in'),
    ("rabais de 1 %", "return self.sous_total() // 10", "return self.sous_total() // 100"),
    ("seuil de livraison strict", ">= SEUIL_LIVRAISON_GRATUITE", "> SEUIL_LIVRAISON_GRATUITE"),
    ("livraison facturée au panier vide", "if not self.lignes:\n            return 0", "if not self.lignes:\n            pass"),
]


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    source = (ICI / "panier.py").read_text(encoding="utf-8")
    survivants = 0
    for nom, avant, apres in MUTANTS:
        assert avant in source, f"mutant « {nom} » : ligne introuvable dans panier.py"
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copy(ICI / "test_panier.py", tmp)
            Path(tmp, "panier.py").write_text(source.replace(avant, apres, 1), encoding="utf-8")
            r = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "-o", "addopts=", tmp],
                capture_output=True, text=True, cwd=tmp,
            )
        tue = r.returncode != 0
        survivants += not tue
        print(f"  {'tué      ' if tue else 'SURVIVANT'}  {nom}")
    print(f"\nScore de mutation : {len(MUTANTS) - survivants}/{len(MUTANTS)}")
    return 0 if survivants == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
