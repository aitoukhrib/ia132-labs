// Lab 08 — Panier d'achat. Ce module n'a AUCUN test : à vous de les générer.
// Les prix sont des entiers en cents.

export const QUANTITE_MAX = 99;
export const SEUIL_LIVRAISON_GRATUITE = 5_000;
export const FRAIS_LIVRAISON = 799;

export class StockInsuffisant extends Error {}

export type Produit = { sku: string; nom: string; prix: number; stock: number };

export class Panier {
  lignes = new Map<string, number>();
  catalogue = new Map<string, Produit>();
  codePromo: string | null = null;

  ajouter(produit: Produit, quantite = 1): void {
    if (quantite < 1) throw new RangeError('quantité invalide');
    const nouvelle = (this.lignes.get(produit.sku) ?? 0) + quantite;
    if (nouvelle > QUANTITE_MAX) throw new RangeError(`maximum ${QUANTITE_MAX} par article`);
    if (nouvelle > produit.stock) throw new StockInsuffisant(`${produit.nom} : ${produit.stock} en stock`);
    this.catalogue.set(produit.sku, produit);
    this.lignes.set(produit.sku, nouvelle);
  }

  retirer(sku: string, quantite?: number): void {
    const actuelle = this.lignes.get(sku);
    if (actuelle === undefined) throw new RangeError(`article absent : ${sku}`);
    if (quantite === undefined || quantite >= actuelle) this.lignes.delete(sku);
    else this.lignes.set(sku, actuelle - quantite);
  }

  appliquerCode(code: string): void {
    if (!['MOINS10', 'LIVRAISON'].includes(code.toUpperCase())) throw new RangeError('code inconnu');
    this.codePromo = code.toUpperCase();
  }

  sousTotal(): number {
    let s = 0;
    for (const [sku, q] of this.lignes) s += this.catalogue.get(sku)!.prix * q;
    return s;
  }

  rabais(): number {
    if (this.codePromo === 'MOINS10') return Math.floor(this.sousTotal() / 10);
    return 0;
  }

  livraison(): number {
    if (this.lignes.size === 0) return 0;
    if (this.codePromo === 'LIVRAISON') return 0;
    if (this.sousTotal() - this.rabais() >= SEUIL_LIVRAISON_GRATUITE) return 0;
    return FRAIS_LIVRAISON;
  }

  total(): number {
    return this.sousTotal() - this.rabais() + this.livraison();
  }

  nombreArticles(): number {
    let n = 0;
    for (const q of this.lignes.values()) n += q;
    return n;
  }
}
