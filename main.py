from expense_calc import calculator


def show_menu():
    print()
    print("=== Expense Calculator ===")
    print("1. Add expense")
    print("2. Show total")
    print("3. Show total by category")
    print("4. Show total with discounts/taxes")
    print("5. List all expenses")
    print("0. Exit")

 
def main():
    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            try:
                amount = float(input("Amount: "))
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue
            category = input("Category (food/health/entertainment/transport/other): ")
            description = input("Description: ")
            try:
                calculator.add_expense(amount, category, description)
                print("Expense added.")
            except ValueError as error:
                print("Error:", error)
        elif choice == "2":
            print("Total:", calculator.get_total())
        elif choice == "3":
            category = input("Category: ")
            print("Total for", category, ":", calculator.get_total_by_category(category))
        elif choice == "4":
            print("Total with rules:", calculator.get_total_with_rules())
        elif choice == "5":
            for e in calculator.expenses:
                print(e["category"], "-", e["description"], "-", e["amount"])
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Unknown option.")


if __name__ == "__main__":
    main()
