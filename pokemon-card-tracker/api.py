# api.py
"""
Pokemon Card Tracker API
=========================

This file implements the SERVICE LAYER of the application using FastAPI.
It exposes all business-layer methods over HTTP endpoints.

--------------------------------------------------
HOW TO RUN LOCALLY (Ubuntu)
--------------------------------------------------

1) Navigate to project root folder:
    cd path/to/project

2) Create virtual environment:
    python3 -m venv .venv

3) Activate virtual environment:
    source .venv/bin/activate

4) Install dependencies:
    pip install -r requirements.txt

5) Start the service:
    uvicorn api:app --reload

6) Open browser:
    http://127.0.0.1:8000/docs

--------------------------------------------------
HOW TO HOST (Production Example - Render.com)
--------------------------------------------------

1) Push repository to GitHub.
2) Create new Web Service on Render.
3) Connect GitHub repository.
4) Set build command:
       pip install -r requirements.txt
5) Set start command:
       uvicorn api:app --host 0.0.0.0 --port $PORT
6) Deploy.

--------------------------------------------------
HOW TO HOST USING DOCKER
--------------------------------------------------

Create a Dockerfile with:

    FROM python:3.12
    WORKDIR /app
    COPY . .
    RUN pip install -r requirements.txt
    CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

Then run:
    docker build -t pokemon-api .
    docker run -p 8000:8000 pokemon-api

--------------------------------------------------
ARCHITECTURE
--------------------------------------------------

Console Client
    ↓
Service Layer (FastAPI)  ← this file
    ↓
Business Layer (business.py)
    ↓
Repository Layer (repositories.py)
    ↓
SQLite Database

This design models a professional layered architecture.
"""


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Any, Dict

from business import PokemonCardBusiness

app = FastAPI(title="Pokemon Card Tracker API", version="2.0")
biz = PokemonCardBusiness()

def row_to_dict(r):
    return dict(r) if r is not None else None


# ---------- Models ----------
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
    is_foil: int = 0
    is_graded: int = 0
    graded_company: Optional[str] = None
    grade: Optional[float] = None
    quantity: int = 1
    purchase_price: float = 0.0
    purchase_date: Optional[str] = None
    notes: Optional[str] = None

class InventoryUpdate(BaseModel):
    card_id: Optional[int] = None
    condition_id: Optional[int] = None
    is_foil: Optional[int] = None
    is_graded: Optional[int] = None
    graded_company: Optional[str] = None
    grade: Optional[float] = None
    quantity: Optional[int] = None
    purchase_price: Optional[float] = None
    purchase_date: Optional[str] = None
    notes: Optional[str] = None


# ---------- Sets ----------
@app.get("/sets")
def list_sets():
    return [row_to_dict(r) for r in biz.list_sets()]

@app.get("/sets/{set_id}")
def get_set(set_id: int):
    r = biz.get_set(set_id)
    if not r:
        raise HTTPException(404, "Set not found")
    return row_to_dict(r)

@app.post("/sets")
def create_set(payload: SetCreate):
    try:
        new_id = biz.create_set(**payload.model_dump())
        return {"set_id": new_id}
    except Exception as e:
        raise HTTPException(400, str(e))

@app.patch("/sets/{set_id}")
def update_set(set_id: int, payload: SetUpdate):
    fields = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not fields:
        return {"updated": False, "reason": "no fields"}
    ok = biz.update_set(set_id, **fields)
    if not ok:
        raise HTTPException(404, "Set not found")
    return {"updated": True}

@app.delete("/sets/{set_id}")
def delete_set(set_id: int):
    ok = biz.delete_set(set_id)
    if not ok:
        raise HTTPException(404, "Set not found")
    return {"deleted": True}


# ---------- Cards ----------
@app.get("/cards")
def list_cards():
    return [row_to_dict(r) for r in biz.list_cards()]

@app.get("/cards/{card_id}")
def get_card(card_id: int):
    r = biz.get_card(card_id)
    if not r:
        raise HTTPException(404, "Card not found")
    return row_to_dict(r)

@app.get("/sets/{set_id}/cards")
def list_cards_in_set(set_id: int):
    return [row_to_dict(r) for r in biz.list_cards_in_set(set_id)]

@app.post("/cards")
def create_card(payload: CardCreate):
    try:
        new_id = biz.create_card(**payload.model_dump())
        return {"card_id": new_id}
    except Exception as e:
        raise HTTPException(400, str(e))

@app.patch("/cards/{card_id}")
def update_card(card_id: int, payload: CardUpdate):
    fields = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not fields:
        return {"updated": False, "reason": "no fields"}
    ok = biz.update_card(card_id, **fields)
    if not ok:
        raise HTTPException(404, "Card not found")
    return {"updated": True}

@app.delete("/cards/{card_id}")
def delete_card(card_id: int):
    ok = biz.delete_card(card_id)
    if not ok:
        raise HTTPException(404, "Card not found")
    return {"deleted": True}


# ---------- Conditions ----------
@app.get("/conditions")
def list_conditions():
    return [row_to_dict(r) for r in biz.list_conditions()]

@app.post("/conditions")
def create_condition(payload: ConditionCreate):
    try:
        new_id = biz.create_condition(**payload.model_dump())
        return {"condition_id": new_id}
    except Exception as e:
        raise HTTPException(400, str(e))

@app.patch("/conditions/{condition_id}")
def update_condition(condition_id: int, payload: ConditionUpdate):
    fields = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not fields:
        return {"updated": False, "reason": "no fields"}
    ok = biz.update_condition(condition_id, **fields)
    if not ok:
        raise HTTPException(404, "Condition not found")
    return {"updated": True}

@app.delete("/conditions/{condition_id}")
def delete_condition(condition_id: int):
    ok = biz.delete_condition(condition_id)
    if not ok:
        raise HTTPException(404, "Condition not found")
    return {"deleted": True}


# ---------- Inventory ----------
@app.get("/inventory")
def list_inventory():
    return [row_to_dict(r) for r in biz.list_inventory()]

@app.get("/inventory/{item_id}")
def get_inventory_item(item_id: int):
    r = biz.get_inventory_item(item_id)
    if not r:
        raise HTTPException(404, "Inventory item not found")
    return row_to_dict(r)

@app.get("/sets/{set_id}/inventory")
def list_inventory_by_set(set_id: int):
    return [row_to_dict(r) for r in biz.list_inventory_by_set(set_id)]

@app.post("/inventory")
def create_inventory(payload: InventoryCreate):
    try:
        new_id = biz.create_inventory_item(**payload.model_dump())
        return {"item_id": new_id}
    except Exception as e:
        raise HTTPException(400, str(e))

@app.patch("/inventory/{item_id}")
def update_inventory(item_id: int, payload: InventoryUpdate):
    fields = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not fields:
        return {"ok": True, "updated": False, "reason": "no fields"}

    try:
        ok = biz.update_inventory_item(item_id, **fields)
    except Exception as e:
        raise HTTPException(400, str(e))

    if not ok:
        raise HTTPException(404, "Inventory item not found")
    return {"ok": True}


@app.delete("/inventory/{item_id}")
def delete_inventory(item_id: int):
    ok = biz.delete_inventory_item(item_id)
    if not ok:
        raise HTTPException(404, "Inventory item not found")
    return {"ok": True}
