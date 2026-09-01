import sqlite3
import psycopg

from flask import current_app, g
from psycopg.rows import dict_row


def postgres_mi():
    database_url = current_app.config['DATABASE_URL']

    return (
        database_url.startswith('postgresql://')
        or database_url.startswith('postgres://')
    )


def get_db():
    if 'db' not in g:

        database_url = current_app.config['DATABASE_URL']

        if postgres_mi():
            g.db = psycopg.connect(
                database_url,
                row_factory=dict_row
            )

        else:
            g.db = sqlite3.connect(database_url)
            g.db.row_factory = sqlite3.Row

    return g.db


def close_db(error=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db(app):

    app.teardown_appcontext(close_db)

    with app.app_context():

        db = get_db()

        if postgres_mi():

            with db.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS leads (
                        id SERIAL PRIMARY KEY,
                        isim TEXT NOT NULL,
                        email TEXT,
                        telefon TEXT NOT NULL,
                        mesaj TEXT,
                        tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                cursor.execute('''
                    ALTER TABLE leads
                    ADD COLUMN IF NOT EXISTS email TEXT
                ''')

            db.commit()

        else:

            db.execute('''
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    isim TEXT NOT NULL,
                    email TEXT,
                    telefon TEXT NOT NULL,
                    mesaj TEXT,
                    tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            kolonlar = db.execute(
                'PRAGMA table_info(leads)'
            ).fetchall()

            kolon_isimleri = [
                kolon['name']
                for kolon in kolonlar
            ]

            if 'email' not in kolon_isimleri:
                db.execute(
                    'ALTER TABLE leads ADD COLUMN email TEXT'
                )

            db.commit()


def lead_ekle(isim, telefon, mesaj='', email=''):

    db = get_db()

    if postgres_mi():

        with db.cursor() as cursor:
            cursor.execute(
                '''
                INSERT INTO leads
                (isim, email, telefon, mesaj)
                VALUES (%s, %s, %s, %s)
                ''',
                (isim, email, telefon, mesaj)
            )

    else:

        db.execute(
            '''
            INSERT INTO leads
            (isim, email, telefon, mesaj)
            VALUES (?, ?, ?, ?)
            ''',
            (isim, email, telefon, mesaj)
        )

    db.commit()


def tum_leadler():

    db = get_db()

    if postgres_mi():

        with db.cursor() as cursor:
            cursor.execute(
                '''
                SELECT *
                FROM leads
                ORDER BY tarih DESC
                '''
            )

            satirlar = cursor.fetchall()

            return [dict(satir) for satir in satirlar]

    else:

        satirlar = db.execute(
            '''
            SELECT *
            FROM leads
            ORDER BY tarih DESC
            '''
        ).fetchall()

        return [dict(satir) for satir in satirlar]