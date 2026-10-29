// Tableau de bord d'occupation des salles (reproduit le ticket INC-101).
//   node labs/lab04-debogage/typescript/tableau-de-bord.ts
import { type Reservation, tauxOccupation } from './reservations.ts';

const SALLES = ['A-101', 'A-102', 'B-204'];

const RESERVATIONS: Reservation[] = [
  { salle: 'A-101', debut: new Date('2026-11-02T09:00'), fin: new Date('2026-11-02T12:00'), tarifHoraire: 20 },
  { salle: 'A-101', debut: new Date('2026-11-02T13:00'), fin: new Date('2026-11-02T16:00'), tarifHoraire: 20 },
  { salle: 'A-102', debut: new Date('2026-11-02T10:00'), fin: new Date('2026-11-02T11:00'), tarifHoraire: 15 },
];

console.log('Occupation des salles · lundi 2 novembre');
for (const salle of SALLES) {
  console.log(`  ${salle} : ${Math.round(tauxOccupation(RESERVATIONS, salle) * 100)} %`);
}
