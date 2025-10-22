import requests
import time
import pandas as pd
from datetime import datetime
import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.config import POLYMARKET_API_KEY, POLYMARKET_BASE_URL, REQUEST_DELAY

class PolymarketClient:
    """Client for interacting with the Polymarket API"""
    
    def __init__(self):
        self.base_url = POLYMARKET_BASE_URL
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {POLYMARKET_API_KEY}"
        }
    
    def _make_request(self, endpoint, method="GET", params=None, data=None):
        """Make a request to the Polymarket API with rate limiting"""
        url = f"{self.base_url}{endpoint}"
        
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            params=params,
            json=data
        )
        
        # Respect rate limits
        time.sleep(REQUEST_DELAY)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code} for {url}: {response.text}")
            return None
    
    def get_markets(self):
        """Get all available markets"""
        return self._make_request("/markets")
    
    def get_market_details(self, market_id):
        """Get detailed information for a specific market"""
        return self._make_request(f"/markets/{market_id}")
    
    def get_order_book(self, market_id):
        """Get order book for a specific market"""
        return self._make_request(f"/markets/{market_id}/orderbook")
    
    def get_price_history(self, market_id, interval="1h"):
        """Get price history for a market"""
        return self._make_request(f"/markets/{market_id}/prices", params={"interval": interval})

# Usage example
if __name__ == "__main__":
    client = PolymarketClient()
    markets = client.get_markets()
    print(f"Found {len(markets)} markets")