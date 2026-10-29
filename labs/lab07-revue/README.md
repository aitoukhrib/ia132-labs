# Lab 07 · Revue de code assistée par l’IA

| Module | Durée | Langages |
| --- | --- | --- |
| 4 · Revue de code et documentation automatisée | 25 min | Python ou TypeScript |

## Objectif

Mener une **revue de pull request** avec l’IA et un analyseur statique, **classer** les constats par gravité, trier les faux positifs, puis corriger les problèmes bloquants.

## Point de départ

- `notes_service.py` / `notes-service.ts` : la PR n° 42 « Service de notes, prêt pour la prod ». Les tests fonctionnels passent.
- `grille-revue.md` : la grille de gravité et le gabarit de commentaire.
- `.github/copilot-instructions.md` (racine du dépôt) : les conventions de l’équipe, lues par Copilot.

## Étapes

1. **Revue humaine éclair (3 min)** — Lisez le fichier **sans IA** et notez ce qui vous frappe.
2. **Revue par l’IA (7 min)** — Demandez :
   > Fais la revue de ce fichier comme un relecteur senior, en suivant grille-revue.md. Pour chaque constat : ligne, gravité (Bloquant / Majeur / Mineur / Suggestion), problème, correction proposée. Termine par un verdict : approuver ou demander des changements.

   Puis l’analyseur statique :
   ```bash
   ruff check labs/lab07-revue/python                  # règles S (bandit) : SQL, MD5, secret en dur…
   ```
3. **Trier (5 min)** — Comparez les trois listes (vous, l’IA, `ruff`). Marquez chaque constat de l’IA **vrai / faux positif / discutable**. Puis lancez les tests de sécurité :
   ```bash
   pytest labs/lab07-revue                             # ou : npm run test:lab07
   ```
   Votre revue avait-elle vu les 5 problèmes que les tests révèlent ?
4. **Corriger les bloquants (10 min)** — Requêtes paramétrées, empreinte de mot de passe salée et lente (`hashlib.pbkdf2_hmac`, `scrypt`), contrôle du propriétaire, secret lu dans l’environnement. Un commit par correction.

## Livrable

- `REVUE.md` : vos constats classés (tableau), avec la colonne « trouvé par : moi / IA / ruff ».
- Les 9 tests au vert.

## Pièges à observer

- L’IA signale 15 « problèmes », dont la moitié de style : un relecteur trie, il ne recopie pas.
- Elle peut manquer le **contrôle d’accès** (`lire_note` ne vérifie pas le propriétaire) : aucun outil statique ne le voit, c’est une règle métier.
- `except Exception: return None` cache les erreurs (et ici l’injection SQL).

## Bonus

Sur votre fork, ouvrez une vraie PR avec ce fichier et demandez une revue à Copilot (*Reviewers → Copilot*). Comparez avec votre `REVUE.md`.
