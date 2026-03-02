# db.py
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CANDIDATES = [
    ROOT / "SQL" / "pokemon_cards.db",
    ROOT / "sql" / "pokemon_cards.db",
    ROOT / "pokemon_cards.db",
    ROOT / "SQL" / "pokemon_cards",
    ROOT / "sql" / "pokemon_cards",
    ROOT / "pokemon_cards",
]

def pick_db() -> Path:
    for p in CANDIDATES:
        if p.exists() and p.is_file():
            return p
    raise FileNotFoundError(
        "Could not find pokemon_cards db. Looked for:\n" + "\n".join(str(p) for p in CANDIDATES)
    )

DB_PATH = pick_db()

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn