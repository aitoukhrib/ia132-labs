"""Vérifie les livrables du lab 10, rangés dans labs/lab10-architecture/livrables/.

    pytest labs/lab10-architecture

Ces tests ne jugent pas la QUALITÉ de votre architecture (c'est le rôle du débriefing),
seulement que les livrables sont complets et cohérents : c'est là que l'IA se trompe le plus.
"""

import csv
import re
from collections import defaultdict
from pathlib import Path

import pytest

LIVRABLES = Path(__file__).resolve().parents[1] / "livrables"
FIBONACCI = {1, 2, 3, 5, 8, 13}
VELOCITE = 20


def lire(nom: str) -> str:
    chemin = LIVRABLES / nom
    assert chemin.exists(), f"livrable manquant : livrables/{nom}"
    return chemin.read_text(encoding="utf-8")


def backlog() -> list[dict]:
    lignes = list(csv.DictReader(lire("backlog.csv").splitlines()))
    assert lignes, "backlog.csv est vide"
    return lignes


# ── Architecture ───────────────────────────────────────────────────────────
def test_architecture_avec_diagramme_mermaid():
    texte = lire("architecture.md")
    assert re.search(r"```mermaid\s+(flowchart|graph|C4Container|C4Context)", texte), "diagramme Mermaid attendu"


def test_architecture_couvre_les_integrations_critiques():
    texte = lire("architecture.md").lower()
    for mot in ("paie", "entra", "allerg", "notification"):
        assert mot in texte, f"l'architecture doit traiter : {mot}"


def test_adr_complete():
    texte = lire("adr-001.md")
    for section in ("## Contexte", "## Décision", "## Alternatives", "## Conséquences"):
        assert section in texte, f"section manquante : {section}"
    assert re.search(r"(?i)statut\W+\s*(proposé|accepté)", texte)


# ── Backlog et planification ───────────────────────────────────────────────
def test_backlog_colonnes_et_taille():
    lignes = backlog()
    attendues = {"id", "epic", "story", "critere_acceptation", "points", "priorite", "sprint", "depend_de"}
    assert attendues <= set(lignes[0]), f"colonnes attendues : {sorted(attendues)}"
    assert len(lignes) >= 12, "au moins 12 user stories"


def test_stories_bien_formees():
    for us in backlog():
        assert re.match(r"(?i)en tant qu", us["story"]), f"{us['id']} : « En tant que … je veux … afin de … »"
        assert re.search(r"(?i)étant donné.*quand.*alors", us["critere_acceptation"]), f"{us['id']} : critère Gherkin attendu"


def test_points_en_suite_de_fibonacci():
    for us in backlog():
        assert int(us["points"]) in FIBONACCI, f"{us['id']} : {us['points']} n'est pas dans {sorted(FIBONACCI)}"


def test_aucune_story_de_13_points_dans_un_sprint():
    for us in backlog():
        if us["sprint"].strip():
            assert int(us["points"]) < 13, f"{us['id']} : 13 points = trop gros pour un sprint, découpez"


def test_capacite_des_sprints_respectee():
    charge = defaultdict(int)
    for us in backlog():
        if us["sprint"].strip():
            charge[int(us["sprint"])] += int(us["points"])
    trop = {s: p for s, p in charge.items() if p > VELOCITE}
    assert not trop, f"sprints au-delà de la vélocité ({VELOCITE} points) : {trop}"


def test_dependances_coherentes():
    lignes = backlog()
    sprint = {us["id"]: int(us["sprint"]) if us["sprint"].strip() else None for us in lignes}
    for us in lignes:
        for dep in filter(None, re.split(r"[ ;|]+", us["depend_de"].strip())):
            assert dep in sprint, f"{us['id']} dépend de {dep}, qui n'existe pas"
            if sprint[us["id"]] is not None:
                assert sprint[dep] is not None and sprint[dep] <= sprint[us["id"]], (
                    f"{us['id']} (sprint {sprint[us['id']]}) dépend de {dep} (sprint {sprint[dep]})"
                )


def test_le_pilote_tient_en_3_sprints():
    must = [us for us in backlog() if us["priorite"].upper() == "MUST"]
    assert must, "aucune story MUST"
    hors = [us["id"] for us in must if not us["sprint"].strip() or int(us["sprint"]) > 3]
    assert not hors, f"stories MUST hors des 3 premiers sprints : {hors}"


# ── Risques et dépendances ─────────────────────────────────────────────────
def test_registre_des_risques():
    lignes = [l for l in lire("risques.md").splitlines() if l.startswith("|") and not re.match(r"\|\s*-", l)]
    assert len(lignes) - 1 >= 5, "au moins 5 risques dans le tableau"
    entete = lignes[0].lower()
    for col in ("probabilit", "impact", "mesure"):
        assert col in entete, f"colonne attendue : {col}"


@pytest.mark.parametrize("paquet", ["django", "requests", "pyyaml", "lodash", "jsonwebtoken", "moment"])
def test_analyse_des_dependances(paquet):
    texte = lire("dependances.md").lower()
    assert paquet in texte, f"dependances.md doit traiter {paquet}"
    assert re.search(r"(?i)(pip-audit|npm audit|osv|github advisory)", texte), "citez l'outil qui a VÉRIFIÉ l'analyse"
