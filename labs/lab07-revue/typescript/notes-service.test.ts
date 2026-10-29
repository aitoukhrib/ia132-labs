// Tests fonctionnels (verts : « la PR marche ») puis tests de sécurité (rouges).
// Les tests de sécurité ne sont révélés qu'APRÈS votre revue (étape 3 du README).
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { beforeEach, test } from 'node:test';
import { NotesService } from './notes-service.ts';

let s: NotesService;
beforeEach(() => {
  process.env.NOTES_SECRET = 'secret-de-test';
  s = new NotesService();
});

// ── Fonctionnel ────────────────────────────────────────────────────────────
test('inscription puis connexion', () => {
  const uid = s.inscrire('ana@exemple.ca', 'Correct-Cheval-42');
  assert.equal(s.connecter('ana@exemple.ca', 'Correct-Cheval-42'), uid);
});

test('mauvais mot de passe', () => {
  s.inscrire('ana@exemple.ca', 'Correct-Cheval-42');
  assert.equal(s.connecter('ana@exemple.ca', 'mauvais'), null);
});

test('lire sa propre note', () => {
  const uid = s.inscrire('ana@exemple.ca', 'Correct-Cheval-42');
  const nid = s.ajouterNote(uid, 'Acheter du café');
  assert.equal(s.lireNote(uid, nid), 'Acheter du café');
});

test('jeton stable et propre à chaque utilisateur', () => {
  assert.equal(s.jeton(1), s.jeton(1));
  assert.notEqual(s.jeton(1), s.jeton(2));
});

// ── Sécurité ───────────────────────────────────────────────────────────────
test('sécurité : injection SQL à la connexion', () => {
  s.inscrire('ana@exemple.ca', 'Correct-Cheval-42');
  assert.equal(s.connecter("ana@exemple.ca' --", "n'importe quoi"), null);
});

test('sécurité : apostrophe dans le courriel', () => {
  const uid = s.inscrire("o'brien@exemple.ca", 'Correct-Cheval-42');
  assert.equal(s.connecter("o'brien@exemple.ca", 'Correct-Cheval-42'), uid);
});

test('sécurité : mots de passe salés et lents', () => {
  s.inscrire('a@exemple.ca', 'meme-mot-de-passe');
  s.inscrire('b@exemple.ca', 'meme-mot-de-passe');
  const [h1, h2] = (s.bd.prepare('select password from users order by id').all() as { password: string }[]).map((r) => r.password);
  assert.notEqual(h1, h2, 'même mot de passe, même empreinte : il manque un sel');
  const md5 = createHash('md5').update('meme-mot-de-passe').digest('hex');
  assert.ok(![h1, h2].includes(md5), "MD5 n'est pas fait pour les mots de passe");
});

test('sécurité : pas d’accès aux notes des autres', () => {
  const ana = s.inscrire('ana@exemple.ca', 'Correct-Cheval-42');
  const bob = s.inscrire('bob@exemple.ca', 'Batterie-Agrafe-7');
  const nid = s.ajouterNote(ana, 'Mon NIP : 1234');
  assert.equal(s.lireNote(bob, nid), null);
});

test('sécurité : aucun secret dans le code', () => {
  const source = readFileSync(new URL('./notes-service.ts', import.meta.url), 'utf8');
  assert.doesNotMatch(source, /SECRET\w*\s*=\s*['"`]/, 'secret en dur : lisez-le dans process.env');
});
