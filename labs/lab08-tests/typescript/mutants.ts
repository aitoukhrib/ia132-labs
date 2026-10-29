// Test de mutation simplifié : vos tests détectent-ils ces 8 bogues ?
//   node labs/lab08-tests/typescript/mutants.ts
// Chaque mutant modifie une ligne de panier.ts dans une copie temporaire, puis relance vos tests.
// Mutant « tué » (vos tests échouent) : bien. Mutant « survivant » : comportement non vérifié.
import { spawnSync } from 'node:child_process';
import { copyFileSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const ici = new URL('.', import.meta.url);
const source = readFileSync(new URL('panier.ts', ici), 'utf8');

const MUTANTS: [string, string, string][] = [
  ['quantité 0 acceptée', 'if (quantite < 1)', 'if (quantite < 0)'],
  ['maximum 99 décalé', 'if (nouvelle > QUANTITE_MAX)', 'if (nouvelle >= QUANTITE_MAX)'],
  ['stock non vérifié', 'if (nouvelle > produit.stock)', 'if (nouvelle > produit.stock + 1)'],
  ['retrait partiel faux', 'quantite >= actuelle', 'quantite > actuelle'],
  ['code sensible à la casse', ".includes(code.toUpperCase())", '.includes(code)'],
  ['rabais de 1 %', 'Math.floor(this.sousTotal() / 10)', 'Math.floor(this.sousTotal() / 100)'],
  ['seuil de livraison strict', '>= SEUIL_LIVRAISON_GRATUITE', '> SEUIL_LIVRAISON_GRATUITE'],
  ['livraison facturée au panier vide', 'if (this.lignes.size === 0) return 0;', ''],
];

let survivants = 0;
for (const [nom, avant, apres] of MUTANTS) {
  if (!source.includes(avant)) throw new Error(`mutant « ${nom} » : ligne introuvable dans panier.ts`);
  const tmp = mkdtempSync(join(tmpdir(), 'mutant-'));
  try {
    copyFileSync(new URL('panier.test.ts', ici), join(tmp, 'panier.test.ts'));
    writeFileSync(join(tmp, 'panier.ts'), source.replace(avant, apres));
    const r = spawnSync(process.execPath, ['--test', join(tmp, 'panier.test.ts')], { encoding: 'utf8' });
    const tue = r.status !== 0;
    if (!tue) survivants++;
    console.log(`  ${tue ? 'tué      ' : 'SURVIVANT'}  ${nom}`);
  } finally {
    rmSync(tmp, { recursive: true, force: true });
  }
}
console.log(`\nScore de mutation : ${MUTANTS.length - survivants}/${MUTANTS.length}`);
process.exitCode = survivants ? 1 : 0;
