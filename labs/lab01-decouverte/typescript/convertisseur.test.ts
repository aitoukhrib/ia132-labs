// Étapes 1 à 3 : ces tests doivent tous passer.
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { celsiusVersFahrenheit, convertir, fahrenheitVersCelsius, kmVersMiles, milesVersKm } from './convertisseur.ts';

const proche = (a: number, b: number, eps = 1e-6) => assert.ok(Math.abs(a - b) < eps, `${a} ≉ ${b}`);

test('celsius → fahrenheit', () => {
  proche(celsiusVersFahrenheit(0), 32);
  proche(celsiusVersFahrenheit(100), 212);
  proche(celsiusVersFahrenheit(-40), -40);
  proche(celsiusVersFahrenheit(37), 98.6);
});

test('fahrenheit → celsius', () => {
  proche(fahrenheitVersCelsius(32), 0);
  proche(fahrenheitVersCelsius(212), 100);
});

test('sous le zéro absolu', () => {
  assert.throws(() => celsiusVersFahrenheit(-300), RangeError);
  assert.throws(() => fahrenheitVersCelsius(-500), RangeError);
});

test('distances', () => {
  proche(kmVersMiles(1.609344), 1);
  proche(milesVersKm(26.2), 42.165, 1e-3);
  assert.throws(() => kmVersMiles(-1), RangeError);
  assert.throws(() => milesVersKm(-0.5), RangeError);
});

test('convertir aiguille vers la bonne fonction', () => {
  proche(convertir(100, 'C', 'F'), 212);
  proche(convertir(10, 'km', 'mi'), 6.2137, 1e-4);
  assert.equal(convertir(5, 'mi', 'mi'), 5);
  assert.throws(() => convertir(1, 'C', 'km'), RangeError);
});
