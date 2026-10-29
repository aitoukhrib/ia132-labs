// Lab 01 — Convertisseur d'unités.
// Complétez chaque fonction avec votre assistant, en suivant les 4 étapes du README :
// complétion en ligne, chat, édition, agent.

export const ZERO_ABSOLU_C = -273.15;
export const KM_PAR_MILE = 1.609344;

export type Unite = 'C' | 'F' | 'km' | 'mi';

/** Celsius → Fahrenheit. Lève une RangeError sous le zéro absolu. */
export function celsiusVersFahrenheit(c: number): number {
  throw new Error('À compléter');
}

/** Fahrenheit → Celsius. Lève une RangeError si le résultat est sous le zéro absolu. */
export function fahrenheitVersCelsius(f: number): number {
  throw new Error('À compléter');
}

/** Kilomètres → miles. Lève une RangeError si la distance est négative. */
export function kmVersMiles(km: number): number {
  throw new Error('À compléter');
}

/** Miles → kilomètres. Lève une RangeError si la distance est négative. */
export function milesVersKm(miles: number): number {
  throw new Error('À compléter');
}

/**
 * Convertit `valeur` de l'unité `de` vers l'unité `vers`.
 * Même unité des deux côtés : la valeur est retournée telle quelle.
 * Paire non prise en charge (ex. 'C' vers 'km') : RangeError.
 */
export function convertir(valeur: number, de: Unite, vers: Unite): number {
  throw new Error('À compléter');
}
