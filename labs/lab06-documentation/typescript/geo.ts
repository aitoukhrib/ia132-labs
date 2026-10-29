export const RAYON_TERRE_KM = 6371;

export type Point = { nom: string; lat: number; lon: number };

const rad = (deg: number) => (deg * Math.PI) / 180;

export function distanceKm(a: Point, b: Point): number {
  const dlat = rad(b.lat - a.lat);
  const dlon = rad(b.lon - a.lon);
  const h = Math.sin(dlat / 2) ** 2 + Math.cos(rad(a.lat)) * Math.cos(rad(b.lat)) * Math.sin(dlon / 2) ** 2;
  return Math.round(2 * RAYON_TERRE_KM * Math.asin(Math.sqrt(h)) * 10) / 10;
}

export function dansLeRayon(centre: Point, points: Point[], rayonKm: number): Point[] {
  if (rayonKm < 0) throw new RangeError('rayon négatif');
  return points.filter((p) => distanceKm(centre, p) <= rayonKm).sort((p, q) => distanceKm(centre, p) - distanceKm(centre, q));
}

export function plusProche(origine: Point, points: Point[]): Point | undefined {
  let meilleur: Point | undefined;
  for (const p of points) {
    if (p === origine) continue;
    if (!meilleur || distanceKm(origine, p) < distanceKm(origine, meilleur)) meilleur = p;
  }
  return meilleur;
}

export function formatCoordonnees(p: Point): string {
  const ns = p.lat >= 0 ? 'N' : 'S';
  const eo = p.lon >= 0 ? 'E' : 'O';
  return `${Math.abs(p.lat).toFixed(4)}° ${ns}, ${Math.abs(p.lon).toFixed(4)}° ${eo}`;
}
