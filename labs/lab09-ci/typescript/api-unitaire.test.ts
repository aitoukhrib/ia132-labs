// Tests unitaires existants (verts). Les tests d'intégration sont à écrire : integration.test.ts.
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { Depot, LONGUEUR_CODE, nouveauCode, urlValide } from './api.ts';

test('URL valides', () => {
  for (const u of ['https://technologia.com', 'http://exemple.ca/a?b=1']) assert.ok(urlValide(u), u);
});

test('URL invalides', () => {
  for (const u of ['ftp://x.ca', 'javascript:alert(1)', 'https://', '', null, 42, `https://a.ca/${'x'.repeat(3000)}`]) {
    assert.ok(!urlValide(u), String(u));
  }
});

test('code de 6 caractères alphanumériques', () => {
  assert.match(nouveauCode(), new RegExp(`^[A-Za-z0-9]{${LONGUEUR_CODE}}$`));
});

test('le dépôt compte les visites', () => {
  const d = new Depot();
  const code = d.creer('https://exemple.ca');
  d.visiter(code);
  d.visiter(code);
  assert.equal(d.stats(code)?.clics, 2);
  assert.equal(d.visiter('inconnu'), null);
});
