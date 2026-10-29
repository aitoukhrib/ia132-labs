from bonjour import saluer


def test_saluer_avec_un_nom():
    assert saluer("Ada") == "Bonjour Ada, bienvenue à la formation IA132 !"


def test_saluer_sans_nom():
    assert saluer("   ") == "Bonjour inconnu, bienvenue à la formation IA132 !"
