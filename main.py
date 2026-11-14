import json
from pathlib import Path

FILE = Path("expenses.json")
CATEGORIES = ["food", "transport", "bills", "shopping", "other"]


def load():
    if FILE.exists():
        return json.loads(FILE.read_text())
    return []


def save(expenses):
    FILE.write_text(json.dumps(expenses, indent=2))


def choose_category():
    print("Categories:")
    for i, c in enumerate(CATEGORIES, 1):
        print(f"{i}. {c}")
    try:
        index = int(input("Pick a category number: ")) - 1
        return CATEGORIES[index]
    except (ValueError, IndexError):
        print("Invalid choice, using 'other'.")
        return "other"


def add_expense(expenses):
    name = input("Description: ").strip()
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    category = choose_category()
    expenses.append({"name": name, "amount": amount, "category": category})
    save(expenses)
    print("Saved.")


def show_expenses(expenses):
    if not expenses:
        print("No expenses yet.")
        return
    for i, e in enumerate(expenses, 1):
        category = e.get("category", "other")
        print(f"{i}. {e['name']} [{category}]: {e['amount']:.2f}")
    total = sum(e["amount"] for e in expenses)
    print(f"Total: {total:.2f}")


def delete_expense(expenses):
    show_expenses(expenses)
    if not expenses:
        return
    try:
        index = int(input("Number to delete: ")) - 1
        removed = expenses.pop(index)
    except (ValueError, IndexError):
        print("Invalid number.")
        return
    save(expenses)
    print(f"Deleted: {removed['name']}")


def show_summary(expenses):
    if not expenses:
        print("No expenses yet.")
        return
    totals = {}
    for e in expenses:
        category = e.get("category", "other")
        totals[category] = totals.get(category, 0) + e["amount"]
    grand_total = sum(totals.values())
    print("\nSpending by category:")
    for category, amount in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        percent = amount / grand_total * 100
        print(f"{category}: {amount:.2f} ({percent:.1f}%)")
    print(f"Total: {grand_total:.2f}")


def main():
    expenses = load()
    while True:
        print("\n1) Add  2) View  3) Delete  4) Summary  5) Quit")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            delete_expense(expenses)
        elif choice == "4":
            show_summary(expenses)
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
