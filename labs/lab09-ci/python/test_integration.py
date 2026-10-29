"""Tests d'intégration : un VRAI serveur HTTP, de vraies requêtes. À compléter (voir README).

La fixture `serveur` démarre l'API sur un port libre et l'arrête à la fin du module.
"""

import json
import threading
import urllib.error
import urllib.request

import pytest

from api import creer_serveur


class SansRedirection(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None  # pour lire la réponse 302 elle-même


ouvrir = urllib.request.build_opener(SansRedirection).open


@pytest.fixture(scope="module")
def serveur():
    srv = creer_serveur()
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


def requete(base, methode, chemin, corps=None):
    """Retourne (statut, en-têtes, corps JSON ou None) sans lever d'exception sur 4xx."""
    donnees = json.dumps(corps).encode() if corps is not None else None
    req = urllib.request.Request(base + chemin, data=donnees, method=methode, headers={"Content-Type": "application/json"})
    try:
        with ouvrir(req, timeout=5) as r:
            brut = r.read()
            return r.status, r.headers, json.loads(brut) if brut else None
    except urllib.error.HTTPError as e:
        brut = e.read()
        return e.code, e.headers, json.loads(brut) if brut else None


def test_sante(serveur):
    statut, _, corps = requete(serveur, "GET", "/sante")
    assert (statut, corps) == (200, {"statut": "ok"})


# À vous : demandez à l'IA les scénarios d'intégration, puis écrivez-les ici.
# Pistes : créer puis suivre un lien (201 → 302 + Location), statistiques après 3 visites,
# URL invalide (400), JSON invalide (400), code inconnu (404), créations concurrentes.
