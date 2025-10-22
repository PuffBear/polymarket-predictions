# Polymarket Prediction Algorithm

This project aims to develop an algorithm for prediction markets, specifically for Polymarket.

## Setup

1. Clone this repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment:
   - Windows: `.\.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with required API key:
```
   POLYMARKET_API_KEY=your_key_here
```
6. Run data collection: `python -m src.data.collect_data`

## Project Structure

- `src/data/`: Data collection modules
- `src/features/`: Feature engineering
- `src/models/`: ML model implementation
- `src/visualization/`: Data visualization
- `data/raw/`: Raw data storage
- `data/processed/`: Processed datasets