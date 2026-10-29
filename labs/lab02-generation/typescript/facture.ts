// Lab 02 — Calcul d'une facture avec TPS et TVQ.
// À générer avec votre assistant à partir de SPEC.md (voir README).
// Tous les montants sont des entiers, en cents.

export type Ligne = { produit: string; prix: number; quantite: number };

export type Facture = {
  sousTotal: number;
  rabais: number;
  livraison: number;
  tps: number;
  tvq: number;
  total: number;
};

/** Calcule une facture. Les règles complètes sont dans SPEC.md. */
export function calculerFacture(lignes: Ligne[], codePromo?: string): Facture {
  throw new Error('À compléter');
}
