# Rapport d’incidents · module Réservations

Tickets ouverts par le support cette semaine. Ils décrivent des **symptômes**, pas des causes.

---

## INC-101 · Le tableau de bord plante (bloquant)

> « Depuis ce matin, le tableau de bord d’occupation ne s’affiche plus. La salle B-204 n’a aucune réservation cette semaine, c’est peut-être lié ? »

Version Python — `python tableau_de_bord.py` :

```text
Occupation des salles · lundi 2 novembre
  A-101 : 60%
  A-102 : 10%
Traceback (most recent call last):
  File "labs/lab04-debogage/python/tableau_de_bord.py", line 26, in <module>
    afficher()
  File "labs/lab04-debogage/python/tableau_de_bord.py", line 22, in afficher
    print(f"  {salle} : {taux_occupation(RESERVATIONS, salle):.0%}")
                         ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "labs/lab04-debogage/python/reservations.py", line 48, in taux_occupation
    return round(heures / (heures_ouvertes * len(jours)), 2)
                 ~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ZeroDivisionError: division by zero
```

Version TypeScript — `node labs/lab04-debogage/typescript/tableau-de-bord.ts` affiche `B-204 : NaN %`.

## INC-102 · Une réservation apparaît deux fois (majeur)

> « Dans la liste paginée, la dernière réservation de la page 1 réapparaît en haut de la page 2. Et la page 3 en a 6 au lieu de 5. »

## INC-103 · Impossible de réserver à 10 h (majeur)

> « Je veux la salle A-101 de 10 h à 11 h. La réservation précédente se termine à 10 h pile, mais le système refuse : “salle occupée”. »

## INC-104 · Un cent d’écart sur la facture (mineur)

> « 1 h 30 à 31,15 $/h, ça fait 46,725 $, donc 46,73 $. La facture indique 46,72 $. Le service des finances n’est pas content. »

## INC-105 · Réservation de deux jours facturée 2 heures (majeur, bonus)

> « Salle C-310 réservée du vendredi 9 h au samedi 11 h pour un hackathon : 26 heures. Facturé : 2 heures. »
