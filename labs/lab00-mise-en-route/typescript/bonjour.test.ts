import assert from 'node:assert/strict';
import { test } from 'node:test';
import { saluer } from './bonjour.ts';

test('saluer avec un nom', () => {
  assert.equal(saluer('Ada'), 'Bonjour Ada, bienvenue à la formation IA132 !');
});

test('saluer sans nom', () => {
  assert.equal(saluer('   '), 'Bonjour inconnu, bienvenue à la formation IA132 !');
});
