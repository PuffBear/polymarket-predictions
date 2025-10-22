import os
import sys
import pandas as pd
from datetime import datetime
import time
import json
import uuid

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
    os.makedirs(markets_dir, exist_ok=True)
    
    # Step 1: Get all markets
    print("Fetching all markets...")
    markets_data = client.get_markets()
    
    # If data is a list, process each item
    if isinstance(markets_data, list):
        # Generate unique IDs for markets that don't have them
        processed_markets = []
        
        for market in markets_data:
            if isinstance(market, dict):
                # Try different ID fields
                market_id = (
                    market.get('id') or 
                    market.get('market_id') or 
                    market.get('marketId') or
                    market.get('condition_id') or
                    market.get('question_id')
                )
                
                if not market_id:
                    # Generate a UUID if no ID is found
                    market_id = str(uuid.uuid4())
                    print(f"Generated ID {market_id} for market: {market.get('question', 'Unknown')}")
                
                # Add the ID to the market data
                market['market_id'] = market_id
                processed_markets.append(market)
        
        # Save the processed markets
        if processed_markets:
            markets_df = pd.DataFrame(processed_markets)
            markets_file = os.path.join(markets_dir, f"markets_{timestamp}.parquet")
            markets_df.to_parquet(markets_file)
            print(f"Saved {len(markets_df)} markets to {markets_file}")
    else:
        print(f"Unexpected data type from API: {type(markets_data)}")
        # Save raw data for debugging
        with open(os.path.join(markets_dir, f"raw_markets_data_{timestamp}.json"), 'w') as f:
            json.dump(markets_data, f, default=str)

if __name__ == "__main__":
    collect_and_save_data()