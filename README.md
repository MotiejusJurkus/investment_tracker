# investment_tracker
Program to keep track of your investments, calculate entry positions and portfolio performance, and fetch real-time stock prices.

Installation:
git clone https://github.com/yourusername/investment-tracker.git
cd investment-tracker
pip install requests

Usage - When running the program you will be greeted with a main menu with 6 options:
1. Add a new stock/crypto investment.
2. Sell assets from portfolio.
3. View portfolio with performance calculation.
4. Calculate cost average of your assets.
5. Fetch current stock/crypto prices.
6. Exit

Configuration - The program uses Alpha Vantage for stock prices and a cryptocurrency API. Set your API keys in an .env file. You can get a free API key from https://www.alphavantage.co/support/#api-key.


Updates:
1. Added class PortfolioManager and main menu
2. Implemented API
3. Added Portfolio.json, updated calculator
4. Added validation and automatic detection if trying to add stock or crypto. When checking portfolio, now shows price change from entry.
5. Added sell function.
6. Updated all functions to have exit to menu option
7. Added feature to show portfolio change when checking portfolio.
8. Changed API key due to security leak and added .env file to store the key
9. Optimized file handling, redundant API calls, improved error handling.
10. Split Class to sepereate file from main. Added unittests.