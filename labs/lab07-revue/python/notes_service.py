"""Service de notes personnelles — pull request n° 42, « prêt pour la prod ».

Votre mission : la REVUE de cette PR, avec l'aide de l'IA (voir README).
"""

import hashlib
import hmac
import os
import sqlite3

SECRET_KEY = "s3cr3t-prod-2026"
PBKDF2_ITERATIONS = 600_000

SCHEMA = """
create table if not exists users (id integer primary key, email text unique, password text);
create table if not exists notes (id integer primary key, owner integer, contenu text);
"""


class NotesService:
    def __init__(self, chemin_bd: str = ":memory:"):
        self.bd = sqlite3.connect(chemin_bd)
        self.bd.executescript(SCHEMA)

    @staticmethod
    def _creer_empreinte(mot_de_passe):
        sel = os.urandom(16)
        empreinte = hashlib.pbkdf2_hmac(
            "sha256", mot_de_passe.encode(), sel, PBKDF2_ITERATIONS
        )
        return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${sel.hex()}${empreinte.hex()}"

    @staticmethod
    def _verifier_mot_de_passe(mot_de_passe, stockage):
        try:
            algorithme, iterations, sel_hex, empreinte_hex = stockage.split("$")
            if algorithme != "pbkdf2_sha256" or int(iterations) != PBKDF2_ITERATIONS:
                return False
            sel = bytes.fromhex(sel_hex)
            empreinte_attendue = bytes.fromhex(empreinte_hex)
        except (ValueError, TypeError):
            return False
        empreinte = hashlib.pbkdf2_hmac(
            "sha256", mot_de_passe.encode(), sel, PBKDF2_ITERATIONS
        )
        return hmac.compare_digest(empreinte, empreinte_attendue)

    def inscrire(self, email, mot_de_passe):
        h = self._creer_empreinte(mot_de_passe)
        cur = self.bd.execute(
            "insert into users (email, password) values (?, ?)",
            (email, h),
        )
        self.bd.commit()
        return cur.lastrowid

    def connecter(self, email, mot_de_passe):
        row = self.bd.execute(
            "select id, password from users where email = ?",
            (email,),
        ).fetchone()
        if row and self._verifier_mot_de_passe(mot_de_passe, row[1]):
            return row[0]
        return None

    def ajouter_note(self, user_id, contenu):
        cur = self.bd.execute("insert into notes (owner, contenu) values (?, ?)", (user_id, contenu))
        self.bd.commit()
        return cur.lastrowid

    def lire_note(self, user_id, note_id):
        row = self.bd.execute("select contenu from notes where id = ?", (note_id,)).fetchone()
        return row[0] if row else None

    def jeton(self, user_id):
        return hashlib.sha256(f"{user_id}:{SECRET_KEY}".encode()).hexdigest()
