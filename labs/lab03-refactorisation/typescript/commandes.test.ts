// Tests de caractérisation (« golden master ») : ils figent le comportement ACTUEL.
// Verts au départ, ils doivent le rester après CHAQUE étape de refactorisation.
// donnees/attendu.json a été produit en exécutant le code hérité.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import { traiter } from './commandes.ts';

const lire = (nom: string) => JSON.parse(readFileSync(new URL(`../donnees/${nom}`, import.meta.url), 'utf8'));
const COMMANDES = lire('commandes.json');
const ATTENDU: Record<string, unknown[]> = lire('attendu.json');

const silencieux = <T>(f: () => T): T => {
  const log = console.log;
  console.log = () => {};
  try {
    return f();
  } finally {
    console.log = log;
  }
};

for (const cas of Object.keys(ATTENDU).sort()) {
  test(`golden master ${cas}`, () => {
    const [region, formule] = cas.split('-');
    assert.deepEqual(silencieux(() => traiter(COMMANDES, region, formule === 'premium')), ATTENDU[cas]);
  });
}

test('commande simple au Québec', () => {
  const commande = { id: 'X', statut: 'payee', poids: 1, lignes: [{ prix: 20, qte: 2 }] };
  assert.deepEqual(traiter([commande], 'QC', false), [{ id: 'X', total: 48, livraison: 8, priorite: 'basse' }]);
});

test('premium : livraison offerte au-delà de 100 $', () => {
  const commande = { id: 'X', statut: 'payee', poids: 5, lignes: [{ prix: 150, qte: 1 }] };
  assert.equal(traiter([commande], 'ON', true)[0].livraison, 0);
});

test('commandes annulées et poids invalides ignorés', () => {
  const commandes = [
    { id: 'A', statut: 'annulee', poids: 1, lignes: [] },
    { id: 'B', statut: 'payee', poids: 0, lignes: [] },
  ];
  assert.deepEqual(silencieux(() => traiter(commandes, 'QC', false)), []);
});
