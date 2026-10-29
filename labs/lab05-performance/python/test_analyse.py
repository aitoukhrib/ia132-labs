"""Le comportement à préserver pendant l'optimisation. Ces tests sont verts au départ."""

from analyse import communs, dedoublonner, top_domaines

LISTE = [" Ana@Exemple.ca", "bob@test.com", "ana@exemple.ca", "Zoe@exemple.ca", "BOB@test.com ", "eve@autre.org"]


def test_dedoublonner_normalise():
    assert dedoublonner(["  Ana@X.ca ", "ana@x.ca"]) == ["ana@x.ca"]


def test_dedoublonner_garde_l_ordre_de_premiere_apparition():
    assert dedoublonner(LISTE) == ["ana@exemple.ca", "bob@test.com", "zoe@exemple.ca", "eve@autre.org"]


def test_dedoublonner_liste_vide():
    assert dedoublonner([]) == []


def test_top_domaines_compte_les_occurrences():
    assert top_domaines(LISTE, 2) == [("exemple.ca", 3), ("test.com", 2)]


def test_top_domaines_egalite_par_ordre_alphabetique():
    assert top_domaines(["a@b.ca", "c@a.ca"], 2) == [("a.ca", 1), ("b.ca", 1)]


def test_communs_dans_l_ordre_de_la_premiere_liste():
    a = ["zoe@exemple.ca", "BOB@test.com", "nouveau@x.ca", "bob@test.com"]
    assert communs(a, LISTE) == ["zoe@exemple.ca", "bob@test.com"]
