import json
import os
from datetime import datetime

FILE_NAME = "expenses.json"


def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read saved data. Starting with an empty list.")
        return []


def save_expenses(expenses):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=4)
        return True
    except OSError:
        print("Error: Could not save expense data.")
        return False


def get_amount():
    while True:
        try:
            amount = float(input("Enter amount (₹): "))

            if amount > 0:
                return amount

            print("Amount must be greater than 0.")

        except ValueError:
            print("Please enter a valid number.")


def get_date():
    while True:
        date = input("Enter date (DD-MM-YYYY): ").strip()

        try:
            datetime.strptime(date, "%d-%m-%Y")
            return date

        except ValueError:
            print("Invalid date. Example: 17-09-2026")


def add_expense(expenses):
    print("\n--- ADD EXPENSE ---")

    expense = {
        "date": get_date(),
        "category": input(
            "Enter category (Food/Travel/Books/Shopping/Other): "
        ).strip().title(),
        "description": input("Enter description: ").strip(),
        "amount": get_amount()
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("Done! Expense added successfully.")


def view_expenses(expenses):
    print("\n--- ALL EXPENSES ---")

    if not expenses:
        print("No expenses added yet.")
        return

    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index}. {expense['date']} | "
            f"{expense['category']} | "
            f"{expense['description']} | "
            f"₹{expense['amount']:.2f}"
        )


def view_total(expenses):
    total = sum(expense["amount"] for expense in expenses)

    print(f"\nTotal Spending: ₹{total:.2f}")


def category_summary(expenses):
    print("\n--- CATEGORY SUMMARY ---")

    if not expenses:
        print("No expenses added yet.")
        return

    summary = {}

    for expense in expenses:
        category = expense["category"]
        summary[category] = summary.get(category, 0) + expense["amount"]

    for category, amount in sorted(summary.items()):
        print(f"{category}: ₹{amount:.2f}")


def delete_expense(expenses):
    print("\n--- DELETE EXPENSE ---")

    if not expenses:
        print("No expenses to delete.")
        return

    view_expenses(expenses)

    try:
        number = int(input("Enter expense number to delete: "))

        if 1 <= number <= len(expenses):
            removed = expenses.pop(number - 1)
            save_expenses(expenses)

            print(
                f"Deleted: {removed['description']} "
                f"(₹{removed['amount']:.2f})"
            )
        else:
            print("Invalid expense number.")

    except ValueError:
        print("Please enter a valid number.")


def search_expenses(expenses):
    print("\n--- SEARCH EXPENSES ---")

    keyword = input(
        "Enter category or description to search: "
    ).strip().lower()

    results = [
        expense for expense in expenses
        if keyword in expense["category"].lower()
        or keyword in expense["description"].lower()
    ]

    if not results:
        print("No matching expenses found.")
        return

    for index, expense in enumerate(results, start=1):
        print(
            f"{index}. {expense['date']} | "
            f"{expense['category']} | "
            f"{expense['description']} | "
            f"₹{expense['amount']:.2f}"
        )


def main():
    expenses = load_expenses()

    print("=" * 45)
    print("      WELCOME TO EXPENSE TRACKER")
    print("        Kharcha kam kiya karo 😭")
    print("=" * 45)

    while True:
        print("\n========== MENU ==========")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Total Spending")
        print("4. Category-wise Summary")
        print("5. Search Expense")
        print("6. Delete Expense")
        print("7. Exit")

        choice = input("Please enter your choice: ").strip()

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            view_total(expenses)

        elif choice == "4":
            category_summary(expenses)

        elif choice == "5":
            search_expenses(expenses)

        elif choice == "6":
            delete_expense(expenses)

        elif choice == "7":
            print("Thanks for using Expense Tracker! 👋")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()