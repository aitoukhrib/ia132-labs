"""Tests d'acceptation de SPEC.md (rouges au départ). Ne les modifiez pas.

Ajoutez VOS tests unitaires dans des fichiers séparés (test_modele.py, test_depot.py…).
"""

import csv
import io
import json
import re

import pytest

from taches.cli import main

LIGNE = re.compile(r"^\[( |x)\] +(\d+) ")


@pytest.fixture
def run(tmp_path):
    fichier = tmp_path / "taches.json"
    return lambda *argv: main(list(argv), fichier)


def ids(sortie: str) -> list[int]:
    return [int(m.group(2)) for l in sortie.splitlines() if (m := LIGNE.match(l))]


def test_ajouter_puis_lister(run):
    assert run("ajouter", "Préparer la démo", "--priorite", "haute") == (0, "Tâche 1 ajoutée : Préparer la démo")
    code, sortie = run("lister")
    assert code == 0 and ids(sortie) == [1]
    assert "Préparer la démo" in sortie and "haute" in sortie


def test_liste_vide(run):
    assert run("lister") == (0, "Aucune tâche.")


def test_persistance_entre_deux_appels(run, tmp_path):
    run("ajouter", "A")
    assert ids(main(["lister"], tmp_path / "taches.json")[1]) == [1]


def test_ordre_priorite_puis_echeance_puis_id(run):
    run("ajouter", "basse", "--priorite", "basse")
    run("ajouter", "normale sans échéance")
    run("ajouter", "normale tard", "--echeance", "2026-12-20")
    run("ajouter", "haute", "--priorite", "haute")
    run("ajouter", "normale tôt", "--echeance", "2026-11-10")
    assert ids(run("lister")[1]) == [4, 5, 3, 2, 1]


def test_terminer_masque_la_tache_sauf_avec_toutes(run):
    run("ajouter", "A")
    run("ajouter", "B")
    assert run("terminer", "1") == (0, "Tâche 1 terminée")
    assert ids(run("lister")[1]) == [2]
    sortie = run("lister", "--toutes")[1]
    assert ids(sortie) == [1, 2]
    assert sortie.splitlines()[0].startswith("[x]")


def test_les_identifiants_ne_sont_jamais_reutilises(run):
    run("ajouter", "A")
    run("ajouter", "B")
    assert run("supprimer", "2") == (0, "Tâche 2 supprimée")
    assert run("ajouter", "C")[1] == "Tâche 3 ajoutée : C"


def test_filtres_etiquette_et_priorite(run):
    run("ajouter", "A", "--etiquette", "ia", "--etiquette", "formation")
    run("ajouter", "B", "--etiquette", "perso", "--priorite", "haute")
    run("ajouter", "C", "--etiquette", "ia", "--priorite", "haute")
    assert ids(run("lister", "--etiquette", "ia")[1]) == [3, 1]
    assert ids(run("lister", "--priorite", "haute")[1]) == [2, 3]
    assert "#ia #formation" in run("lister")[1]


def test_en_retard_strictement_avant(run):
    run("ajouter", "hier", "--echeance", "2026-11-01")
    run("ajouter", "aujourd'hui", "--echeance", "2026-11-02")
    run("ajouter", "sans date")
    run("ajouter", "hier mais faite", "--echeance", "2026-10-01")
    run("terminer", "4")
    assert ids(run("en-retard", "--aujourdhui", "2026-11-02")[1]) == [1]


def test_export_json(run):
    run("ajouter", "A", "--etiquette", "ia", "--echeance", "2026-11-05")
    run("ajouter", "B")
    donnees = json.loads(run("exporter", "--format", "json")[1])
    assert donnees[0] == {"id": 1, "titre": "A", "priorite": "normale", "echeance": "2026-11-05",
                          "etiquettes": ["ia"], "terminee": False}
    assert donnees[1]["echeance"] is None


def test_export_csv(run):
    run("ajouter", "Titre, avec virgule", "--etiquette", "a", "--etiquette", "b")
    run("terminer", "1")
    lignes = list(csv.reader(io.StringIO(run("exporter", "--format", "csv")[1])))
    assert lignes[0] == ["id", "titre", "priorite", "echeance", "etiquettes", "terminee"]
    assert lignes[1] == ["1", "Titre, avec virgule", "normale", "", "a;b", "oui"]


@pytest.mark.parametrize(
    "argv",
    [
        ["ajouter", "X", "--priorite", "urgente"],
        ["ajouter", "X", "--echeance", "2026-13-45"],
        ["ajouter", "   "],
        ["voler"],
    ],
    ids=["priorité", "date", "titre vide", "commande"],
)
def test_arguments_invalides(run, argv):
    code, sortie = run(*argv)
    assert code == 2 and sortie.startswith("Erreur")


@pytest.mark.parametrize("commande", ["terminer", "supprimer"])
def test_tache_introuvable(run, commande):
    assert run(commande, "42") == (1, "Erreur : tâche 42 introuvable")
