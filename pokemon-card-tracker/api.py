# api.py
"""
Pokemon Card Tracker API (Service Layer)

Run:
  source .venv/bin/activate
  uvicorn api:app --reload

Docs:
  http://127.0.0.1:8000/docs
"""
# api.py
from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from business import PokemonCardBusiness

app = FastAPI(title="Pokemon Card Tracker API", version="3.1")

# CORS so your browser client (port 5500) can call the API (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

biz = PokemonCardBusiness()


def row_to_dict(r):
    return dict(r) if r is not None else None


# -----------------------------
# SETS (GET all, GET one, GET subset)
# -----------------------------
@app.get("/sets")
def get_sets(set_code: Optional[str] = None, era: Optional[str] = None):
    rows = [row_to_dict(r) for r in biz.list_sets()]
    if set_code:
        sc = set_code.lower()
        rows = [r for r in rows if sc in str(r.get("set_code", "")).lower()]
    if era:
        e = era.lower()
        rows = [r for r in rows if e in str(r.get("era", "")).lower()]
    return rows


@app.get("/sets/{set_id}")
def get_set(set_id: int):
    r = biz.get_set(set_id)
    if not r:
        raise HTTPException(404, "Set not found")
    return row_to_dict(r)


# -----------------------------
# CARDS (GET all, GET one, GET subset)
# -----------------------------
@app.get("/cards")
def get_cards(
    set_id: Optional[int] = None,
    rarity: Optional[str] = None,
):
    # subset by set_id uses list_cards_in_set
    if set_id is not None:
        rows = [row_to_dict(r) for r in biz.list_cards_in_set(set_id)]
    else:
        rows = [row_to_dict(r) for r in biz.list_cards()]

    # subset by rarity
    if rarity:
        rr = rarity.lower()
        rows = [r for r in rows if rr in str(r.get("rarity", "")).lower()]

    return rows


@app.get("/cards/{card_id}")
def get_card(card_id: int):
    r = biz.get_card(card_id)
    if not r:
        raise HTTPException(404, "Card not found")
    return row_to_dict(r)


# Keep your nice subset endpoint too (optional but helpful)
@app.get("/sets/{set_id}/cards")
def get_cards_in_set(set_id: int, rarity: Optional[str] = None):
    rows = [row_to_dict(r) for r in biz.list_cards_in_set(set_id)]
    if rarity:
        rr = rarity.lower()
        rows = [r for r in rows if rr in str(r.get("rarity", "")).lower()]
    return rows


# -----------------------------
# CONDITIONS (GET all, GET one, GET subset)
# -----------------------------
@app.get("/conditions")
def get_conditions(query: Optional[str] = None):
    rows = [row_to_dict(r) for r in biz.list_conditions()]

    # subset: query in condition_code or description
    if query:
        q = query.lower()
        rows = [
            r for r in rows
            if q in str(r.get("condition_code", "")).lower()
            or q in str(r.get("description", "")).lower()
        ]
    return rows


@app.get("/conditions/{condition_id}")
def get_condition(condition_id: int):
    # If your business layer has get_condition(), use it:
    if hasattr(biz, "get_condition"):
        r = biz.get_condition(condition_id)
        if not r:
            raise HTTPException(404, "Condition not found")
        return row_to_dict(r)

    # Fallback (scan list) so GET-one works even if business lacks method
    rows = [row_to_dict(r) for r in biz.list_conditions()]
    for r in rows:
        if r is not None and int(r.get("condition_id", -1)) == condition_id:
            return r
    raise HTTPException(404, "Condition not found")


# -----------------------------
# INVENTORY (GET all, GET one, GET subset)
# Subset demo: filter by graded vs ungraded
# -----------------------------
@app.get("/inventory")
def get_inventory(
    set_id: Optional[int] = None,
    is_graded: Optional[int] = None,  # 0 or 1
):
    # subset by set (optional)
    if set_id is not None:
        rows = [row_to_dict(r) for r in biz.list_inventory_by_set(set_id)]
    else:
        rows = [row_to_dict(r) for r in biz.list_inventory()]

    # subset by graded status
    if is_graded is not None:
        rows = [r for r in rows if int(r.get("is_graded", 0)) == int(is_graded)]

    return rows


@app.get("/inventory/{item_id}")
def get_inventory_item(item_id: int):
    r = biz.get_inventory_item(item_id)
    if not r:
        raise HTTPException(404, "Inventory item not found")
    return row_to_dict(r)


@app.get("/sets/{set_id}/inventory")
def get_inventory_by_set(set_id: int, is_graded: Optional[int] = None):
    rows = [row_to_dict(r) for r in biz.list_inventory_by_set(set_id)]
    if is_graded is not None:
        rows = [r for r in rows if int(r.get("is_graded", 0)) == int(is_graded)]
    return rows