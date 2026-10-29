// Vérifie les livrables du lab 10 (labs/lab10-architecture/livrables/). Même contrôle que la version Python.
//   npm run test:lab10
import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { test } from 'node:test';

const FIBONACCI = new Set([1, 2, 3, 5, 8, 13]);
const VELOCITE = 20;

const lire = (nom: string) => {
  const url = new URL(`../livrables/${nom}`, import.meta.url);
  assert.ok(existsSync(url), `livrable manquant : livrables/${nom}`);
  return readFileSync(url, 'utf8');
};

type Story = Record<string, string>;

/** Lecture CSV minimale (champs entre guillemets acceptés). */
function backlog(): Story[] {
  const lignes = lire('backlog.csv').trim().split(/\r?\n/);
  const champs = (l: string) => {
    const out: string[] = [];
    let cur = '';
    let guillemets = false;
    for (let i = 0; i < l.length; i++) {
      const c = l[i];
      if (guillemets && c === '"' && l[i + 1] === '"') (cur += '"'), i++;
      else if (c === '"') guillemets = !guillemets;
      else if (c === ',' && !guillemets) out.push(cur), (cur = '');
      else cur += c;
    }
    return [...out, cur];
  };
  const entete = champs(lignes[0]);
  return lignes.slice(1).map((l) => Object.fromEntries(champs(l).map((v, i) => [entete[i], v.trim()])));
}

test('architecture avec diagramme Mermaid et intégrations critiques', () => {
  const t = lire('architecture.md');
  assert.match(t, /```mermaid\s+(flowchart|graph|C4Container|C4Context)/);
  for (const mot of ['paie', 'entra', 'allerg', 'notification']) assert.ok(t.toLowerCase().includes(mot), `à traiter : ${mot}`);
});

test('ADR complète', () => {
  const t = lire('adr-001.md');
  for (const s of ['## Contexte', '## Décision', '## Alternatives', '## Conséquences']) assert.ok(t.includes(s), `section manquante : ${s}`);
});

test('backlog : au moins 12 stories bien formées, points de Fibonacci', () => {
  const b = backlog();
  assert.ok(b.length >= 12, 'au moins 12 user stories');
  for (const us of b) {
    assert.match(us.story, /^en tant qu/i, `${us.id} : « En tant que … »`);
    assert.match(us.critere_acceptation, /étant donné.*quand.*alors/i, `${us.id} : critère Gherkin attendu`);
    assert.ok(FIBONACCI.has(Number(us.points)), `${us.id} : ${us.points} hors Fibonacci`);
    if (us.sprint) assert.ok(Number(us.points) < 13, `${us.id} : 13 points dans un sprint`);
  }
});

test('capacité des sprints, dépendances et pilote en 3 sprints', () => {
  const b = backlog();
  const charge = new Map<number, number>();
  const sprint = new Map(b.map((us) => [us.id, us.sprint ? Number(us.sprint) : null]));
  for (const us of b) {
    if (us.sprint) charge.set(Number(us.sprint), (charge.get(Number(us.sprint)) ?? 0) + Number(us.points));
    for (const dep of us.depend_de.split(/[ ;|]+/).filter(Boolean)) {
      assert.ok(sprint.has(dep), `${us.id} dépend de ${dep}, qui n'existe pas`);
      const s = sprint.get(us.id);
      const d = sprint.get(dep);
      if (s != null) assert.ok(d != null && d <= s, `${us.id} (sprint ${s}) dépend de ${dep} (sprint ${d})`);
    }
    if (us.priorite.toUpperCase() === 'MUST') assert.ok(us.sprint && Number(us.sprint) <= 3, `${us.id} MUST hors des 3 premiers sprints`);
  }
  for (const [s, p] of charge) assert.ok(p <= VELOCITE, `sprint ${s} : ${p} points > ${VELOCITE}`);
});

test('registre des risques et analyse des dépendances', () => {
  const lignes = lire('risques.md').split('\n').filter((l) => l.startsWith('|') && !/^\|\s*-/.test(l));
  assert.ok(lignes.length - 1 >= 5, 'au moins 5 risques');
  for (const c of ['probabilit', 'impact', 'mesure']) assert.ok(lignes[0].toLowerCase().includes(c), `colonne ${c}`);
  const d = lire('dependances.md').toLowerCase();
  for (const p of ['django', 'requests', 'pyyaml', 'lodash', 'jsonwebtoken', 'moment']) assert.ok(d.includes(p), `à traiter : ${p}`);
  assert.match(d, /pip-audit|npm audit|osv|github advisory/, "citez l'outil qui a VÉRIFIÉ l'analyse");
});
