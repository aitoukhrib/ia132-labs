"""Tests d'intégration : un VRAI serveur HTTP, de vraies requêtes. À compléter (voir README).

La fixture `serveur` démarre l'API sur un port libre et l'arrête à la fin du module.
"""

import json
import threading
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

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
    donnees = (
        corps
        if isinstance(corps, bytes)
        else json.dumps(corps).encode() if corps is not None else None
    )
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


def test_creer_puis_suivre_un_lien_redirige_vers_url_originale(serveur):
    url = "https://exemple.ca/article"
    statut, _, corps = requete(serveur, "POST", "/liens", {"url": url})

    assert statut == 201
    assert corps["url"] == url
    assert len(corps["code"]) == 6

    statut, entetes, corps = requete(serveur, "GET", f"/l/{corps['code']}")
    assert statut == 302
    assert entetes["Location"] == url
    assert corps is None


def test_statistiques_comptent_trois_visites(serveur):
    statut, _, creation = requete(
        serveur, "POST", "/liens", {"url": "https://exemple.ca/stats"}
    )
    assert statut == 201

    for _ in range(3):
        statut, _, _ = requete(serveur, "GET", f"/l/{creation['code']}")
        assert statut == 302

    statut, _, stats = requete(serveur, "GET", f"/stats/{creation['code']}")
    assert statut == 200
    assert stats == {
        "code": creation["code"],
        "url": "https://exemple.ca/stats",
        "clics": 3,
    }


@pytest.mark.parametrize(
    "corps",
    [
        {"url": "ftp://exemple.ca"},
        {"url": "https://"},
        {},
    ],
)
def test_creation_avec_url_invalide_renvoie_400(serveur, corps):
    statut, _, reponse = requete(serveur, "POST", "/liens", corps)

    assert statut == 400
    assert reponse == {"erreur": "url invalide : http(s)://… attendu"}


def test_creation_avec_json_malforme_renvoie_400(serveur):
    statut, _, corps = requete(serveur, "POST", "/liens", b'{"url":')

    assert statut == 400
    assert corps == {"erreur": "JSON invalide"}


@pytest.mark.parametrize("chemin", ["/l/inconnu", "/stats/inconnu"])
def test_code_inconnu_renvoie_404(serveur, chemin):
    statut, _, corps = requete(serveur, "GET", chemin)

    assert statut == 404
    assert corps == {"erreur": "lien inconnu"}


def test_route_inconnue_renvoie_404(serveur):
    statut, _, corps = requete(serveur, "GET", "/route-inconnue")

    assert statut == 404
    assert corps == {"erreur": "route inconnue"}


def test_deux_cents_creations_concurrentes_produisent_des_codes_uniques(serveur):
    urls = [f"https://exemple.ca/{i}" for i in range(200)]

    def creer(url):
        return requete(serveur, "POST", "/liens", {"url": url})

    with ThreadPoolExecutor(max_workers=20) as pool:
        reponses = list(pool.map(creer, urls))

    assert all(statut == 201 for statut, _, _ in reponses)
    codes = [corps["code"] for _, _, corps in reponses]
    assert len(set(codes)) == 200
    assert all(len(code) == 6 and code.isalnum() for code in codes)
