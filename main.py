import json
from pathlib import Path

FILE = Path("expenses.json")


def load():
    if FILE.exists():
        return json.loads(FILE.read_text())
    return []


def save(expenses):
    FILE.write_text(json.dumps(expenses, indent=2))


def add_expense(expenses):
    name = input("Description: ").strip()
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    expenses.append({"name": name, "amount": amount})
    save(expenses)
    print("Saved.")


def show_expenses(expenses):
    if not expenses:
        print("No expenses yet.")
        return
    for i, e in enumerate(expenses, 1):
        print(f"{i}. {e['name']}: {e['amount']:.2f}")
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


def main():
    expenses = load()
    while True:
        print("\n1) Add  2) View  3) Delete  4) Quit")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            delete_expense(expenses)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
