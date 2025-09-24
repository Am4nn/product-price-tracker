
# Product Price Tracker - Tracker Module

This module is responsible for tracking product prices from e-commerce websites, logging price history, and sending notifications via Telegram. It uses Supabase for database operations and supports Flipkart, Amazon, and generic product pages.

## Features

- Scrapes product prices and stock status from supported e-commerce sites
- Logs price and stock data to a Supabase database
- Sends Telegram alerts when price drops or products are in stock
- Easily extensible for new sites via pluggable parsers

## Directory Structure

- `tracker.py` - Main script for running the tracker
- `parsers.py` - HTML parsers for supported e-commerce sites
- `supabase_utils.py` - Supabase database integration (insert/log functions)
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (Supabase, Telegram, etc.)

## Setup

1. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   Create a `.env` file in the `tracker/` directory with the following:

   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   TELEGRAM_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   ```

3. **Configure products:**
   Edit `../config/config.yml` to add products and notification preferences.

## Usage

Run the tracker:

```sh
python tracker.py
```

The script will check all configured products, log their prices, and send Telegram alerts if conditions are met.

## Database Schema

Supabase schema (PostgreSQL):

```sql
-- Products table
CREATE TABLE "product-price-tracker".products (
   id TEXT PRIMARY KEY,
   title TEXT,
   url TEXT
);

-- Prices table
CREATE TABLE "product-price-tracker".prices (
   id BIGSERIAL PRIMARY KEY,
   product_id TEXT REFERENCES "product-price-tracker".products(id),
   price INTEGER,
   in_stock BOOLEAN,
   checked_at TIMESTAMP DEFAULT NOW()
);
```

## Extending Parsers

To add support for a new site, add a function to `parsers.py` that extracts `price`, `in_stock`, and `title` from the HTML. Update `get_domain_parser()` in `tracker.py` to use your new parser.

## Requirements

- Python 3.8+
- Supabase account (for database)
- Telegram bot (for notifications)

## License

MIT License
