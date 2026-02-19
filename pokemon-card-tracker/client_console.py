# client_console.py
import requests
import json

BASE = "http://127.0.0.1:8000"

def pretty(obj):
    print(json.dumps(obj, indent=2))

def demo_inventory_crud():
    print("\n--- INVENTORY CRUD via Service ---")

    # CREATE
    create_payload = {
        "card_id": 4,
        "condition_id": 1,
        "is_foil": False,
        "is_graded": False,
        "graded_company": None,
        "grade": None,
        "quantity": 1,
        "purchase_price": 3.50,
        "purchase_date": "2026-02-18",
        "notes": "Created via API"
    }

    r = requests.post(f"{BASE}/inventory", json=create_payload)

    print("POST /inventory status:", r.status_code)
    print("POST /inventory body:", r.text)

    r.raise_for_status()

    item_id = r.json()["item_id"]
    print("Created item_id =", item_id)

    # GET
    r = requests.get(f"{BASE}/inventory/{item_id}")
    r.raise_for_status()
    print("GET after create:")
    pretty(r.json())

    # UPDATE (PATCH)
    patch_payload = {
        "quantity": 2,
        "notes": "Updated via API"
    }

    r = requests.patch(f"{BASE}/inventory/{item_id}", json=patch_payload)
    r.raise_for_status()
    print("PATCH result:", r.json())

    # GET AGAIN
    r = requests.get(f"{BASE}/inventory/{item_id}")
    r.raise_for_status()
    print("GET after update:")
    pretty(r.json())

    # DELETE
    r = requests.delete(f"{BASE}/inventory/{item_id}")
    r.raise_for_status()
    print("DELETE result:", r.json())

    # GET AFTER DELETE (expect 404)
    r = requests.get(f"{BASE}/inventory/{item_id}")
    print("GET after delete status:", r.status_code)
    print("Response:", r.text)

def main():
    print("Make sure API is running:")
    print("  uvicorn api:app --reload")
    demo_inventory_crud()

if __name__ == "__main__":
    main()
