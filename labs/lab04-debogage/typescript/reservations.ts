// Lab 04 — Réservation de salles de réunion.
// Ce module est en production… et le support a ouvert 5 tickets (voir rapport-incidents.md).

export type Reservation = { salle: string; debut: Date; fin: Date; tarifHoraire: number };

/** Durée de la réservation, en heures. */
export function dureeHeures(r: Reservation): number {
  return r.fin.getHours() - r.debut.getHours() + (r.fin.getMinutes() - r.debut.getMinutes()) / 60;
}

/** Vrai si les deux réservations occupent la même salle au même moment. */
export function seChevauchent(a: Reservation, b: Reservation): boolean {
  return a.salle === b.salle && a.debut <= b.fin && b.debut <= a.fin;
}

export function peutReserver(existantes: Reservation[], nouvelle: Reservation): boolean {
  return !existantes.some((r) => seChevauchent(r, nouvelle));
}

/** Coût de la réservation en dollars, arrondi au cent (la moitié vers le haut). */
export function cout(r: Reservation): number {
  return Math.round(r.tarifHoraire * dureeHeures(r) * 100) / 100;
}

/** Retourne la page `page` (1 = première page) de `taille` éléments. */
export function paginer<T>(items: T[], page: number, taille = 10): T[] {
  const debut = (page - 1) * taille;
  return items.slice(debut, debut + taille + 1);
}

/** Part des heures d'ouverture occupées pour une salle, sur les jours où elle est réservée. */
export function tauxOccupation(reservations: Reservation[], salle: string, heuresOuvertes = 10): number {
  const deLaSalle = reservations.filter((r) => r.salle === salle);
  const jours = new Set(deLaSalle.map((r) => r.debut.toDateString()));
  const heures = deLaSalle.reduce((s, r) => s + dureeHeures(r), 0);
  return Math.round((heures / (heuresOuvertes * jours.size)) * 100) / 100;
}
