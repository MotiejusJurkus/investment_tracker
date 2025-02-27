import unittest
from unittest.mock import patch, mock_open
import json
from portfolio_manager import PortfolioManager

class TestPortfolioManager(unittest.TestCase):

    @patch.dict("os.environ", {"ALPHA_VANTAGE_API_KEY": "test_api_key"})
    def setUp(self):
        self.mock_portfolio = {
            "AAPL": {"amount": 10, "entry_price": 150.0, "asset_type": "stock"},
            "BTC": {"amount": 0.5, "entry_price": 40000.0, "asset_type": "crypto"}
        }
        self.manager = PortfolioManager()
        self.manager.portfolio = self.mock_portfolio.copy()

    def tearDown(self):
        self.manager.portfolio = {}

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({}))
    @patch("json.load", return_value={})
    def test_load_portfolio(self, mock_json_load, mock_file):
        manager = PortfolioManager()
        mock_file.assert_called() 

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_portfolio(self, mock_json_dump, mock_file):
        manager = PortfolioManager()
        manager.save_portfolio(force=True)
        mock_file.assert_any_call(PortfolioManager.PORTFOLIO_FILE, "w")

    @patch("portfolio_manager.PortfolioManager.get_stock_price", return_value=200.0)
    @patch("builtins.input", side_effect=["MSFT", "5", "180"]) 
    def test_add_position_new_stock(self, mock_input, mock_get_stock_price):
        self.manager.add_position()
        
        self.assertIn("MSFT", self.manager.portfolio)
        self.assertEqual(self.manager.portfolio["MSFT"]["amount"], 5)
        self.assertEqual(self.manager.portfolio["MSFT"]["entry_price"], 180.0)

    @patch("builtins.input", side_effect=["AAPL", "5"])
    def test_sell_position_partial(self, mock_input):
        self.manager.sell_position()
        self.assertEqual(self.manager.portfolio["AAPL"]["amount"], 5)

    @patch("builtins.input", side_effect=["AAPL", "10"]) 
    def test_sell_position_full(self, mock_input):
        self.manager.sell_position()
        self.assertNotIn("AAPL", self.manager.portfolio)

    @patch("portfolio_manager.PortfolioManager.get_stock_price", return_value=250.0)
    def test_check_ticker_price_stock(self, mock_get_stock_price):
        price = self.manager.get_stock_price("AAPL")
        self.assertEqual(price, 250.0)

    @patch("portfolio_manager.PortfolioManager.get_crypto_price", return_value=50000.0)
    def test_check_ticker_price_crypto(self, mock_get_crypto_price):
        price = self.manager.get_crypto_price("BTC")
        self.assertEqual(price, 50000.0)

if __name__ == "__main__":
    unittest.main()
