// Vos tests du panier. Remplacez ces tests par les vôtres (voir README).
//   npm run cov:lab08
//   node labs/lab08-tests/typescript/mutants.ts
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { Panier, type Produit } from './panier.ts';

const CLAVIER: Produit = { sku: 'KB-01', nom: 'Clavier', prix: 4_999, stock: 10 };

test('panier vide', () => {
  assert.equal(new Panier().total(), 0);
});

test('ajouter un article', () => {
  const p = new Panier();
  p.ajouter(CLAVIER);
  assert.equal(p.nombreArticles(), 1);
});
