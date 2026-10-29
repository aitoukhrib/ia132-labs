// Mesure le temps des 3 fonctions quand la taille de la liste double.
//   npm run bench:lab05              # tailles 5 000, 10 000, 20 000
//   node labs/lab05-performance/typescript/bench.ts 200000
// Si le temps est multiplié par ~4 quand la taille double, l'algorithme est quadratique, O(n²).
import { communs, dedoublonner, topDomaines } from './analyse.ts';

/** Générateur pseudo-aléatoire déterministe (mêmes listes à chaque exécution). */
function aleatoire(graine: number) {
  let a = graine >>> 0; // mulberry32 : arithmétique 32 bits exacte
  return (max: number) => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), a | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) % max;
  };
}

export function generer(n: number, graine = 42): string[] {
  const rnd = aleatoire(graine);
  return Array.from({ length: n }, () => `  Personne${rnd(Math.floor(n / 2))}@DOMAINE${rnd(200)}.CA `);
}

const chrono = (f: () => unknown) => {
  const t0 = performance.now();
  f();
  return (performance.now() - t0) / 1000;
};

if (import.meta.main) {
  const tailles = process.argv[2] ? [Number(process.argv[2])] : [5_000, 10_000, 20_000];
  console.log('  taille   dedoublonner   topDomaines    communs');
  for (const n of tailles) {
    const a = generer(n, 1);
    const b = generer(n, 2);
    const t = [chrono(() => dedoublonner(a)), chrono(() => topDomaines(a)), chrono(() => communs(a, b))];
    console.log(`${String(n).padStart(8)} ${t.map((x) => `${x.toFixed(3)}s`.padStart(14)).join(' ')}`);
  }
}
