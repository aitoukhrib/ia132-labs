# Lab 10 · Concevoir et planifier avec l’IA

| Module | Durée | Langages |
| --- | --- | --- |
| 6 · IA pour la planification et l’architecture logicielle | 35 min | Markdown, Mermaid, CSV (vérification en Python ou TypeScript) |

## Objectif

Utiliser l’IA comme **partenaire d’architecture** : faire émerger les questions, comparer des options, documenter une décision (ADR), découper et estimer un backlog réaliste, puis auditer des dépendances… en **vérifiant** chaque affirmation.

## Point de départ

- `cahier-des-charges.md` : Cantine+, précommande de repas pour 3 cafétérias (projet fictif).
- `gabarits/` : modèle d’ADR et en-tête du backlog CSV.
- `dependances/` : les fichiers de dépendances d’un vieux prototype que l’équipe veut réutiliser.
- `python/test_livrables.py` / `typescript/livrables.test.ts` : vérifient que vos livrables sont **complets et cohérents** (pas leur qualité).

Créez vos fichiers dans `labs/lab10-architecture/livrables/`.

```bash
pytest labs/lab10-architecture          # ou : npm run test:lab10
```

## Étapes

1. **Questions d’abord (5 min)** — Joignez le cahier des charges et demandez :
   > Avant de proposer une architecture, pose-moi les 8 questions les plus importantes sur ce projet, classées par impact sur l’architecture.

   Répondez à 3 d’entre elles (vous jouez le PO).
2. **Architecture (10 min)** — Demandez **2 options contrastées** (ex. monolithe modulaire vs microservices) avec leurs compromis face aux contraintes (pic de 10 h 30, paie SAP, allergènes, équipe de 4). Choisissez. Faites produire `livrables/architecture.md` avec un diagramme **Mermaid** et un tableau des composants.
3. **ADR (5 min)** — `livrables/adr-001.md` à partir du gabarit : votre décision, ses alternatives, ses conséquences.
4. **Backlog et planification (12 min)** — Faites découper le projet en **12 user stories ou plus** (`livrables/backlog.csv`) : critère d’acceptation Gherkin, points (suite de Fibonacci), priorité MoSCoW, sprint, dépendances. Lancez les tests : l’IA respecte-t-elle la **vélocité de 20 points**, l’ordre des dépendances, le pilote en 3 sprints ? Corrigez.
5. **Risques et dépendances (8 min)** — `livrables/risques.md` (≥ 5 risques : probabilité, impact, mesure). Puis faites analyser `dependances/` par l’IA et **vérifiez** avec un outil :
   ```bash
   pip install pip-audit
   pip-audit --disable-pip --no-deps -r labs/lab10-architecture/dependances/requirements-legacy.txt
   cd labs/lab10-architecture/dependances
   npm install --package-lock-only && npm audit
   ```
   Consignez le résultat dans `livrables/dependances.md`, en signalant chaque identifiant CVE inventé par l’IA.

## Livrable

Les 5 fichiers de `livrables/`, tous les tests du lab au vert, et une phrase dans `NOTES.md` : « l’IA a été utile pour… / je l’ai corrigée sur… ».

## Pièges à observer

- L’IA propose des microservices, Kubernetes et Kafka pour 4 développeurs et un pilote en 6 semaines.
- Les estimations « au doigt mouillé » : demandez-lui de justifier chaque 8 par un critère (inconnue, intégration, risque).
- Sprints surchargés et dépendances inversées : c’est exactement ce que les tests détectent.
- Des numéros de CVE plausibles… mais inexistants. Seul un outil d’audit fait foi.

## Bonus

Demandez à l’IA de jouer l’**avocat du diable** sur votre ADR : quel scénario ferait regretter cette décision dans 2 ans ?
