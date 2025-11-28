import sqlite3
from pathlib import Path
import os

def get_db():
    DB_PATH = Path(os.getenv("DB_PATH", "app/data/database.db"))
    print(f"Using database at: {DB_PATH}")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # allows row["col"] style access
    return conn


def init_db():
    db = get_db()
    cur = db.cursor()

    # == AUDIO TABLE ==
    cur.execute("""
    CREATE TABLE IF NOT EXISTS audio_transcriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        transcript TEXT NOT NULL,
        segments_json TEXT NOT NULL,
        embedding BLOB NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # == VIDEO TABLE (future — not active yet) ==
    cur.execute("""
    CREATE TABLE IF NOT EXISTS video_index (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        summary TEXT NOT NULL,
        objects_json TEXT NOT NULL,
        embedding BLOB NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    db.commit()
