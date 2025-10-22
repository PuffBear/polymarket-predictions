import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
POLYMARKET_API_KEY = os.getenv("POLYMARKET_API_KEY")

# Base URLs
POLYMARKET_BASE_URL = "https://clob.polymarket.com"

# Data paths
RAW_DATA_PATH = "data/raw"
PROCESSED_DATA_PATH = "data/processed"
MODELS_PATH = "data/models"

# Ensure required environment variables are set
if not POLYMARKET_API_KEY:
    raise EnvironmentError("POLYMARKET_API_KEY environment variable is not set")

# Database configuration (if using)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "polymarket_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# API rate limiting settings
REQUEST_DELAY = 1  # seconds between API calls