// Lab 05 — Analyse d'une liste de diffusion.
// Correct, testé… et beaucoup trop lent sur les 200 000 abonnés de la vraie liste.

export const normaliser = (courriel: string) => courriel.trim().toLowerCase();

/** Courriels uniques, normalisés, dans l'ordre de leur PREMIÈRE apparition. */
export function dedoublonner(courriels: string[]): string[] {
  const resultat: string[] = [];
  for (const brut of courriels) {
    const c = normaliser(brut);
    if (!resultat.includes(c)) resultat.push(c);
  }
  return resultat;
}

/** Les n domaines les plus fréquents : [domaine, nombre], par nombre décroissant puis par nom. */
export function topDomaines(courriels: string[], n = 3): [string, number][] {
  const domaines = courriels.map((c) => normaliser(c).split('@')[1]);
  const comptes: [string, number][] = [];
  for (const d of dedoublonner(domaines)) {
    comptes.push([d, domaines.filter((x) => x === d).length]);
  }
  comptes.sort((x, y) => y[1] - x[1] || x[0].localeCompare(y[0]));
  return comptes.slice(0, n);
}

/** Courriels présents dans les deux listes, sans doublon, dans l'ordre de listeA. */
export function communs(listeA: string[], listeB: string[]): string[] {
  const b = listeB.map(normaliser);
  return dedoublonner(listeA).filter((c) => b.includes(c));
}
