# main.py
from __future__ import annotations

import inspect
from typing import Any, Dict, Optional

from repositories import SetRepository, CardRepository, InventoryRepository, ConditionRepository

sets_repo = SetRepository()
cards_repo = CardRepository()
inv_repo = InventoryRepository()

# ConditionRepository might exist in your repo; if it doesn't, we won't crash.
try:
    cond_repo = ConditionRepository()
except Exception:
    cond_repo = None


# -----------------------------
# Helpers
# -----------------------------
def to_dict(row):
    return dict(row) if row is not None else None


def prompt_int(label: str, allow_blank: bool = False) -> Optional[int]:
    while True:
        raw = input(label).strip()
        if raw == "" and allow_blank:
            return None
        try:
            return int(raw)
        except ValueError:
            print("Enter an integer.")


def prompt_float(label: str, allow_blank: bool = False) -> Optional[float]:
    while True:
        raw = input(label).strip()
        if raw == "" and allow_blank:
            return None
        try:
            return float(raw)
        except ValueError:
            print("Enter a number.")


def prompt_str(label: str, allow_blank: bool = False) -> Optional[str]:
    raw = input(label).strip()
    if raw == "" and allow_blank:
        return None
    return raw


def repo_supports_kwargs(method) -> bool:
    """True if the method accepts **kwargs (VAR_KEYWORD)."""
    sig = inspect.signature(method)
    return any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())


def call_update(repo, method_name: str, obj_id: int, fields: Dict[str, Any]) -> None:
    """
    Calls repo.update in a way that works for either:
      update(id, **fields)
    OR
      update(id, field1, field2, ...)
    """
    method = getattr(repo, method_name)

    if repo_supports_kwargs(method):
        method(obj_id, **fields)
        return

    sig = inspect.signature(method)
    param_names = list(sig.parameters.keys())
    field_params = param_names[1:]  # skip the id
    args = [fields.get(name) for name in field_params]
    method(obj_id, *args)


def call_create(repo, method_name: str, fields: Dict[str, Any]) -> int:
    """
    Calls repo.create in a way that works for either:
      create(**fields)
    OR
      create(field1, field2, ...)
    """
    method = getattr(repo, method_name)

    if repo_supports_kwargs(method):
        return method(**fields)

    sig = inspect.signature(method)
    param_names = list(sig.parameters.keys())
    args = [fields.get(name) for name in param_names]
    return method(*args)


# -----------------------------
# Menu
# -----------------------------
def menu():
    print("\n=== Pokémon Card Tracker (Project 1 Console) ===")
    print("1) List sets")
    print("2) List cards in a set")
    print("3) List inventory (owned cards) by set")
    print("----- CRUD: Sets -----")
    print("4) Add set")
    print("5) Update set")
    print("6) Delete set")
    print("----- CRUD: Cards -----")
    print("7) Add card")
    print("8) Update card")
    print("9) Delete card")
    print("----- CRUD: Inventory -----")
    print("10) Add inventory item")
    print("11) Update inventory item")
    print("12) Delete inventory item")
    print("13) List conditions (help)")
    print("0) Exit")


# -----------------------------
# Original Features (kept)
# -----------------------------
def list_sets():
    rows = list(sets_repo.get_all())
    if len(rows) == 0:
        print("(no sets)")
        return
    for r in rows:
        r = dict(r)
        print(f"{r['set_id']:>3} | {r['set_code']:<8} | {r['set_name']:<28} | {r['release_date']} | {r['era']}")


def list_cards_in_set():
    set_id = prompt_int("Enter set_id: ")
    rows = list(cards_repo.get_by_set(set_id))
    if len(rows) == 0:
        print("(no cards found for that set_id)")
        return
    for r in rows:
        r = dict(r)
        print(
            f"{r['card_id']:>4} | set={r['set_id']:<3} | #{r['card_number']:<10} | "
            f"{r['card_name']:<28} | {r['rarity']:<12} | {r['card_type']}"
        )


def list_inventory():
    print("\nSelect a set to filter your inventory:")
    list_sets()
    raw = input("Enter set_id (or press Enter to show all owned cards): ").strip()

    if raw == "":
        rows = inv_repo.get_all()
    else:
        set_id = int(raw)
        rows = inv_repo.get_by_set(set_id)

    # Force to list so empty results are detectable (prevents “blank”)
    rows = list(rows)

    if len(rows) == 0:
        print("(no owned cards found for that set)")
        return

    for r in rows:
        r = dict(r)  # sqlite3.Row -> dict (so .get works)

        set_code = r.get("set_code", "")
        card_number = r.get("card_number", "")
        card_name = r.get("card_name", "")
        rarity = r.get("rarity", "")
        cond_code = r.get("condition_code", r.get("condition_id", ""))

        graded = ""
        if r.get("is_graded", 0) == 1:
            graded = f" | {r.get('graded_company')} {r.get('grade')}"

        print(
            f"Item {r['item_id']:>3} | {set_code} {card_number:<10} {card_name:<24}"
            f"| {rarity:<12} | cond={cond_code} | qty={r['quantity']} | paid=${float(r['purchase_price']):.2f}{graded}"
        )


def list_conditions():
    if cond_repo is None:
        print("(ConditionRepository not available in your repositories.py)")
        return
    rows = list(cond_repo.get_all())
    if len(rows) == 0:
        print("(no conditions)")
        return
    for r in rows:
        r = dict(r)
        print(f"{r['condition_id']:>2} | {r['condition_code']:<4} | {r['description']}")


# -----------------------------
# CRUD: Sets
# -----------------------------
def add_set():
    print("\n--- Add Set ---")
    fields = {
        "set_code": prompt_str("set_code (e.g., SV1): "),
        "set_name": prompt_str("set_name: "),
        "release_date": prompt_str("release_date (YYYY-MM-DD): "),
        "era": prompt_str("era: "),
    }
    new_id = call_create(sets_repo, "create", fields)
    print(f"Created set_id = {new_id}")


def update_set():
    print("\n--- Update Set ---")
    set_id = prompt_int("set_id to update: ")
    current = sets_repo.get_by_id(set_id) if hasattr(sets_repo, "get_by_id") else None
    cur = to_dict(current) if current else {}

    print("Press Enter to keep current value.")
    fields = {
        "set_code": prompt_str(f"set_code [{cur.get('set_code','')}]: ", allow_blank=True) or cur.get("set_code"),
        "set_name": prompt_str(f"set_name [{cur.get('set_name','')}]: ", allow_blank=True) or cur.get("set_name"),
        "release_date": prompt_str(f"release_date [{cur.get('release_date','')}]: ", allow_blank=True) or cur.get("release_date"),
        "era": prompt_str(f"era [{cur.get('era','')}]: ", allow_blank=True) or cur.get("era"),
    }
    call_update(sets_repo, "update", set_id, fields)
    print("Updated set.")


def delete_set():
    print("\n--- Delete Set ---")
    set_id = prompt_int("set_id to delete: ")
    sets_repo.delete(set_id)
    print("Deleted (if it existed and FK constraints allowed).")


# -----------------------------
# CRUD: Cards
# -----------------------------
def add_card():
    print("\n--- Add Card ---")
    list_sets()

    set_id = prompt_int("set_id: ")
    card_number = prompt_str("card_number (e.g., 080/202): ")
    card_name = prompt_str("card_name: ")
    rarity = prompt_str("rarity (Common/Uncommon/Rare/Double Rare/Ultra Rare/IR/SIR/Hyper Rare/Promo): ")
    card_type = prompt_str("card_type (Pokémon/Trainer/Energy): ")

    # Normalize common lowercase input to satisfy DB CHECK constraints (case-sensitive)
    rarity_map = {
        "common": "Common",
        "uncommon": "Uncommon",
        "rare": "Rare",
        "double rare": "Double Rare",
        "ultra rare": "Ultra Rare",
        "ir": "IR",
        "sir": "SIR",
        "hyper rare": "Hyper Rare",
        "promo": "Promo",
    }
    ctype_map = {
        "pokemon": "Pokémon",
        "pokémon": "Pokémon",
        "trainer": "Trainer",
        "energy": "Energy",
    }

    rarity_norm = rarity_map.get(rarity.strip().lower(), rarity.strip())
    ctype_norm = ctype_map.get(card_type.strip().lower(), card_type.strip())

    fields = {
        "set_id": set_id,
        "card_number": card_number,
        "card_name": card_name,
        "rarity": rarity_norm,
        "card_type": ctype_norm,
    }

    new_id = call_create(cards_repo, "create", fields)
    print(f"Created card_id = {new_id}")


def update_card():
    print("\n--- Update Card ---")
    card_id = prompt_int("card_id to update: ")
    current = cards_repo.get_by_id(card_id) if hasattr(cards_repo, "get_by_id") else None
    cur = to_dict(current) if current else {}

    print("Press Enter to keep current value.")
    fields = {
        "set_id": prompt_int(f"set_id [{cur.get('set_id','')}]: ", allow_blank=True) or cur.get("set_id"),
        "card_number": prompt_str(f"card_number [{cur.get('card_number','')}]: ", allow_blank=True) or cur.get("card_number"),
        "card_name": prompt_str(f"card_name [{cur.get('card_name','')}]: ", allow_blank=True) or cur.get("card_name"),
        "rarity": prompt_str(f"rarity [{cur.get('rarity','')}]: ", allow_blank=True) or cur.get("rarity"),
        "card_type": prompt_str(f"card_type [{cur.get('card_type','')}]: ", allow_blank=True) or cur.get("card_type"),
    }
    call_update(cards_repo, "update", card_id, fields)
    print("Updated card.")


def delete_card():
    print("\n--- Delete Card ---")
    card_id = prompt_int("card_id to delete: ")
    cards_repo.delete(card_id)
    print("Deleted (if it existed).")


# -----------------------------
# CRUD: Inventory
# -----------------------------
def add_inventory_item():
    print("\n--- Add Inventory Item ---")
    print("Helpful: list conditions:")
    list_conditions()

    fields = {
        "card_id": prompt_int("card_id: "),
        "condition_id": prompt_int("condition_id: "),
        "is_foil": prompt_int("is_foil (0/1) [0]: ", allow_blank=True) or 0,
        "is_graded": prompt_int("is_graded (0/1) [0]: ", allow_blank=True) or 0,
        "graded_company": None,
        "grade": None,
        "quantity": prompt_int("quantity [1]: ", allow_blank=True) or 1,
        "purchase_price": prompt_float("purchase_price [0.0]: ", allow_blank=True) or 0.0,
        "purchase_date": prompt_str("purchase_date (YYYY-MM-DD) [blank]: ", allow_blank=True),
        "notes": prompt_str("notes [blank]: ", allow_blank=True),
    }

    if fields["is_graded"] == 1:
        fields["graded_company"] = prompt_str("graded_company (PSA/BGS/CGC): ")
        fields["grade"] = prompt_float("grade (1.0 - 10.0): ")

    new_id = call_create(inv_repo, "create", fields)
    print(f"Created item_id = {new_id}")


def update_inventory_item():
    print("\n--- Update Inventory Item ---")
    item_id = prompt_int("item_id to update: ")
    current = inv_repo.get_by_id(item_id) if hasattr(inv_repo, "get_by_id") else None
    cur = to_dict(current) if current else {}

    print("Press Enter to keep current value.")
    fields = {
        "card_id": prompt_int(f"card_id [{cur.get('card_id','')}]: ", allow_blank=True) or cur.get("card_id"),
        "condition_id": prompt_int(f"condition_id [{cur.get('condition_id','')}]: ", allow_blank=True) or cur.get("condition_id"),
        "is_foil": prompt_int(f"is_foil (0/1) [{cur.get('is_foil',0)}]: ", allow_blank=True),
        "is_graded": prompt_int(f"is_graded (0/1) [{cur.get('is_graded',0)}]: ", allow_blank=True),
        "graded_company": None,
        "grade": None,
        "quantity": prompt_int(f"quantity [{cur.get('quantity',1)}]: ", allow_blank=True) or cur.get("quantity", 1),
        "purchase_price": prompt_float(f"purchase_price [{cur.get('purchase_price',0.0)}]: ", allow_blank=True) or cur.get("purchase_price", 0.0),
        "purchase_date": prompt_str(f"purchase_date [{cur.get('purchase_date','')}]: ", allow_blank=True) or cur.get("purchase_date"),
        "notes": prompt_str(f"notes [{cur.get('notes','')}]: ", allow_blank=True) or cur.get("notes"),
    }

    if fields["is_foil"] is None:
        fields["is_foil"] = cur.get("is_foil", 0)
    if fields["is_graded"] is None:
        fields["is_graded"] = cur.get("is_graded", 0)

    if fields["is_graded"] == 1:
        fields["graded_company"] = prompt_str(f"graded_company [{cur.get('graded_company','PSA')}]: ", allow_blank=True) or cur.get("graded_company")
        fields["grade"] = prompt_float(f"grade [{cur.get('grade','9.0')}]: ", allow_blank=True) or cur.get("grade")
    else:
        fields["graded_company"] = None
        fields["grade"] = None

    call_update(inv_repo, "update", item_id, fields)
    print("Updated inventory item.")


def delete_inventory_item():
    print("\n--- Delete Inventory Item ---")
    item_id = prompt_int("item_id to delete: ")
    inv_repo.delete(item_id)
    print("Deleted (if it existed).")


# -----------------------------
# Main loop
# -----------------------------
def main():
    while True:
        menu()
        choice = input("Choose: ").strip()

        if choice == "1":
            list_sets()
        elif choice == "2":
            list_cards_in_set()
        elif choice == "3":
            list_inventory()

        elif choice == "4":
            add_set()
        elif choice == "5":
            update_set()
        elif choice == "6":
            delete_set()

        elif choice == "7":
            add_card()
        elif choice == "8":
            update_card()
        elif choice == "9":
            delete_card()

        elif choice == "10":
            add_inventory_item()
        elif choice == "11":
            update_inventory_item()
        elif choice == "12":
            delete_inventory_item()

        elif choice == "13":
            list_conditions()

        elif choice == "0":
            print("Bye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
