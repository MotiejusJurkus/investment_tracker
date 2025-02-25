# investment_tracker
Program to save your investment portfolio and calculate entry positions, returns at set prices, retrieve current ticker prices.
Planned usage: A menu interface to select desired action
1. Keep track of portfolio
2. Check portfolio positions with change in price
3. Calculate cost average of a stock
4. Retrieve ticker current prices

Updates:
1. Added class PortfolioManager and main menu
2. Implemented API
3. Added Portfolio.json, updated calculator
4. Added validation and automatic detection if trying to add stock or crypto. When checking portfolio, now shows price change from entry.
5. Added sell function.
6. Updated all functions to have exit to menu option
7. Added feature to show portfolio change when checking portfolio.
8. Changed API key due to security leak and added .env file to store the key