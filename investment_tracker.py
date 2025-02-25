import sys
import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()

class PortfolioManager:
    API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    STOCK_API_URL = "https://www.alphavantage.co/query"
    PORTFOLIO_FILE = "portfolio.json"

    def __init__(self):
        self.portfolio = self.load_portfolio()
        if not self.API_KEY:
            raise ValueError("API Key not found. Make sure it's set in the .env file.")

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

        return None, None
    
    @staticmethod
    def prompt_input(prompt_text):

        user_input = input(prompt_text).strip()
        if user_input.lower() in ["exit", "q"]:
            print("Returning to main menu...\n")
            return None
        return user_input

    def add_position(self):
        ticker = self.prompt_input("Enter stock/crypto ticker (or 'exit' to return): ")
        if ticker is None:
            return
        
        ticker = ticker.upper()
        asset_type, current_price = self.validate_ticker(ticker)
        if asset_type is None:
            print("Invalid ticker. Please enter a valid stock or crypto symbol.\n")
            return

        amount_input = self.prompt_input(f"Enter amount of {'shares' if asset_type == 'stock' else 'coins'} (or 'exit' to return): ")
        if amount_input is None:
            return
        try:
            amount = float(amount_input)
        except ValueError:
            print("Invalid input. Please enter a numeric value.\n")
            return

        entry_input = self.prompt_input("Enter entry price (or 'exit' to return): ")
        if entry_input is None:
            return
        try:
            entry_price = float(entry_input)
        except ValueError:
            print("Invalid input. Please enter a numeric value.\n")
            return

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

    def sell_position(self):
        ticker = self.prompt_input("Enter the ticker of the asset to sell (or 'exit' to return): ")
        if ticker is None:
            return

        ticker = ticker.upper()
        if ticker not in self.portfolio:
            print("Ticker not found in portfolio.\n")
            return

        amount_input = self.prompt_input(f"Enter amount of {'shares' if self.portfolio[ticker]['asset_type'] == 'stock' else 'coins'} to sell (or 'exit' to return): ")
        if amount_input is None:
            return
        try:
            amount_to_sell = float(amount_input)
        except ValueError:
            print("Invalid input. Please enter a numeric value.\n")
            return

        if amount_to_sell > self.portfolio[ticker]["amount"]:
            print("You don't have enough to sell that amount.\n")
            return

        self.portfolio[ticker]["amount"] -= amount_to_sell
        if self.portfolio[ticker]["amount"] == 0:
            del self.portfolio[ticker]

        print(f"Sold {amount_to_sell} of {ticker}.\n")
        self.save_portfolio()

    def check_portfolio(self):
        if not self.portfolio:
            print("Your portfolio is empty.\n")
            return
        
        total_invested = 0
        total_value = 0
        
        print("\nCurrent Portfolio:")
        for ticker, details in self.portfolio.items():
            asset_type = details["asset_type"]
            unit = "shares" if asset_type == "stock" else "coins"
            current_price = self.get_stock_price(ticker) or self.get_crypto_price(ticker)
            
            if current_price:
                entry_price = details["entry_price"]
                amount = details["amount"]
                
                total_cost = entry_price * amount
                current_value = current_price * amount
                
                total_invested += total_cost
                total_value += current_value

                change_percent = ((current_price - entry_price) / entry_price) * 100
                print(f"{ticker}: {amount} {unit} at ${entry_price:.2f}, {change_percent:+.2f}%")
            else:
                print(f"{ticker}: {details['amount']} {unit} at ${details['entry_price']:.2f}, price unavailable")

        if total_invested > 0:
            portfolio_change_percent = ((total_value - total_invested) / total_invested) * 100
            print(f"\nTotal Portfolio Performance: {portfolio_change_percent:+.2f}%\n")
        else:
            print("\nTotal Portfolio Performance: N/A (no valid price data)\n")

    def check_ticker_price(self):
        ticker = self.prompt_input("Enter the ticker symbol (or 'exit' to return): ")
        if ticker is None:
            return

        ticker = ticker.upper()
        asset_type, price = self.validate_ticker(ticker)
        if asset_type:
            print(f"Current price of {ticker}: ${price:.2f}\n")
        else:
            print(f"Failed to retrieve price for {ticker}. Please check the symbol.\n")

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
        ticker = self.prompt_input("Enter ticker to calculate cost average (or 'exit' to return): ")
        if ticker is None:
            return

        ticker = ticker.upper()
        asset_type, current_price = self.validate_ticker(ticker)
        if asset_type is None:
            print("Invalid ticker. Please enter a valid stock or crypto symbol.\n")
            return

        percent_input = self.prompt_input("Enter percentage change (e.g., 7.5 for +7.5%, -3.2 for -3.2%) (or 'exit' to return): ")
        if percent_input is None:
            return
        try:
            percent_change = float(percent_input)
        except ValueError:
            print("Invalid input. Please enter a numeric value.\n")
            return

        entry_price = current_price / (1 + (percent_change / 100))
        print(f"\nYour estimated cost average for {ticker} is: ${entry_price:.2f} per share/coin.\n")

    def exit_program(self):
        self.save_portfolio()
        sys.exit()

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
