# Module `geo`

Outils Python pour représenter des lieux et effectuer des calculs géographiques
simples. Le module fournit la distance entre deux points, la recherche de points
dans un rayon, la recherche du point le plus proche et le formatage de
coordonnées.

## Installation

Le module utilise uniquement la bibliothèque standard de Python 3.10 ou plus
récent. Aucune installation de dépendance n'est nécessaire pour l'utiliser.

Depuis la racine du dépôt, les tests nécessitent `pytest` :

```powershell
python -m pytest .\labs\lab06-documentation\python
```

Pour vérifier les exemples intégrés aux docstrings :

```powershell
python -m doctest -v .\labs\lab06-documentation\python\geo.py
```

## Exemple

Depuis le dossier `labs/lab06-documentation/python`, exécutez cet exemple dans
un interpréteur Python :

```python
from geo import Point, distance_km, format_coordonnees

montreal = Point("Montréal", 45.5019, -73.5674)
quebec = Point("Québec", 46.8139, -71.2080)

print(distance_km(montreal, quebec))  # 233.0
print(format_coordonnees(montreal))   # 45.5019° N, 73.5674° O
```

## Limites

- Les distances utilisent la formule de Haversine avec une Terre sphérique de
  rayon 6 371 km ; elles ne représentent pas une distance routière et ne tiennent
  pas compte du relief.
- Les résultats de distance sont arrondis au dixième de kilomètre.
- `Point` ne valide pas les plages des latitudes et longitudes.
- `dans_le_rayon` refuse un rayon négatif avec `ValueError`. Les autres fonctions
  ne valident pas les valeurs fournies.
