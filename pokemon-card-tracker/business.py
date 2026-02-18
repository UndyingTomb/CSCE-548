# business.py
"""
Business layer: wraps the repositories, adds validation + "did it exist?" checks.
This layer is called by the service layer (api.py).
"""

from __future__ import annotations
from typing import Optional, Any, Dict

from repositories import (
    SetRepository,
    CardRepository,
    ConditionRepository,
    InventoryRepository,
)


class PokemonCardBusiness:
    def __init__(
        self,
        sets_repo: Optional[SetRepository] = None,
        cards_repo: Optional[CardRepository] = None,
        cond_repo: Optional[ConditionRepository] = None,
        inv_repo: Optional[InventoryRepository] = None,
    ):
        self.sets_repo = sets_repo or SetRepository()
        self.cards_repo = cards_repo or CardRepository()
        self.cond_repo = cond_repo or ConditionRepository()
        self.inv_repo = inv_repo or InventoryRepository()

    # -----------------------
    # SETS (CRUD)
    # -----------------------
    def create_set(self, set_code: str, set_name: str, release_date: str, era: str) -> int:
        if not set_code or not set_name:
            raise ValueError("set_code and set_name are required")
        return self.sets_repo.create(set_code, set_name, release_date, era)

    def list_sets(self):
        return self.sets_repo.get_all()

    def get_set(self, set_id: int):
        return self.sets_repo.get_by_id(set_id)

    def update_set(self, set_id: int, **fields: Any) -> bool:
        if not self.get_set(set_id):
            return False
        self.sets_repo.update(set_id, **fields)
        return True

    def delete_set(self, set_id: int) -> bool:
        if not self.get_set(set_id):
            return False
        self.sets_repo.delete(set_id)
        return True

    # -----------------------
    # CARDS (CRUD)
    # -----------------------
    def create_card(self, set_id: int, card_number: str, card_name: str, rarity: str, card_type: str) -> int:
        if set_id <= 0:
            raise ValueError("set_id must be positive")
        if not card_number or not card_name:
            raise ValueError("card_number and card_name are required")
        return self.cards_repo.create(set_id, card_number, card_name, rarity, card_type)

    def list_cards(self):
        return self.cards_repo.get_all()

    def get_card(self, card_id: int):
        return self.cards_repo.get_by_id(card_id)

    def list_cards_in_set(self, set_id: int):
        return self.cards_repo.get_by_set(set_id)

    def update_card(self, card_id: int, **fields: Any) -> bool:
        if not self.get_card(card_id):
            return False
        self.cards_repo.update(card_id, **fields)
        return True

    def delete_card(self, card_id: int) -> bool:
        if not self.get_card(card_id):
            return False
        self.cards_repo.delete(card_id)
        return True

    # -----------------------
    # CONDITIONS (CRUD-ish)
    # (your repo has create/get_all/update/delete; no get_by_id)
    # -----------------------
    def create_condition(self, condition_code: str, description: str) -> int:
        if not condition_code or not description:
            raise ValueError("condition_code and description are required")
        return self.cond_repo.create(condition_code, description)

    def list_conditions(self):
        return self.cond_repo.get_all()

    def update_condition(self, condition_id: int, **fields: Any) -> bool:
        # no get_by_id in repo; approximate existence check by scanning get_all
        exists = any(r["condition_id"] == condition_id for r in self.list_conditions())
        if not exists:
            return False
        self.cond_repo.update(condition_id, **fields)
        return True

    def delete_condition(self, condition_id: int) -> bool:
        exists = any(r["condition_id"] == condition_id for r in self.list_conditions())
        if not exists:
            return False
        self.cond_repo.delete(condition_id)
        return True

    # -----------------------
    # INVENTORY (CRUD)
    # -----------------------
    def create_inventory_item(self, **fields: Any) -> int:
        # enforce some sanity before DB constraints explode
        if fields.get("quantity", 1) < 0:
            raise ValueError("quantity must be >= 0")
        if fields.get("purchase_price", 0.0) < 0:
            raise ValueError("purchase_price must be >= 0")

        is_graded = int(fields.get("is_graded", 0))
        if is_graded == 1:
            if fields.get("graded_company") is None or fields.get("grade") is None:
                raise ValueError("graded_company and grade required if is_graded=1")
        else:
            # match your DB constraint expectation
            fields["graded_company"] = None
            fields["grade"] = None

        return self.inv_repo.create(**fields)

    def list_inventory(self):
        return self.inv_repo.get_all()

    def list_inventory_by_set(self, set_id: int):
        return self.inv_repo.get_by_set(set_id)

    def get_inventory_item(self, item_id: int):
        return self.inv_repo.get_by_id(item_id)

    def update_inventory_item(self, item_id: int, **fields: Any) -> bool:
        if not self.get_inventory_item(item_id):
            return False
        self.inv_repo.update(item_id, **fields)
        return True

    def delete_inventory_item(self, item_id: int) -> bool:
        if not self.get_inventory_item(item_id):
            return False
        self.inv_repo.delete(item_id)
        return True
