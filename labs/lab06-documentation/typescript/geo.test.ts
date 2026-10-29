// 1. Comportement : verts au départ, ils doivent le rester.
// 2. Documentation : rouges au départ. Chaque fonction exportée doit être précédée d'un
//    bloc TSDoc (/** … */) avec @param pour chaque paramètre, @returns, @throws si elle
//    lève une exception, et un @example.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import { dansLeRayon, distanceKm, formatCoordonnees, type Point, plusProche } from './geo.ts';

const MTL: Point = { nom: 'Montréal', lat: 45.5019, lon: -73.5674 };
const QC: Point = { nom: 'Québec', lat: 46.8139, lon: -71.208 };
const OTT: Point = { nom: 'Ottawa', lat: 45.4215, lon: -75.6972 };
const TR: Point = { nom: 'Trois-Rivières', lat: 46.343, lon: -72.5477 };
const SH: Point = { nom: 'Sherbrooke', lat: 45.4042, lon: -71.8929 };

// ── 1. Comportement ────────────────────────────────────────────────────────
test('distances', () => {
  assert.equal(distanceKm(MTL, QC), 233);
  assert.equal(distanceKm(MTL, OTT), 166.3);
});

test('dansLeRayon trie par distance', () => {
  assert.deepEqual(dansLeRayon(MTL, [QC, OTT, TR, SH], 150).map((p) => p.nom), ['Trois-Rivières', 'Sherbrooke']);
});

test("plusProche ignore l'origine", () => {
  assert.equal(plusProche(MTL, [MTL, QC, OTT, TR, SH]), TR);
  assert.equal(plusProche(MTL, [MTL]), undefined);
});

test('format', () => assert.equal(formatCoordonnees(MTL), '45.5019° N, 73.5674° O'));

// ── 2. Documentation ───────────────────────────────────────────────────────
const source = readFileSync(new URL('./geo.ts', import.meta.url), 'utf8');

const docDe = (nom: string): string => {
  const m = source.match(new RegExp(`/\\*\\*((?:(?!\\*/)[\\s\\S])*)\\*/\\s*export function ${nom}\\(([^)]*)\\)`));
  assert.ok(m, `${nom} : bloc /** … */ attendu juste avant « export function ${nom} »`);
  return m[1] + '\n@@params ' + m[2];
};

for (const nom of ['distanceKm', 'dansLeRayon', 'plusProche', 'formatCoordonnees']) {
  test(`TSDoc complet : ${nom}`, () => {
    const doc = docDe(nom);
    const params = doc.split('@@params ')[1].split(',').map((p) => p.split(':')[0].trim()).filter(Boolean);
    for (const p of params) assert.match(doc, new RegExp(`@param ${p}\\b`), `@param ${p} manquant`);
    assert.match(doc, /@returns/, '@returns manquant');
    assert.match(doc, /@example/, '@example manquant');
    const corps = source.split(`export function ${nom}(`)[1].split('\nexport ')[0];
    if (corps.includes('throw ')) assert.match(doc, /@throws/, 'la fonction lève une exception : @throws attendu');
  });
}

test('le type Point est documenté', () => {
  assert.match(source, /\/\*\*[\s\S]*?\*\/\s*export type Point/, 'bloc /** … */ attendu avant « export type Point »');
});
