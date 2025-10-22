import os
import sys
import pandas as pd
from datetime import datetime
import time

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.data.polymarket_client import PolymarketClient
from src.config import RAW_DATA_PATH

def collect_and_save_data():
    """Collect data from Polymarket API and save to files"""
    client = PolymarketClient()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Ensure directories exist
    markets_dir = os.path.join(RAW_DATA_PATH, "markets")
    prices_dir = os.path.join(RAW_DATA_PATH, "prices")
    orderbooks_dir = os.path.join(RAW_DATA_PATH, "orderbooks")
    
    os.makedirs(markets_dir, exist_ok=True)
    os.makedirs(prices_dir, exist_ok=True)
    os.makedirs(orderbooks_dir, exist_ok=True)
    
    # Step 1: Get all markets
    print("Fetching all markets...")
    markets = client.get_markets()
    
    if not markets:
        print("Failed to fetch markets. Exiting.")
        return
    
    # Save markets data
    markets_df = pd.DataFrame(markets)
    markets_file = os.path.join(markets_dir, f"markets_{timestamp}.parquet")
    markets_df.to_parquet(markets_file)
    print(f"Saved {len(markets_df)} markets to {markets_file}")
    
    # Step 2: For each market, get details, price history and order book
    for i, market in enumerate(markets):
        market_id = market.get('id')
        if not market_id:
            continue
            
        print(f"Processing market {i+1}/{len(markets)}: {market_id}")
        
        # Get market details
        details = client.get_market_details(market_id)
        if details:
            details_df = pd.DataFrame([details])
            details_file = os.path.join(markets_dir, f"market_details_{market_id}.parquet")
            details_df.to_parquet(details_file)
        
        # Get price history
        for interval in ['1h', '1d']:
            prices = client.get_price_history(market_id, interval)
            if prices:
                prices_df = pd.DataFrame(prices)
                prices_file = os.path.join(
                    prices_dir, 
                    f"prices_{market_id}_{interval}_{timestamp}.parquet"
                )
                prices_df.to_parquet(prices_file)
        
        # Get order book
        orderbook = client.get_order_book(market_id)
        if orderbook:
            orderbook_df = pd.DataFrame([orderbook])
            orderbook_file = os.path.join(
                orderbooks_dir, 
                f"orderbook_{market_id}_{timestamp}.parquet"
            )
            orderbook_df.to_parquet(orderbook_file)
            
    print(f"Data collection completed at {datetime.now()}")

if __name__ == "__main__":
    collect_and_save_data()