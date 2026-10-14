"""A small command-line expense tracker for a beginner portfolio project."""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path


DATA_FILE = Path(__file__).with_name("expenses.json")


def load_expenses() -> list[dict[str, str | float]]:
    """Load saved expenses, returning an empty list when there is no data yet."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            expenses = json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Не удалось прочитать файл расходов. Начинаю с пустого списка.")
        return []

    if not isinstance(expenses, list):
        print("Файл расходов имеет неверный формат. Начинаю с пустого списка.")
        return []
    return expenses


def save_expenses(expenses: list[dict[str, str | float]]) -> None:
    """Save expenses as readable UTF-8 JSON."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(expenses, file, ensure_ascii=False, indent=2)


def ask_amount() -> float:
    """Ask for a positive amount and accept either comma or dot decimals."""
    while True:
        raw_amount = input("Сумма: ").strip().replace(",", ".")
        try:
            amount = float(raw_amount)
        except ValueError:
            print("Введите число, например 250 или 99.50.")
            continue

        if amount <= 0:
            print("Сумма должна быть больше нуля.")
            continue
        return round(amount, 2)


def add_expense(expenses: list[dict[str, str | float]]) -> None:
    """Collect and save one expense."""
    category = input("Категория (например, еда, транспорт): ").strip()
    while not category:
        print("Категория не должна быть пустой.")
        category = input("Категория: ").strip()

    note = input("Комментарий (можно оставить пустым): ").strip()
    amount = ask_amount()

    expense = {
        "date": date.today().isoformat(),
        "category": category,
        "amount": amount,
        "note": note,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print("Расход сохранён.")


def list_expenses(expenses: list[dict[str, str | float]]) -> None:
    """Print all expenses in date order."""
    if not expenses:
        print("Расходов пока нет.")
        return

    print("\nДата       | Категория          | Сумма      | Комментарий")
    print("-" * 72)
    for expense in sorted(expenses, key=lambda item: str(item.get("date", ""))):
        print(
            f"{str(expense.get('date', '')):10} | "
            f"{str(expense.get('category', ''))[:18]:18} | "
            f"{float(expense.get('amount', 0)) :>10.2f} | "
            f"{expense.get('note', '')}"
        )


def show_summary(expenses: list[dict[str, str | float]]) -> None:
    """Show the current month's total and totals grouped by category."""
    current_month = date.today().strftime("%Y-%m")
    monthly_expenses = [
        expense
        for expense in expenses
        if str(expense.get("date", "")).startswith(current_month)
    ]

    if not monthly_expenses:
        print("В этом месяце расходов пока нет.")
        return

    totals: dict[str, float] = {}
    for expense in monthly_expenses:
        category = str(expense.get("category", "Без категории"))
        totals[category] = totals.get(category, 0.0) + float(expense.get("amount", 0))

    total = sum(totals.values())
    print(f"\nИтого за {datetime.now():%m.%Y}: {total:.2f}")
    print("По категориям:")
    for category, amount in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        print(f"  {category}: {amount:.2f}")


def main() -> None:
    expenses = load_expenses()
    actions = {
        "1": ("Добавить расход", lambda: add_expense(expenses)),
        "2": ("Показать все расходы", lambda: list_expenses(expenses)),
        "3": ("Сводка за текущий месяц", lambda: show_summary(expenses)),
    }

    while True:
        print("\n=== Трекер расходов ===")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()
        if choice == "0":
            print("До встречи!")
            break
        if choice in actions:
            actions[choice][1]()
        else:
            print("Такого пункта нет. Выберите 0, 1, 2 или 3.")


if __name__ == "__main__":
    main()
