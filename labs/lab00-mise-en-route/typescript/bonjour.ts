// Lab 00 — Vérifie que l'environnement Node.js / TypeScript fonctionne.

export function saluer(nom: string): string {
  const propre = nom.trim() || 'inconnu';
  return `Bonjour ${propre}, bienvenue à la formation IA132 !`;
}
