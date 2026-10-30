// Lab 09 — Mini-API de liens courts (modules natifs de Node uniquement).
//   npm run api:lab09          # http://localhost:8009
//
//   POST /liens        {"url": "https://…"}   → 201 {code, url}
//   GET  /l/<code>                            → 302 vers l'URL
//   GET  /stats/<code>                        → 200 {code, url, clics}
//   GET  /sante                               → 200 {statut: "ok"}
import { randomInt } from 'node:crypto';
import { createServer, type IncomingMessage, type Server, type ServerResponse } from 'node:http';

const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
export const LONGUEUR_CODE = 5;
const TAILLE_MAX_URL = 2_048;

export function urlValide(url: unknown): url is string {
  if (typeof url !== 'string' || url.length > TAILLE_MAX_URL) return false;
  try {
    const u = new URL(url);
    return (u.protocol === 'http:' || u.protocol === 'https:') && u.host !== '';
  } catch {
    return false;
  }
}

export const nouveauCode = () => Array.from({ length: LONGUEUR_CODE }, () => ALPHABET[randomInt(ALPHABET.length)]).join('');

export class Depot {
  private liens = new Map<string, { url: string; clics: number }>();

  creer(url: string): string {
    let code = nouveauCode();
    while (this.liens.has(code)) code = nouveauCode();
    this.liens.set(code, { url, clics: 0 });
    return code;
  }

  visiter(code: string): string | null {
    const lien = this.liens.get(code);
    if (!lien) return null;
    lien.clics++;
    return lien.url;
  }

  stats(code: string) {
    const lien = this.liens.get(code);
    return lien ? { code, ...lien } : null;
  }
}

function json(res: ServerResponse, statut: number, corps: unknown): void {
  const donnees = JSON.stringify(corps);
  res.writeHead(statut, { 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': Buffer.byteLength(donnees) });
  res.end(donnees);
}

async function lireCorps(req: IncomingMessage): Promise<string> {
  let s = '';
  for await (const morceau of req) s += morceau;
  return s;
}

export function creerServeur(depot = new Depot()): Server {
  return createServer(async (req, res) => {
    const chemin = req.url ?? '/';
    if (req.method === 'GET') {
      if (chemin === '/sante') return json(res, 200, { statut: 'ok' });
      if (chemin.startsWith('/l/')) {
        const url = depot.visiter(chemin.slice(3));
        if (!url) return json(res, 404, { erreur: 'lien inconnu' });
        res.writeHead(302, { Location: url, 'Content-Length': 0 });
        return res.end();
      }
      if (chemin.startsWith('/stats/')) {
        const s = depot.stats(chemin.slice(7));
        return s ? json(res, 200, s) : json(res, 404, { erreur: 'lien inconnu' });
      }
    }
    if (req.method === 'POST' && chemin === '/liens') {
      let corps: unknown;
      try {
        corps = JSON.parse((await lireCorps(req)) || '{}');
      } catch {
        return json(res, 400, { erreur: 'JSON invalide' });
      }
      const url = corps && typeof corps === 'object' && !Array.isArray(corps) ? (corps as { url?: unknown }).url : undefined;
      if (!urlValide(url)) return json(res, 400, { erreur: 'url invalide : http(s)://… attendu' });
      return json(res, 201, { code: depot.creer(url), url });
    }
    return json(res, 404, { erreur: 'route inconnue' });
  });
}

if (import.meta.main) {
  creerServeur().listen(8009, () => console.log('API de liens courts sur http://localhost:8009 (Ctrl+C pour arrêter)'));
}
