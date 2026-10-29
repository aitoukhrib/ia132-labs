# Lab 01 · Les 4 modes de votre assistant

| Module | Durée | Langages |
| --- | --- | --- |
| 1 · Panorama des assistants de codage | 20 min | Python ou TypeScript |

## Objectif

Utiliser les **4 modes d’interaction** d’un assistant de codage — complétion en ligne, chat, édition, agent — et savoir lequel choisir selon la tâche.

## Point de départ

- `python/convertisseur.py` ou `typescript/convertisseur.ts` : 5 fonctions avec leur signature et leur documentation, mais sans code.
- Les tests des étapes 1 à 3 (`test_convertisseur.py` / `convertisseur.test.ts`) et de l’étape 4 (`test_cli.py` / `cli.test.ts`) échouent tous au départ.

```bash
pytest labs/lab01-decouverte           # Python
npm run test:lab01                     # TypeScript
```

## Étapes

1. **Complétion en ligne (5 min)** — Effacez la ligne `raise NotImplementedError` (ou `throw`) de `celsius_vers_fahrenheit`, placez le curseur dans la fonction et attendez la suggestion grisée. `Tab` pour accepter, `Échap` pour refuser. Faites de même pour les 3 conversions suivantes. **Lisez chaque suggestion avant de l’accepter.**
2. **Chat (5 min)** — Sélectionnez `fahrenheit_vers_celsius` et demandez :
   > Explique cette fonction. Quels cas limites ne sont pas couverts par les tests ?

   Notez une idée de cas limite pertinente… et une qui ne l’est pas.
3. **Édition (5 min)** — Ouvrez le mode édition (Copilot Edits, Cursor `Ctrl+K`, JetBrains *AI Actions*) et demandez :
   > Implémente convertir() avec un dictionnaire de fonctions plutôt qu’une suite de if. Lève ValueError pour une paire non prise en charge.

   Relisez le **diff** proposé avant de l’accepter. Lancez les tests : étapes 1 à 3 au vert.
4. **Agent (5 min)** — Passez en mode agent (Copilot *Agent*, Cursor *Agent*, Claude Code, Junie) et demandez :
   > Ajoute une fonction main(argv) qui rend le module utilisable en ligne de commande, de façon à faire passer les tests de test_cli. Lance les tests pour vérifier.

   Observez : quels fichiers l’agent lit-il ? Quelles commandes lance-t-il ? Vous demande-t-il votre accord ?

## Livrable

- Tous les tests du lab au vert.
- Un fichier `NOTES.md` dans le dossier du lab : pour chaque mode, **une phrase** « utile pour… / à éviter pour… ».

## Pièges à observer

- La complétion invente parfois une constante au lieu d’utiliser `KM_PAR_MILE` déjà définie.
- En mode agent, l’outil peut modifier les **tests** pour les faire passer : refusez, et dites-le dans votre demande.

## Bonus

Demandez au chat la même implémentation avec **deux modèles différents** (sélecteur de modèle) et comparez : longueur, style, cas limites.
