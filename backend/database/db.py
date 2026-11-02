import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def connect(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    return connection


def initialize(path: Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inputs_json TEXT NOT NULL,
                predicted_yield REAL NOT NULL,
                predicted_at TEXT NOT NULL
            )
            """
        )


def save_prediction(path: Path, inputs: dict, predicted_yield: float) -> int:
    timestamp = datetime.now(timezone.utc).isoformat()
    with connect(path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO predictions (inputs_json, predicted_yield, predicted_at)
            VALUES (?, ?, ?)
            """,
            (json.dumps(inputs), predicted_yield, timestamp),
        )
        return int(cursor.lastrowid)


def list_predictions(path: Path, limit: int = 100) -> list[dict]:
    with connect(path) as connection:
        rows = connection.execute(
            """
            SELECT id, inputs_json, predicted_yield, predicted_at
            FROM predictions ORDER BY id DESC LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [
        {
            "id": row["id"],
            "inputs": json.loads(row["inputs_json"]),
            "predicted_yield": row["predicted_yield"],
            "predicted_at": row["predicted_at"],
        }
        for row in rows
    ]


def prediction_count(path: Path) -> int:
    with connect(path) as connection:
        return int(connection.execute("SELECT COUNT(*) FROM predictions").fetchone()[0])
