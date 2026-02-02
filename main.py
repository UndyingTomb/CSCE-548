from repositories import SetRepository, CardRepository, InventoryRepository

sets_repo = SetRepository()
cards_repo = CardRepository()
inv_repo = InventoryRepository()

def print_rows(rows):
    if not rows:
        print("(no results)")
        return
    for r in rows:
        print(dict(r))

def menu():
    print("\n=== Pokémon Card Tracker ===")
    print("1) List sets")
    print("2) List cards in a set")
    print("3) List inventory (owned cards) by set")
    print("4) Exit")

def list_sets():
    rows = sets_repo.get_all()
    for r in rows:
        print(f"{r['set_id']:>2} | {r['set_code']:<5} | {r['set_name']:<25} | {r['release_date']} | {r['era']}")

def list_cards_in_set():
    set_id = int(input("Enter set_id: ").strip())
    rows = cards_repo.get_by_set(set_id)
    if not rows:
        print("(no cards found for that set_id)")
        return
    for r in rows:
        print(f"{r['card_id']:>3} | #{r['card_number']:<8} | {r['card_name']:<25} | {r['rarity']:<12} | {r['card_type']}")

def list_inventory():
    print("\nSelect a set to filter your inventory:")
    list_sets()

    raw = input("Enter set_id (or press Enter to show all owned cards): ").strip()

    if raw == "":
        rows = inv_repo.get_all()
    else:
        set_id = int(raw)
        rows = inv_repo.get_by_set(set_id)

    if not rows:
        print("(no owned cards found for that set)")
        return

    for r in rows:
        graded = ""
        if r["is_graded"] == 1:
            graded = f" | {r['graded_company']} {r['grade']}"

        print(
            f"Item {r['item_id']:>2} | {r['set_code']} {r['card_number']:<10} {r['card_name']:<22}"
            f"| {r['rarity']:<11} | {r['condition_code']} | qty={r['quantity']} | paid=${r['purchase_price']:.2f}{graded}"
        )


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
            print("Bye.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
 