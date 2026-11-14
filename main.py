import json
from pathlib import Path

FILE = Path("expenses.json")
CATEGORIES = ["food", "transport", "bills", "shopping", "other"]


def load():
    if FILE.exists():
        try:
            return json.loads(FILE.read_text())
        except json.JSONDecodeError:
            print("Data file is corrupted. Starting fresh.")
    return []


def save(expenses):
    FILE.write_text(json.dumps(expenses, indent=2))


def ask_description():
    while True:
        name = input("Description: ").strip()
        if name:
            return name
        print("Description cannot be empty.")


def ask_amount():
    while True:
        try:
            amount = float(input("Amount: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        if amount <= 0:
            print("Amount must be greater than zero.")
            continue
        return amount


def choose_category():
    print("Categories:")
    for i, c in enumerate(CATEGORIES, 1):
        print(f"{i}. {c}")
    try:
        index = int(input("Pick a category number: ")) - 1
        if index < 0:
            raise IndexError
        return CATEGORIES[index]
    except (ValueError, IndexError):
        print("Invalid choice, using 'other'.")
        return "other"


def add_expense(expenses):
    name = ask_description()
    amount = ask_amount()
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
        if index < 0:
            raise IndexError
        removed = expenses.pop(index)
    except (ValueError, IndexError):
        print("Invalid number.")
        return
    save(expenses)
    print(f"Deleted: {removed['name']}")


def edit_expense(expenses):
    show_expenses(expenses)
    if not expenses:
        return
    try:
        index = int(input("Number to edit: ")) - 1
        if index < 0:
            raise IndexError
        expense = expenses[index]
    except (ValueError, IndexError):
        print("Invalid number.")
        return

    print("Press Enter to keep the current value.")

    new_name = input(f"Description [{expense['name']}]: ").strip()
    if new_name:
        expense["name"] = new_name

    while True:
        new_amount = input(f"Amount [{expense['amount']:.2f}]: ").strip()
        if not new_amount:
            break
        try:
            value = float(new_amount)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if value <= 0:
            print("Amount must be greater than zero.")
            continue
        expense["amount"] = value
        break

    change_category = input("Change category? (y/n): ").strip().lower()
    if change_category == "y":
        expense["category"] = choose_category()

    save(expenses)
    print("Updated.")


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
        print("\n1) Add  2) View  3) Edit  4) Delete  5) Summary  6) Quit")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            edit_expense(expenses)
        elif choice == "4":
            delete_expense(expenses)
        elif choice == "5":
            show_summary(expenses)
        elif choice == "6":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
