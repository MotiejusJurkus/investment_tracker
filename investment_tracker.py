from portfolio_manager import PortfolioManager

def main():
    manager = PortfolioManager()

    while True:
        print("\nInvestment Tracker Menu:")
        print("1. Add stock/crypto to portfolio")
        print("2. Sell stock/crypto from portfolio")
        print("3. Check portfolio")
        print("4. Calculate cost average")
        print("5. Check ticker/crypto prices")
        print("6. Exit")

        choice = input("Select an option (1-6): ")

        if choice == "1":
            manager.add_position()
        elif choice == "2":
            manager.sell_position()
        elif choice == "3":
            manager.check_portfolio()
        elif choice == "4":
            manager.calculate_cost_average()
        elif choice == "5":
            manager.check_ticker_price()
        elif choice == "6":
            manager.exit_program()
        else:
            print("Invalid choice. Please select a valid option.\n")

if __name__ == "__main__":
    main()
