# Module hérité : calcule le total, la livraison et la priorité des commandes.
# Écrit en 2017, « ça marche, on n'y touche pas ». Jusqu'à aujourd'hui.


def traiter(c, r, p):
    # c = commandes, r = region, p = client premium
    res = []
    for x in c:
        if x["statut"] != "annulee":
            if x["poids"] > 0:
                t = 0
                for l in x["lignes"]:
                    t = t + l["prix"] * l["qte"]
                if r == "QC":
                    if x["poids"] <= 2:
                        f = 8
                    else:
                        if x["poids"] <= 10:
                            f = 15
                        else:
                            f = 15 + (x["poids"] - 10) * 1.5
                elif r == "ON":
                    if x["poids"] <= 2:
                        f = 10
                    else:
                        if x["poids"] <= 10:
                            f = 18
                        else:
                            f = 18 + (x["poids"] - 10) * 1.75
                else:
                    if x["poids"] <= 2:
                        f = 14
                    else:
                        if x["poids"] <= 10:
                            f = 25
                        else:
                            f = 25 + (x["poids"] - 10) * 2.5
                if p:
                    if t > 100:
                        f = 0
                    else:
                        f = f / 2
                if t > 500:
                    pr = "haute"
                elif t > 100:
                    pr = "normale"
                else:
                    pr = "basse"
                res.append({"id": x["id"], "total": round(t + f, 2), "livraison": round(f, 2), "priorite": pr})
            else:
                print("poids invalide " + str(x["id"]))
    return res
