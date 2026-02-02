from typing import Any, Optional
from db import get_conn

# -----------------------
# card_set CRUD
# -----------------------
class SetRepository:
    def create(self, set_code: str, set_name: str, release_date: str, era: str) -> int:
        with get_conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO card_set(set_code, set_name, release_date, era)
                VALUES (?,?,?,?)
                """,
                (set_code, set_name, release_date, era),
            )
            return int(cur.lastrowid)

    def get_all(self):
        with get_conn() as conn:
            return conn.execute("SELECT * FROM card_set ORDER BY release_date;").fetchall()

    def get_by_id(self, set_id: int):
        with get_conn() as conn:
            return conn.execute("SELECT * FROM card_set WHERE set_id = ?;", (set_id,)).fetchone()

    def update(self, set_id: int, **fields: Any) -> None:
        allowed = {"set_code", "set_name", "release_date", "era"}
        updates = [(k, v) for k, v in fields.items() if k in allowed]
        if not updates:
            return
        set_clause = ", ".join([f"{k} = ?" for k, _ in updates])
        params = [v for _, v in updates] + [set_id]
        with get_conn() as conn:
            conn.execute(f"UPDATE card_set SET {set_clause} WHERE set_id = ?;", params)

    def delete(self, set_id: int) -> None:
        with get_conn() as conn:
            conn.execute("DELETE FROM card_set WHERE set_id = ?;", (set_id,))


# -----------------------
# card CRUD
# -----------------------
class CardRepository:
    def create(self, set_id: int, card_number: str, card_name: str, rarity: str, card_type: str) -> int:
        with get_conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO card(set_id, card_number, card_name, rarity, card_type)
                VALUES (?,?,?,?,?)
                """,
                (set_id, card_number, card_name, rarity, card_type),
            )
            return int(cur.lastrowid)

    def get_all(self):
        with get_conn() as conn:
            return conn.execute(
                """
                SELECT c.*, s.set_code, s.set_name
                FROM card c
                JOIN card_set s ON s.set_id = c.set_id
                ORDER BY s.release_date, c.card_number;
                """
            ).fetchall()

    def get_by_id(self, card_id: int):
        with get_conn() as conn:
            return conn.execute("SELECT * FROM card WHERE card_id = ?;", (card_id,)).fetchone()

    def get_by_set(self, set_id: int):
        with get_conn() as conn:
            return conn.execute(
                "SELECT * FROM card WHERE set_id = ? ORDER BY card_number;",
                (set_id,),
            ).fetchall()

    def update(self, card_id: int, **fields: Any) -> None:
        allowed = {"set_id", "card_number", "card_name", "rarity", "card_type"}
        updates = [(k, v) for k, v in fields.items() if k in allowed]
        if not updates:
            return
        set_clause = ", ".join([f"{k} = ?" for k, _ in updates])
        params = [v for _, v in updates] + [card_id]
        with get_conn() as conn:
            conn.execute(f"UPDATE card SET {set_clause} WHERE card_id = ?;", params)

    def delete(self, card_id: int) -> None:
        with get_conn() as conn:
            conn.execute("DELETE FROM card WHERE card_id = ?;", (card_id,))


# -----------------------
# card_condition CRUD
# -----------------------
class ConditionRepository:
    def create(self, condition_code: str, description: str) -> int:
        with get_conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO card_condition(condition_code, description)
                VALUES (?,?)
                """,
                (condition_code, description),
            )
            return int(cur.lastrowid)

    def get_all(self):
        with get_conn() as conn:
            return conn.execute("SELECT * FROM card_condition ORDER BY condition_id;").fetchall()

    def update(self, condition_id: int, **fields: Any) -> None:
        allowed = {"condition_code", "description"}
        updates = [(k, v) for k, v in fields.items() if k in allowed]
        if not updates:
            return
        set_clause = ", ".join([f"{k} = ?" for k, _ in updates])
        params = [v for _, v in updates] + [condition_id]
        with get_conn() as conn:
            conn.execute(f"UPDATE card_condition SET {set_clause} WHERE condition_id = ?;", params)

    def delete(self, condition_id: int) -> None:
        with get_conn() as conn:
            conn.execute("DELETE FROM card_condition WHERE condition_id = ?;", (condition_id,))


# -----------------------
# inventory_item CRUD
# -----------------------
class InventoryRepository:
    def create(
        self,
        card_id: int,
        condition_id: int,
        is_foil: int = 0,
        is_graded: int = 0,
        graded_company: Optional[str] = None,
        grade: Optional[float] = None,
        quantity: int = 1,
        purchase_price: float = 0.0,
        purchase_date: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> int:
        with get_conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO inventory_item
                (card_id, condition_id, is_foil, is_graded, graded_company, grade,
                 quantity, purchase_price, purchase_date, notes)
                VALUES (?,?,?,?,?,?,?,?,?,?)
                """,
                (card_id, condition_id, is_foil, is_graded, graded_company, grade,
                 quantity, purchase_price, purchase_date, notes),
            )
            return int(cur.lastrowid)

    def get_all(self):
        with get_conn() as conn:
            return conn.execute(
                """
                SELECT i.*, c.card_name, c.card_number, c.rarity, s.set_code, s.set_name, cc.condition_code
                FROM inventory_item i
                JOIN card c ON c.card_id = i.card_id
                JOIN card_set s ON s.set_id = c.set_id
                JOIN card_condition cc ON cc.condition_id = i.condition_id
                ORDER BY s.release_date, c.card_number;
                """
            ).fetchall()

    def get_by_set(self, set_id: int):
        with get_conn() as conn:
            return conn.execute(
                """
                SELECT i.*, c.card_name, c.card_number, c.rarity, s.set_code, s.set_name, cc.condition_code
                FROM inventory_item i
                JOIN card c ON c.card_id = i.card_id
                JOIN card_set s ON s.set_id = c.set_id
                JOIN card_condition cc ON cc.condition_id = i.condition_id
                WHERE c.set_id = ?
                ORDER BY c.card_number;
                """,
                (set_id,),
            ).fetchall()


    def get_by_id(self, item_id: int):
        with get_conn() as conn:
            return conn.execute("SELECT * FROM inventory_item WHERE item_id = ?;", (item_id,)).fetchone()

    def update(self, item_id: int, **fields: Any) -> None:
        allowed = {
            "card_id", "condition_id", "is_foil", "is_graded", "graded_company", "grade",
            "quantity", "purchase_price", "purchase_date", "notes"
        }
        updates = [(k, v) for k, v in fields.items() if k in allowed]
        if not updates:
            return
        set_clause = ", ".join([f"{k} = ?" for k, _ in updates])
        params = [v for _, v in updates] + [item_id]
        with get_conn() as conn:
            conn.execute(f"UPDATE inventory_item SET {set_clause} WHERE item_id = ?;", params)

    def delete(self, item_id: int) -> None:
        with get_conn() as conn:
            conn.execute("DELETE FROM inventory_item WHERE item_id = ?;", (item_id,))
