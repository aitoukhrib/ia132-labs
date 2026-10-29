# Labs IA132 · IA pour développeurs : code assisté et programmation intelligente

Exercices pratiques de la formation **IA132** (Technologia, 2 jours). Chaque lab est **indépendant** : un dossier, un objectif, un point de départ, des tests qui disent quand c’est fini. Chaque lab existe en **Python** et en **TypeScript** : choisissez votre langage.

## Démarrage

```bash
# 1. Forkez ce dépôt (bouton Fork), puis clonez VOTRE fork
git clone https://github.com/<votre-compte>/ia132-labs.git
cd ia132-labs

# 2. Vérifiez votre poste
python scripts/verifier_env.py

# 3. Python : environnement virtuel + outils
python -m venv .venv
.venv\Scripts\activate            # macOS / Linux : source .venv/bin/activate
pip install -r requirements-dev.txt

# 4. TypeScript : rien à installer (Node 22.18+ exécute les .ts directement)
npm run test:lab00
```

Prérequis : Git, un IDE (VS Code, IntelliJ, PyCharm…), Python 3.10+ et/ou Node.js 22.18+, et un assistant de code : GitHub Copilot (un essai gratuit suffit), Cursor, JetBrains AI Assistant ou Claude Code.

## Les labs

| Lab | Module | Durée | Objectif |
| --- | --- | --- | --- |
| [00 · Mise en route](labs/lab00-mise-en-route/) | Ouverture | 10 min | Poste prêt : dépôt cloné, tests verts, assistant actif |
| [01 · Les 4 modes de l’assistant](labs/lab01-decouverte/) | 1 · Panorama des assistants | 20 min | Complétion, chat, édition, agent : savoir lequel choisir |
| [02 · Générer depuis une spécification](labs/lab02-generation/) | 2 · Génération et réécriture | 25 min | Prompt structuré + tests d’acceptation comme critère |
| [03 · Refactoriser du code hérité](labs/lab03-refactorisation/) | 2 · Génération et réécriture | 25 min | Petites étapes, tests de caractérisation, un commit par étape |
| [04 · Chasse aux bogues](labs/lab04-debogage/) | 3 · Débogage et optimisation | 25 min | Reproduire, faire expliquer, corriger, prouver |
| [05 · Optimiser et mesurer](labs/lab05-performance/) | 3 · Débogage et optimisation | 20 min | Complexité O(n²) → O(n), gain prouvé par la mesure |
| [06 · Documentation automatisée](labs/lab06-documentation/) | 4 · Revue et documentation | 20 min | Docstrings / TSDoc conformes, exemples vérifiés, README |
| [07 · Revue de code assistée](labs/lab07-revue/) | 4 · Revue et documentation | 25 min | Revue d’une PR : IA + analyseur, tri, correction des failles |
| [08 · Tests unitaires utiles](labs/lab08-tests/) | 5 · Tests et assurance qualité | 30 min | Couverture des branches et score de mutation 8/8 |
| [09 · Intégration, charge et CI](labs/lab09-ci/) | 5 · Tests et assurance qualité | 35 min | Tests d’intégration, test de charge, pipeline GitHub Actions |
| [10 · Architecture et planification](labs/lab10-architecture/) | 6 · Planification et architecture | 35 min | Diagramme, ADR, backlog estimé, risques, audit des dépendances |
| [11 · Projet final](labs/lab11-projet-final/) | 7 · Ateliers pratiques | 55 min | Un outil complet avec un agent : plan, code, tests, doc, PR |

Chaque `README.md` de lab suit le même plan : **objectif · point de départ · étapes · livrable · pièges à observer · bonus**. Le guide PDF remis en formation reprend ces fiches.

## Lancer les tests d’un lab

```bash
pytest labs/lab04-debogage          # Python
npm run test:lab04                  # TypeScript
```

Au départ, la plupart des tests sont **rouges** : c’est normal, c’est l’exercice. Un lab est terminé quand ses tests sont verts **sans avoir modifié les tests** (sauf consigne contraire).

## Règles du jeu

- Travaillez sur votre **fork**, une branche par lab si vous le souhaitez (`git switch -c lab04`).
- **Relisez** tout ce que l’IA propose avant de l’accepter ; lancez les tests après chaque changement.
- Aucune donnée confidentielle de votre entreprise dans ces exercices.
- `.github/copilot-instructions.md` contient les conventions du dépôt : votre assistant les lit.
