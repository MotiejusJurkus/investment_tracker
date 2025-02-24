import sys
import requests
import json
import os

class PortfolioManager:
    API_KEY = "BSWVS0SUEAX7QSJX" 
    STOCK_API_URL = "https://www.alphavantage.co/query"
    PORTFOLIO_FILE = "portfolio.json"

    def __init__(self):
        self.portfolio = self.load_portfolio()

    def load_portfolio(self):
        if os.path.exists(self.PORTFOLIO_FILE):
            try:
                with open(self.PORTFOLIO_FILE, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Error loading portfolio.\n")
                return {}
        return {}

    def save_portfolio(self):
        with open(self.PORTFOLIO_FILE, "w") as file:
            json.dump(self.portfolio, file, indent=4)

    def validate_ticker(self, ticker):
        stock_price = self.get_stock_price(ticker)
        crypto_price = self.get_crypto_price(ticker)

        if stock_price and crypto_price:
            choice = input(f"The ticker '{ticker}' exists as both a stock and a cryptocurrency. Is this a stock or a crypto? (stock/crypto): ").strip().lower()
            if choice == "stock":
                return "stock", stock_price
            elif choice == "crypto":
                return "crypto", crypto_price
            else:
                print("Invalid selection.")
                return None, None

        if stock_price:
            return "stock", stock_price
        if crypto_price:
            return "crypto", crypto_price

        return None, None  # Invalid ticker

    def add_position(self):
        ticker = input("Enter stock/crypto ticker (e.g., AAPL, BTC): ").upper()
        asset_type, current_price = self.validate_ticker(ticker)

        if asset_type is None:
            print("Invalid ticker. Please enter a valid stock or crypto symbol.\n")
            return

        try:
            amount = float(input(f"Enter amount of {'shares' if asset_type == 'stock' else 'coins'}: "))
            entry_price = float(input("Enter entry price: $"))

            if ticker in self.portfolio:
                old_amount = self.portfolio[ticker]["amount"]
                old_price = self.portfolio[ticker]["entry_price"]
                
                total_cost = (old_amount * old_price) + (amount * entry_price)
                total_amount = old_amount + amount
                new_entry_price = total_cost / total_amount

                self.portfolio[ticker] = {
                    "amount": total_amount,
                    "entry_price": new_entry_price,
                    "asset_type": asset_type
                }
            else:
                self.portfolio[ticker] = {
                    "amount": amount,
                    "entry_price": entry_price,
                    "asset_type": asset_type
                }

            print(f"{ticker} added to portfolio.\n")
            self.save_portfolio()
        except ValueError:
            print("Invalid input. Please enter numeric values.\n")

    def check_portfolio(self):
        if not self.portfolio:
            print("Your portfolio is empty.\n")
            return
        
        print("\nCurrent Portfolio:")
        for ticker, details in self.portfolio.items():
            asset_type = details["asset_type"]
            unit = "shares" if asset_type == "stock" else "coins"
            current_price = self.get_stock_price(ticker) or self.get_crypto_price(ticker)
            
            if current_price:
                change_percent = ((current_price - details["entry_price"]) / details["entry_price"]) * 100
                print(f"{ticker}: {details['amount']} {unit} at ${details['entry_price']:.2f}, {change_percent:+.2f}%")
            else:
                print(f"{ticker}: {details['amount']} {unit} at ${details['entry_price']:.2f}, price unavailable")
        print()

    def check_ticker_price(self):
         ticker = input("Enter the ticker symbol (e.g., AAPL for stocks, BTC for crypto): ").upper()
         asset_type, price = self.validate_ticker(ticker)

         if asset_type is None:
             print("Invalid ticker. Please enter a valid stock or crypto symbol.\n")
             return

         print(f"Current price of {ticker} ({asset_type}): ${price:.2f}\n")

    def get_stock_price(self, ticker):
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": self.API_KEY
        }
        try:
            response = requests.get(self.STOCK_API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "Global Quote" in data and "05. price" in data["Global Quote"]:
                return float(data["Global Quote"]["05. price"])
            else:
                return None
        except requests.RequestException as e:
            print(f"Error fetching stock data: {e}")
            return None

    def get_crypto_price(self, ticker):
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": ticker,
            "to_currency": "USD",
            "apikey": self.API_KEY
        }
        try:
            response = requests.get(self.STOCK_API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "Realtime Currency Exchange Rate" in data and "5. Exchange Rate" in data["Realtime Currency Exchange Rate"]:
                return float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
            
            return None
        except requests.RequestException as e:
            print(f"Error fetching crypto data: {e}")
            return None


    def calculate_cost_average(self):
        try:
            ticker = input("Enter ticker to calculate cost average: ").upper()
            asset_type = input("Is this a stock or cryptocurrency? (stock/crypto): ").strip().lower()

            if asset_type == "crypto":
                current_price = self.get_crypto_price(ticker)
            elif asset_type == "stock":
                current_price = self.get_stock_price(ticker)
            else:
                print("Invalid asset type. Please enter 'stock' or 'crypto'.\n")
                return

            if current_price is None:
                print(f"Could not retrieve price for {ticker}. Please check the symbol.\n")
                return
            
            percent_change = float(input("Enter percentage change (e.g., 7.5 for +7.5%, -3.2 for -3.2%): "))

            entry_price = current_price / (1 + (percent_change / 100))

            print(f"\nYour estimated cost average for {ticker} is: ${entry_price:.2f} per share/coin.\n")

        except ValueError:
            print("Invalid input. Please enter numeric values.\n")

    def exit_program(self):
        self.save_portfolio()
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
