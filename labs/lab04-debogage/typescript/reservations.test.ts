// Les 4 premiers tests passent. Les 5 suivants reproduisent les tickets INC-101 à INC-105.
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { cout, dureeHeures, paginer, peutReserver, type Reservation, tauxOccupation } from './reservations.ts';

const resa = (salle: string, debut: string, fin: string, tarifHoraire = 20): Reservation => ({
  salle,
  debut: new Date(debut),
  fin: new Date(fin),
  tarifHoraire,
});

const A = resa('A-101', '2026-11-02T09:00', '2026-11-02T10:00');
const B = resa('A-101', '2026-11-02T13:00', '2026-11-02T16:00');
const C = resa('B-204', '2026-11-02T09:00', '2026-11-02T11:30');
const range = (a: number, b: number) => Array.from({ length: b - a }, (_, i) => a + i);

// ── Ce qui fonctionne ──────────────────────────────────────────────────────
test('durée simple', () => assert.equal(dureeHeures(C), 2.5));
test('conflit détecté', () => assert.equal(peutReserver([A], resa('A-101', '2026-11-02T09:30', '2026-11-02T10:30')), false));
test('coût simple', () => assert.equal(cout(C), 50));
test("taux d'occupation simple", () => assert.equal(tauxOccupation([A, B, C], 'A-101'), 0.4));

// ── Les tickets du support ─────────────────────────────────────────────────
test('INC-101 salle sans réservation', () => assert.equal(tauxOccupation([A, B], 'B-204'), 0));

test('INC-102 pas de doublon entre deux pages', () => {
  assert.deepEqual(paginer(range(0, 25), 1), range(0, 10));
  assert.deepEqual(paginer(range(0, 25), 2), range(10, 20));
  assert.deepEqual(paginer(range(0, 25), 3), range(20, 25));
});

test('INC-103 réservations bout à bout autorisées', () => {
  assert.equal(peutReserver([A], resa('A-101', '2026-11-02T10:00', '2026-11-02T11:00')), true);
});

test('INC-104 arrondi au cent supérieur', () => {
  assert.equal(cout(resa('A-101', '2026-11-02T09:00', '2026-11-02T10:30', 31.15)), 46.73);
});

test('INC-105 réservation sur deux jours', () => {
  assert.equal(dureeHeures(resa('C-310', '2026-11-06T09:00', '2026-11-07T11:00')), 26);
});
