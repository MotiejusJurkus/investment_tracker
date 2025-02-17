import sys

class PortfolioManager:
    def __init__(self):
        self.portfolio = {}

    def add_position(self):
        """Add a stock/crypto to portfolio with entry price and amount."""
        ticker = input("Enter stock/crypto ticker (e.g., AAPL, BTC): ").upper()
        try:
            shares = float(input("Enter amount of shares/coins: "))
            entry_price = float(input("Enter entry price: $"))
            self.portfolio[ticker] = {"shares": shares, "entry_price": entry_price}
            print(f"{ticker} added to portfolio.\n")
        except ValueError:
            print("Invalid input. Please enter numeric values.\n")

    def check_portfolio(self):
        """Display all positions in the portfolio."""
        if not self.portfolio:
            print("Your portfolio is empty.\n")
            return
        
        print("\nCurrent Portfolio:")
        for ticker, details in self.portfolio.items():
            print(f"{ticker}: {details['shares']} shares at ${details['entry_price']} entry price")
        print()

    def calculate_cost_average(self):
        """Calculate cost average based on percentage change."""
        try:
            ticker = input("Enter ticker to calculate cost average: ").upper()
            if ticker not in self.portfolio:
                print(f"{ticker} not found in portfolio.\n")
                return
            
            shares = float(input("Enter number of shares/coins: "))
            percent_change = float(input("Enter percentage change (positive or negative): "))

            old_price = self.portfolio[ticker]["entry_price"]
            new_price = old_price * (1 + percent_change / 100)
            print(f"New estimated price for {ticker}: ${new_price:.2f}\n")

        except ValueError:
            print("Invalid input. Please enter numeric values.\n")

    def check_ticker_price(self):
        """Price retrieval with API"""
        ticker = input("Enter stock/crypto ticker to check price: ").upper()
        print(f"Fetching live price for {ticker}... (API integration needed)\n")

    def exit_program(self):
        """Exit the program."""
        sys.exit()

def main():
    manager = PortfolioManager()

    while True:
        print("\nInvestment Tracker Menu:")
        print("1. Add stock/crypto to portfolio")
        print("2. Check portfolio")
        print("3. Calculate cost average")
        print("4. Check ticker/crypto prices")
        print("5. Exit")

        choice = input("Select an option (1-5): ")

        if choice == "1":
            manager.add_position()
        elif choice == "2":
            manager.check_portfolio()
        elif choice == "3":
            manager.calculate_cost_average()
        elif choice == "4":
            manager.check_ticker_price()
        elif choice == "5":
            manager.exit_program()
        else:
            print("Invalid choice. Please select a valid option.\n")

if __name__ == "__main__":
    main()
