// Module hérité : calcule le total, la livraison et la priorité des commandes.
// Écrit en 2017, « ça marche, on n'y touche pas ». Jusqu'à aujourd'hui.

export function traiter(c: any[], r: string, p: boolean): any[] {
  // c = commandes, r = region, p = client premium
  const res: any[] = [];
  for (let i = 0; i < c.length; i++) {
    const x = c[i];
    if (x.statut != 'annulee') {
      if (x.poids > 0) {
        let t = 0;
        for (let j = 0; j < x.lignes.length; j++) {
          t = t + x.lignes[j].prix * x.lignes[j].qte;
        }
        let f;
        if (r == 'QC') {
          if (x.poids <= 2) {
            f = 8;
          } else {
            if (x.poids <= 10) {
              f = 15;
            } else {
              f = 15 + (x.poids - 10) * 1.5;
            }
          }
        } else if (r == 'ON') {
          if (x.poids <= 2) {
            f = 10;
          } else {
            if (x.poids <= 10) {
              f = 18;
            } else {
              f = 18 + (x.poids - 10) * 1.75;
            }
          }
        } else {
          if (x.poids <= 2) {
            f = 14;
          } else {
            if (x.poids <= 10) {
              f = 25;
            } else {
              f = 25 + (x.poids - 10) * 2.5;
            }
          }
        }
        if (p) {
          if (t > 100) {
            f = 0;
          } else {
            f = f / 2;
          }
        }
        let pr;
        if (t > 500) {
          pr = 'haute';
        } else if (t > 100) {
          pr = 'normale';
        } else {
          pr = 'basse';
        }
        res.push({ id: x.id, total: Math.round((t + f) * 100) / 100, livraison: Math.round(f * 100) / 100, priorite: pr });
      } else {
        console.log('poids invalide ' + x.id);
      }
    }
  }
  return res;
}
