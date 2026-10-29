"""Critères d'acceptation du pipeline CI (rouges tant que .github/workflows/ci.yml n'existe pas).

    pytest labs/lab09-ci/python/test_workflow.py
"""

import re
from pathlib import Path

RACINE = Path(__file__).resolve().parents[3]
WORKFLOW = RACINE / ".github" / "workflows" / "ci.yml"


def contenu() -> str:
    assert WORKFLOW.exists(), "créez .github/workflows/ci.yml (partez de labs/lab09-ci/ci-a-completer.yml)"
    return WORKFLOW.read_text(encoding="utf-8")


def test_declenche_sur_push_et_pull_request():
    yml = contenu()
    assert re.search(r"^on:", yml, re.M)
    assert "push" in yml and "pull_request" in yml


def test_matrice_de_versions_python():
    yml = contenu()
    assert "matrix" in yml and re.search(r"python-version", yml)
    assert len(re.findall(r"['\"]?3\.1\d['\"]?", yml)) >= 2, "au moins 2 versions de Python dans la matrice"


def test_lint_puis_tests_avec_seuil_de_couverture():
    yml = contenu()
    assert "ruff check" in yml
    assert "pytest" in yml and "labs/lab09-ci" in yml
    assert re.search(r"--cov-fail-under[= ]\d+", yml), "seuil de couverture attendu (--cov-fail-under=80)"


def test_tests_typescript():
    yml = contenu()
    assert "setup-node" in yml and "node --test" in yml


def test_cache_des_dependances():
    assert re.search(r"cache:\s*['\"]?pip", contenu()), "activez le cache pip de setup-python"


def test_pas_de_secret_en_clair():
    assert not re.search(r"(?i)(password|token|secret)\s*[:=]\s*['\"]?\w{6,}", contenu())
