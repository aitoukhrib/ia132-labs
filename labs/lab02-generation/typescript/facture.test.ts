// Tests d'acceptation : ils décrivent SPEC.md. Ne les modifiez pas, faites-les passer.
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { calculerFacture, type Ligne } from './facture.ts';

const lignes = (...articles: [number, number][]): Ligne[] =>
  articles.map(([prix, quantite], i) => ({ produit: `article ${i}`, prix, quantite }));

const PANIER = lignes([18_999, 1], [1_299, 2]); // écran + 2 câbles = 215,97 $

test('petite commande avec livraison', () => {
  assert.deepEqual(calculerFacture(lignes([4_999, 1])), {
    sousTotal: 4_999, rabais: 0, livraison: 999, tps: 300, tvq: 598, total: 6_896,
  });
});

test('livraison gratuite dès 75 $', () => {
  assert.deepEqual(calculerFacture(PANIER), {
    sousTotal: 21_597, rabais: 0, livraison: 0, tps: 1_080, tvq: 2_154, total: 24_831,
  });
});

test('code BIENVENUE10', () => {
  assert.deepEqual(calculerFacture(PANIER, 'BIENVENUE10'), {
    sousTotal: 21_597, rabais: 2_160, livraison: 0, tps: 972, tvq: 1_939, total: 22_348,
  });
});

test('le rabais peut faire perdre la livraison gratuite', () => {
  const f = calculerFacture(lignes([4_000, 2]), 'BIENVENUE10');
  assert.equal(f.rabais, 800);
  assert.equal(f.livraison, 999);
  assert.equal(f.total, 9_427);
});

test('ETE15 sous le seuil ne donne rien', () => {
  const f = calculerFacture(lignes([4_000, 2]), 'ETE15');
  assert.equal(f.rabais, 0);
  assert.equal(f.total, 9_198);
});

test('ETE15 au-dessus du seuil', () => {
  assert.equal(calculerFacture(PANIER, 'ETE15').rabais, 3_240);
  assert.equal(calculerFacture(PANIER, 'ETE15').total, 21_106);
});

test('code insensible à la casse et aux espaces', () => {
  assert.deepEqual(calculerFacture(PANIER, '  bienvenue10 '), calculerFacture(PANIER, 'BIENVENUE10'));
});

test('arrondi de la moitié vers le haut', () => {
  // base taxable 1 010 ¢ : TPS = 50,5 ¢ → 51 ¢
  const f = calculerFacture(lignes([11, 1]));
  assert.equal(f.tps, 51);
  assert.equal(f.total, 1_162);
});

test('code promo inconnu', () => {
  assert.throws(() => calculerFacture(PANIER, 'GRATUIT100'), { name: 'RangeError', message: /code promo/i });
});

test('entrées invalides', () => {
  assert.throws(() => calculerFacture([]), RangeError);
  assert.throws(() => calculerFacture(lignes([1_000, 0])), RangeError);
  assert.throws(() => calculerFacture(lignes([-1, 1])), RangeError);
});
