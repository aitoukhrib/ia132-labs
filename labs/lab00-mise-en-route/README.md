# Lab 00 · Mise en route

| Module | Durée | Langages |
| --- | --- | --- |
| Ouverture | 10 min | Python et/ou TypeScript |

## Objectif

Avoir un poste prêt pour les 2 jours : le dépôt cloné, les tests qui passent, l’assistant d’IA actif dans votre IDE.

## Étapes

1. **Forkez** le dépôt sur votre compte GitHub (bouton *Fork*), puis clonez **votre** fork :
   ```bash
   git clone https://github.com/<votre-compte>/ia132-labs.git
   cd ia132-labs
   ```
2. **Vérifiez vos outils** :
   ```bash
   python scripts/verifier_env.py
   ```
3. **Python** — créez un environnement virtuel et installez les outils :
   ```bash
   python -m venv .venv
   # Windows : .venv\Scripts\activate   ·   macOS / Linux : source .venv/bin/activate
   pip install -r requirements-dev.txt
   pytest labs/lab00-mise-en-route
   ```
4. **TypeScript** — rien à installer, Node 22.18+ exécute les fichiers `.ts` :
   ```bash
   npm run test:lab00
   ```
5. **Assistant d’IA** — ouvrez le chat de votre outil (Copilot, Cursor, JetBrains AI, Claude Code…) et demandez :
   > Résume ce dépôt en 5 lignes, puis liste les labs avec leur objectif.

   Vérifiez que la réponse cite bien les dossiers `labs/…` : l’assistant « voit » votre projet.
6. Notez le **nom du modèle** utilisé par votre assistant (sélecteur de modèle du chat).

## Livrable

- `pytest labs/lab00-mise-en-route` et/ou `npm run test:lab00` : **2 tests verts**.
- Votre assistant répond dans le chat en citant les fichiers du dépôt.

## Coincé ?

- `python` introuvable sous Windows : essayez `py`.
- Proxy d’entreprise : `pip install --proxy http://proxy:port -r requirements-dev.txt`.
- Pas de Copilot ? Un essai gratuit suffit ; sinon Cursor ou Claude Code font l’affaire pour tous les labs.
