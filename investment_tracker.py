import sys
import requests

class PortfolioManager:
    API_KEY = "BSWVS0SUEAX7QSJX" 
    STOCK_API_URL = "https://www.alphavantage.co/query"

    def check_ticker_price(self):
        """Prompt user for stock or crypto, then fetch price from Alpha Vantage API."""
        asset_type = input("Do you want to check a stock or cryptocurrency? (stock/crypto): ").strip().lower()

        if asset_type not in ["stock", "crypto"]:
            print("Invalid input. Please enter 'stock' or 'crypto'.\n")
            return

        ticker = input("Enter the ticker symbol (e.g., AAPL for stocks, BTC for crypto): ").upper()
        
        if asset_type == "crypto":
            price = self.get_crypto_price(ticker)
        else:
            price = self.get_stock_price(ticker)

        if price:
            print(f"Current price of {ticker}: ${price:.2f}\n")
        else:
            print(f"Failed to retrieve price for {ticker}. Please check the symbol and try again.\n")


    def get_stock_price(self, ticker):
        """Fetch stock price from Alpha Vantage API."""
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": self.API_KEY
        }
        response = requests.get(self.STOCK_API_URL, params=params)
        data = response.json()
        
        try:
            return float(data["Global Quote"]["05. price"])
        except KeyError:
            return None

    def get_crypto_price(self, ticker):
        """Fetch cryptocurrency price from Alpha Vantage API."""
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": ticker,
            "to_currency": "USD",
            "apikey": self.API_KEY
        }
        response = requests.get(self.STOCK_API_URL, params=params)
        data = response.json()
        
        try:
            return float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
        except KeyError:
            return None

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
