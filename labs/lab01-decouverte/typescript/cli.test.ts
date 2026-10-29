// Étape 4 (mode agent) : ces tests échouent tant que la fonction main() n'existe pas.
import assert from 'node:assert/strict';
import { test } from 'node:test';
import * as conv from './convertisseur.ts';

const main = (conv as unknown as { main?: (argv: string[]) => string }).main;

test('cli : conversion', () => {
  assert.ok(main, 'exportez une fonction main(argv: string[]): string');
  assert.equal(main(['100', 'C', 'F']), '212.00 F');
  assert.equal(main(['42.195', 'km', 'mi']), '26.22 mi');
});

test('cli : erreurs', () => {
  assert.ok(main, 'exportez une fonction main(argv: string[]): string');
  assert.match(main(['abc', 'C', 'F']), /^Erreur/);
  assert.match(main(['100']), /^Usage/);
});
