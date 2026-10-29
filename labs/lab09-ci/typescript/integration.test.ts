// Tests d'intégration : un VRAI serveur HTTP, de vraies requêtes. À compléter (voir README).
import assert from 'node:assert/strict';
import type { AddressInfo } from 'node:net';
import { after, before, test } from 'node:test';
import { creerServeur } from './api.ts';

const serveur = creerServeur();
let base = '';

before(async () => {
  await new Promise<void>((ok) => serveur.listen(0, '127.0.0.1', ok));
  base = `http://127.0.0.1:${(serveur.address() as AddressInfo).port}`;
});
after(() => serveur.close());

// redirect: 'manual' pour lire la réponse 302 elle-même.
const appel = (chemin: string, init: RequestInit = {}) => fetch(base + chemin, { redirect: 'manual', ...init });

test('santé', async () => {
  const r = await appel('/sante');
  assert.equal(r.status, 200);
  assert.deepEqual(await r.json(), { statut: 'ok' });
});

// À vous : demandez à l'IA les scénarios d'intégration, puis écrivez-les ici.
// Pistes : créer puis suivre un lien (201 → 302 + Location), statistiques après 3 visites,
// URL invalide (400), JSON invalide (400), code inconnu (404), créations concurrentes.
