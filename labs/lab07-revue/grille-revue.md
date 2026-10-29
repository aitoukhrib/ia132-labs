# Grille de revue de code

## Gravité

| Niveau | Définition | Exemple | Effet sur la PR |
| --- | --- | --- | --- |
| **Bloquant** | Faille de sécurité, perte de données, comportement faux | Injection SQL, secret en dur | Demander des changements |
| **Majeur** | Bogue probable, maintenance coûteuse | Exception avalée, absence de test | Corriger avant fusion |
| **Mineur** | Lisibilité, convention | Nom peu clair, type manquant | Corriger si simple |
| **Suggestion** | Amélioration facultative | Extraire une fonction | Au choix de l’auteur |

## Points de contrôle

1. **Sécurité** — entrées non fiables (SQL, chemins, commandes), secrets, cryptographie, contrôle d’accès.
2. **Exactitude** — cas limites, erreurs gérées et non avalées, transactions.
3. **Tests** — le changement est-il couvert ? Les tests échouent-ils si on casse le code ?
4. **Lisibilité** — noms, types, taille des fonctions, commentaires utiles.
5. **Conventions** — celles du dépôt (`.github/copilot-instructions.md`).

## Gabarit de commentaire

```text
[Bloquant] notes_service.py:24 · Injection SQL
Le courriel est inséré tel quel dans la requête : « ana@x.ca' -- » contourne le mot de passe.
Correction : requête paramétrée, execute("… where email = ?", (email,)).
```

Un bon commentaire : **où**, **quoi**, **pourquoi c’est grave**, **comment corriger**. Il critique le code, jamais la personne.
