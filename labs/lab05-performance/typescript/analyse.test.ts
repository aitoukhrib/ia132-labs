// Le comportement à préserver pendant l'optimisation : verts au départ.
// Les budgets de temps (fin de fichier) sont rouges au départ.
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { communs, dedoublonner, topDomaines } from './analyse.ts';
import { generer } from './bench.ts';

const LISTE = [' Ana@Exemple.ca', 'bob@test.com', 'ana@exemple.ca', 'Zoe@exemple.ca', 'BOB@test.com ', 'eve@autre.org'];

test('dedoublonner normalise', () => {
  assert.deepEqual(dedoublonner(['  Ana@X.ca ', 'ana@x.ca']), ['ana@x.ca']);
});

test("dedoublonner garde l'ordre de première apparition", () => {
  assert.deepEqual(dedoublonner(LISTE), ['ana@exemple.ca', 'bob@test.com', 'zoe@exemple.ca', 'eve@autre.org']);
});

test('topDomaines compte les occurrences', () => {
  assert.deepEqual(topDomaines(LISTE, 2), [['exemple.ca', 3], ['test.com', 2]]);
});

test('topDomaines : égalité par ordre alphabétique', () => {
  assert.deepEqual(topDomaines(['a@b.ca', 'c@a.ca'], 2), [['a.ca', 1], ['b.ca', 1]]);
});

test("communs dans l'ordre de la première liste", () => {
  const a = ['zoe@exemple.ca', 'BOB@test.com', 'nouveau@x.ca', 'bob@test.com'];
  assert.deepEqual(communs(a, LISTE), ['zoe@exemple.ca', 'bob@test.com']);
});

// ── Budgets de temps ───────────────────────────────────────────────────────
const N = 10_000;
const BUDGET_MS = 150;
const duree = (f: () => unknown) => {
  const t0 = performance.now();
  f();
  return performance.now() - t0;
};

test(`dedoublonner : ${N} courriels en moins de ${BUDGET_MS} ms`, () => {
  const a = generer(N, 1);
  assert.ok(duree(() => dedoublonner(a)) < BUDGET_MS);
});

test(`communs : ${N} courriels en moins de ${BUDGET_MS} ms`, () => {
  const a = generer(N, 1);
  const b = generer(N, 2);
  assert.ok(duree(() => communs(a, b)) < BUDGET_MS);
});
