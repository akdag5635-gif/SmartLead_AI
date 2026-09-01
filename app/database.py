import sqlite3
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE_URL'])
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db(app):
    with app.app_context():
        db = get_db()

        # Yeni kurulumlarda tabloyu e-posta alanıyla oluşturur.
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

        # Render'daki mevcut veritabanında email sütunu yoksa ekler.
        kolonlar = db.execute(
            'PRAGMA table_info(leads)'
        ).fetchall()

        kolon_isimleri = [kolon['name'] for kolon in kolonlar]

        if 'email' not in kolon_isimleri:
            db.execute(
                'ALTER TABLE leads ADD COLUMN email TEXT'
            )

        db.commit()


def lead_ekle(isim, telefon, mesaj='', email=''):
    db = get_db()

    db.execute(
        '''
        INSERT INTO leads (isim, email, telefon, mesaj)
        VALUES (?, ?, ?, ?)
        ''',
        (isim, email, telefon, mesaj)
    )

    db.commit()


def tum_leadler():
    db = get_db()

    satirlar = db.execute(
        'SELECT * FROM leads ORDER BY tarih DESC'
    ).fetchall()

    return [dict(satir) for satir in satirlar]