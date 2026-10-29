// Commandes de la ligne de commande :  npm run taches -- lister
// À construire avec votre assistant en mode agent, en suivant SPEC.md et le README du lab.
// Découpage suggéré : modele.ts (la tâche), depot.ts (lecture / écriture JSON), cli.ts (commandes).

export type Resultat = { code: number; sortie: string };

/** Exécute une commande et retourne le code de sortie et le texte à afficher. */
export function main(argv: string[], fichier: string): Resultat {
  throw new Error('À construire');
}

if (import.meta.main) {
  const { code, sortie } = main(process.argv.slice(2), 'taches.json');
  console.log(sortie);
  process.exitCode = code;
}
