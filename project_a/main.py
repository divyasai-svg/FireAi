from project_a.parser.tax_assistant import process_tax_query


def main():
    print("\n===== INCOME TAX CALCULATOR =====")

    query = input("Enter your salary and tax regime: ")

    resident_input = input(
        "Are you a resident of India for tax purposes? (yes/no): "
    ).strip().lower()

    if resident_input not in ("yes", "no"):
        print("Please enter yes or no.")
        return

    result = process_tax_query(
        query,
        is_resident=(resident_input == "yes")
    )

    if result["status"] != "success":
        print("\n" + result["message"])
        return

    print("\n===== TAX CALCULATION =====")

    for key, value in result["tax_result"].items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()