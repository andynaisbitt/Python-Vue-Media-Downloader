# backend/app/database/db.py
import sqlite3
import os
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            os.path.join(current_app.instance_path, 'youtube_downloader.db'),
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    
    with current_app.open_resource('database/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)