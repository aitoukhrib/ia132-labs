# Lab 06 · Documenter automatiquement… et vérifier ce qui est écrit

| Module | Durée | Langages |
| --- | --- | --- |
| 4 · Revue de code et documentation automatisée | 20 min | Python ou TypeScript |

## Objectif

Générer une documentation **conforme à une convention** (docstrings Google / TSDoc), un README de module et un journal des modifications, puis **vérifier** que la documentation dit vrai.

## Point de départ

- `geo.py` / `geo.ts` : 4 fonctions géographiques, **zéro** commentaire.
- Les tests de comportement sont verts ; les tests de documentation sont rouges : ils exigent `Args:` / `Returns:` / `Raises:` et un exemple exécutable (Python, vérifié par `doctest`), ou `@param` / `@returns` / `@throws` / `@example` (TypeScript).

```bash
pytest labs/lab06-documentation              # ou : npm run test:lab06
python -m doctest -v labs/lab06-documentation/python/geo.py
```

## Étapes

1. **Convention d’abord (3 min)** — Demandez à l’assistant de documenter **une** fonction en précisant la convention (« docstring au format Google, en français, avec un exemple doctest exécutable »). Comparez avec le même prompt **sans** préciser la convention.
2. **Tout le module (7 min)** — Documentez le module, la classe `Point` et les 4 fonctions (commande `/doc` de Copilot, *Generate documentation* de JetBrains, ou le chat). Lancez les tests.
3. **Vérifier (5 min)** — Les exemples sont-ils justes ? Python : `doctest` le prouve. TypeScript : exécutez un exemple à la main. Cherchez une phrase **fausse** ou invérifiable (ex. « précision au mètre »).
4. **README et changelog (5 min)** — Demandez un `README.md` pour ce module (but, installation, exemple, limites), puis :
   > À partir de `git log --oneline -15`, rédige une entrée de CHANGELOG au format Keep a Changelog (Ajouté / Modifié / Corrigé).

## Livrable

- Tous les tests du lab au vert.
- `README.md` du module, revu par vous (au moins une correction de votre part).

## Pièges à observer

- L’IA paraphrase le code (« incrémente i de 1 ») au lieu d’expliquer le **pourquoi** (haversine, Terre sphérique, bord inclus).
- Les exemples inventés : `distance_km(Montréal, Québec) == 250` « à peu près » → le doctest échoue.
- La documentation qui promet un comportement que le code n’a pas (ex. « lève une erreur si la liste est vide »).

## Bonus

Générez la doc HTML : `python -m pydoc -w geo` ou `npx typedoc labs/lab06-documentation/typescript/geo.ts`.
