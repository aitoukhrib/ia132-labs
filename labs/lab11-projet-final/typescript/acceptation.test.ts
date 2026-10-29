// Tests d'acceptation de SPEC.md (rouges au départ). Ne les modifiez pas.
// Ajoutez VOS tests unitaires dans des fichiers séparés (taches/modele.test.ts…).
import assert from 'node:assert/strict';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { beforeEach, test } from 'node:test';
import { main } from './taches/cli.ts';

let fichier = '';
beforeEach(() => {
  fichier = join(mkdtempSync(join(tmpdir(), 'taches-')), 'taches.json');
});

const run = (...argv: string[]) => main(argv, fichier);
const ids = (sortie: string) =>
  sortie
    .split('\n')
    .map((l) => l.match(/^\[( |x)\] +(\d+) /))
    .filter((m) => m !== null)
    .map((m) => Number(m[2]));

/** Lecture CSV minimale (guillemets acceptés), pour vérifier l'export. */
const csv = (texte: string) =>
  texte.split('\n').map((l) => {
    const out: string[] = [];
    let cur = '';
    let q = false;
    for (let i = 0; i < l.length; i++) {
      if (q && l[i] === '"' && l[i + 1] === '"') (cur += '"'), i++;
      else if (l[i] === '"') q = !q;
      else if (l[i] === ',' && !q) out.push(cur), (cur = '');
      else cur += l[i];
    }
    return [...out, cur];
  });

test('ajouter puis lister', () => {
  assert.deepEqual(run('ajouter', 'Préparer la démo', '--priorite', 'haute'), { code: 0, sortie: 'Tâche 1 ajoutée : Préparer la démo' });
  const { code, sortie } = run('lister');
  assert.equal(code, 0);
  assert.deepEqual(ids(sortie), [1]);
  assert.ok(sortie.includes('Préparer la démo') && sortie.includes('haute'));
});

test('liste vide', () => assert.deepEqual(run('lister'), { code: 0, sortie: 'Aucune tâche.' }));

test('ordre : priorité, puis échéance, puis identifiant', () => {
  run('ajouter', 'basse', '--priorite', 'basse');
  run('ajouter', 'normale sans échéance');
  run('ajouter', 'normale tard', '--echeance', '2026-12-20');
  run('ajouter', 'haute', '--priorite', 'haute');
  run('ajouter', 'normale tôt', '--echeance', '2026-11-10');
  assert.deepEqual(ids(run('lister').sortie), [4, 5, 3, 2, 1]);
});

test('terminer masque la tâche, sauf avec --toutes', () => {
  run('ajouter', 'A');
  run('ajouter', 'B');
  assert.deepEqual(run('terminer', '1'), { code: 0, sortie: 'Tâche 1 terminée' });
  assert.deepEqual(ids(run('lister').sortie), [2]);
  const s = run('lister', '--toutes').sortie;
  assert.deepEqual(ids(s), [1, 2]);
  assert.ok(s.startsWith('[x]'));
});

test('les identifiants ne sont jamais réutilisés', () => {
  run('ajouter', 'A');
  run('ajouter', 'B');
  assert.deepEqual(run('supprimer', '2'), { code: 0, sortie: 'Tâche 2 supprimée' });
  assert.equal(run('ajouter', 'C').sortie, 'Tâche 3 ajoutée : C');
});

test('filtres étiquette et priorité', () => {
  run('ajouter', 'A', '--etiquette', 'ia', '--etiquette', 'formation');
  run('ajouter', 'B', '--etiquette', 'perso', '--priorite', 'haute');
  run('ajouter', 'C', '--etiquette', 'ia', '--priorite', 'haute');
  assert.deepEqual(ids(run('lister', '--etiquette', 'ia').sortie), [3, 1]);
  assert.deepEqual(ids(run('lister', '--priorite', 'haute').sortie), [2, 3]);
  assert.ok(run('lister').sortie.includes('#ia #formation'));
});

test('en retard : strictement avant la date', () => {
  run('ajouter', 'hier', '--echeance', '2026-11-01');
  run('ajouter', "aujourd'hui", '--echeance', '2026-11-02');
  run('ajouter', 'sans date');
  run('ajouter', 'hier mais faite', '--echeance', '2026-10-01');
  run('terminer', '4');
  assert.deepEqual(ids(run('en-retard', '--aujourdhui', '2026-11-02').sortie), [1]);
});

test('export JSON', () => {
  run('ajouter', 'A', '--etiquette', 'ia', '--echeance', '2026-11-05');
  run('ajouter', 'B');
  const d = JSON.parse(run('exporter', '--format', 'json').sortie);
  assert.deepEqual(d[0], { id: 1, titre: 'A', priorite: 'normale', echeance: '2026-11-05', etiquettes: ['ia'], terminee: false });
  assert.equal(d[1].echeance, null);
});

test('export CSV', () => {
  run('ajouter', 'Titre, avec virgule', '--etiquette', 'a', '--etiquette', 'b');
  run('terminer', '1');
  const lignes = csv(run('exporter', '--format', 'csv').sortie);
  assert.deepEqual(lignes[0], ['id', 'titre', 'priorite', 'echeance', 'etiquettes', 'terminee']);
  assert.deepEqual(lignes[1], ['1', 'Titre, avec virgule', 'normale', '', 'a;b', 'oui']);
});

test('arguments invalides → code 2', () => {
  for (const argv of [['ajouter', 'X', '--priorite', 'urgente'], ['ajouter', 'X', '--echeance', '2026-13-45'], ['ajouter', '   '], ['voler']]) {
    const r = run(...argv);
    assert.equal(r.code, 2, argv.join(' '));
    assert.match(r.sortie, /^Erreur/);
  }
});

test('tâche introuvable → code 1', () => {
  for (const c of ['terminer', 'supprimer']) assert.deepEqual(run(c, '42'), { code: 1, sortie: 'Erreur : tâche 42 introuvable' });
});
