from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from business import PokemonCardBusiness

app = FastAPI(title="Pokemon Card Tracker API", version="4.0")

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
# Pydantic models
# -----------------------------
class SetCreate(BaseModel):
    set_code: str
    set_name: str
    release_date: str
    era: str


class SetUpdate(BaseModel):
    set_code: Optional[str] = None
    set_name: Optional[str] = None
    release_date: Optional[str] = None
    era: Optional[str] = None


class CardCreate(BaseModel):
    set_id: int
    card_number: str
    card_name: str
    rarity: str
    card_type: str


class CardUpdate(BaseModel):
    set_id: Optional[int] = None
    card_number: Optional[str] = None
    card_name: Optional[str] = None
    rarity: Optional[str] = None
    card_type: Optional[str] = None


class ConditionCreate(BaseModel):
    condition_code: str
    description: str


class ConditionUpdate(BaseModel):
    condition_code: Optional[str] = None
    description: Optional[str] = None


class InventoryCreate(BaseModel):
    card_id: int
    condition_id: int
    is_graded: int = Field(0, description="0 = ungraded, 1 = graded")
    graded_company: Optional[str] = None
    grade: Optional[float] = None
    quantity: int = Field(..., ge=1)
    purchase_price: float = Field(..., ge=0)
    purchase_date: str
    notes: Optional[str] = None


class InventoryUpdate(BaseModel):
    card_id: Optional[int] = None
    condition_id: Optional[int] = None
    is_graded: Optional[int] = None
    graded_company: Optional[str] = None
    grade: Optional[float] = None
    quantity: Optional[int] = Field(None, ge=1)
    purchase_price: Optional[float] = Field(None, ge=0)
    purchase_date: Optional[str] = None
    notes: Optional[str] = None


# -----------------------------
# SETS
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
        raise HTTPException(status_code=404, detail="Set not found")
    return row_to_dict(r)


@app.post("/sets", status_code=201)
def create_set(payload: SetCreate):
    try:
        set_id = biz.create_set(**payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    created = biz.get_set(set_id)
    if created:
        return row_to_dict(created)
    return {"set_id": set_id, "message": "Set created successfully"}


@app.put("/sets/{set_id}")
def update_set(set_id: int, payload: SetUpdate):
    try:
        ok = biz.update_set(set_id, **payload.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not ok:
        raise HTTPException(status_code=404, detail="Set not found")

    updated = biz.get_set(set_id)
    if updated:
        return row_to_dict(updated)
    return {"set_id": set_id, "message": "Set updated successfully"}


@app.delete("/sets/{set_id}")
def delete_set(set_id: int):
    ok = biz.delete_set(set_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Set not found")
    return {"set_id": set_id, "message": "Set deleted successfully"}


# -----------------------------
# CARDS
# -----------------------------
@app.get("/cards")
def get_cards(set_id: Optional[int] = None, rarity: Optional[str] = None):
    if set_id is not None:
        rows = [row_to_dict(r) for r in biz.list_cards_in_set(set_id)]
    else:
        rows = [row_to_dict(r) for r in biz.list_cards()]

    if rarity:
        rr = rarity.lower()
        rows = [r for r in rows if rr in str(r.get("rarity", "")).lower()]

    return rows


@app.get("/cards/{card_id}")
def get_card(card_id: int):
    r = biz.get_card(card_id)
    if not r:
        raise HTTPException(status_code=404, detail="Card not found")
    return row_to_dict(r)


@app.get("/sets/{set_id}/cards")
def get_cards_in_set(set_id: int, rarity: Optional[str] = None):
    rows = [row_to_dict(r) for r in biz.list_cards_in_set(set_id)]
    if rarity:
        rr = rarity.lower()
        rows = [r for r in rows if rr in str(r.get("rarity", "")).lower()]
    return rows


@app.post("/cards", status_code=201)
def create_card(payload: CardCreate):
    try:
        card_id = biz.create_card(**payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    created = biz.get_card(card_id)
    if created:
        return row_to_dict(created)
    return {"card_id": card_id, "message": "Card created successfully"}


@app.put("/cards/{card_id}")
def update_card(card_id: int, payload: CardUpdate):
    try:
        ok = biz.update_card(card_id, **payload.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not ok:
        raise HTTPException(status_code=404, detail="Card not found")

    updated = biz.get_card(card_id)
    if updated:
        return row_to_dict(updated)
    return {"card_id": card_id, "message": "Card updated successfully"}


@app.delete("/cards/{card_id}")
def delete_card(card_id: int):
    ok = biz.delete_card(card_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Card not found")
    return {"card_id": card_id, "message": "Card deleted successfully"}


# -----------------------------
# CONDITIONS
# -----------------------------
@app.get("/conditions")
def get_conditions(query: Optional[str] = None):
    rows = [row_to_dict(r) for r in biz.list_conditions()]
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
    rows = [row_to_dict(r) for r in biz.list_conditions()]
    for r in rows:
        if r is not None and int(r.get("condition_id", -1)) == condition_id:
            return r
    raise HTTPException(status_code=404, detail="Condition not found")


@app.post("/conditions", status_code=201)
def create_condition(payload: ConditionCreate):
    try:
        condition_id = biz.create_condition(**payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"condition_id": condition_id, "message": "Condition created successfully"}


@app.put("/conditions/{condition_id}")
def update_condition(condition_id: int, payload: ConditionUpdate):
    try:
        ok = biz.update_condition(condition_id, **payload.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not ok:
        raise HTTPException(status_code=404, detail="Condition not found")

    return {"condition_id": condition_id, "message": "Condition updated successfully"}


@app.delete("/conditions/{condition_id}")
def delete_condition(condition_id: int):
    ok = biz.delete_condition(condition_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Condition not found")
    return {"condition_id": condition_id, "message": "Condition deleted successfully"}


# -----------------------------
# INVENTORY
# -----------------------------
@app.get("/inventory")
def get_inventory(
    set_id: Optional[int] = None,
    is_graded: Optional[int] = None,
):
    if set_id is not None:
        rows = [row_to_dict(r) for r in biz.list_inventory_by_set(set_id)]
    else:
        rows = [row_to_dict(r) for r in biz.list_inventory()]

    if is_graded is not None:
        rows = [r for r in rows if int(r.get("is_graded", 0)) == int(is_graded)]

    return rows


@app.get("/inventory/{item_id}")
def get_inventory_item(item_id: int):
    r = biz.get_inventory_item(item_id)
    if not r:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return row_to_dict(r)


@app.get("/sets/{set_id}/inventory")
def get_inventory_by_set(set_id: int, is_graded: Optional[int] = None):
    rows = [row_to_dict(r) for r in biz.list_inventory_by_set(set_id)]
    if is_graded is not None:
        rows = [r for r in rows if int(r.get("is_graded", 0)) == int(is_graded)]
    return rows


@app.post("/inventory", status_code=201)
def create_inventory_item(payload: InventoryCreate):
    try:
        item_id = biz.create_inventory_item(**payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    created = biz.get_inventory_item(item_id)
    if created:
        return row_to_dict(created)
    return {"item_id": item_id, "message": "Inventory item created successfully"}


@app.put("/inventory/{item_id}")
def update_inventory_item(item_id: int, payload: InventoryUpdate):
    try:
        ok = biz.update_inventory_item(item_id, **payload.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not ok:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    updated = biz.get_inventory_item(item_id)
    if updated:
        return row_to_dict(updated)
    return {"item_id": item_id, "message": "Inventory item updated successfully"}


@app.delete("/inventory/{item_id}")
def delete_inventory_item(item_id: int):
    ok = biz.delete_inventory_item(item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return {"item_id": item_id, "message": "Inventory item deleted successfully"}