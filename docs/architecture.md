# 🏗️ Architecture – PriceTracker

This document explains the internal architecture of the PriceTracker project: how each module works, how they interact, and how data flows across the system.

## 🔹 High-Level Overview

```plaintext
 ┌─────────────┐        ┌───────────────┐       ┌──────────────┐
 │   Tracker   │  --->  │   Supabase    │  ---> │   Next.js UI │
 │ (Python)    │        │   (Postgres)  │       │ (Dashboard)  │
 └─────────────┘        └───────────────┘       └──────────────┘
        │                        │                       │
        └─── Telegram Alerts <───┘                       │
```

- **Tracker (Python):** Scrapes product pages, parses HTML, logs price + stock.
- **Supabase DB:** Central store for product metadata + historical price logs.
- **Next.js UI:** Fetches data from Supabase and plots price charts.
- **Telegram Bot:** Sends notifications for price drops / stock availability.

## 🔹 Components

### 1. Tracker (`tracker/`)

- `tracker.py` – Main runner. Orchestrates scraping, DB logging, and alerting.
- `parsers.py` – Site-specific logic (e.g., Flipkart, Amazon). Each parser extracts title, price, in_stock.
- `utils.py` – DB helpers (insert product, log price). Uses Supabase Postgres.
- `alerts.py` – Sends messages to Telegram.
- 🕒 Runs every 30 min (configurable) via GitHub Actions.

### 2. Database (Supabase)

- **Products Table:** Stores unique product IDs, titles, and URLs.
- **Prices Table:** Logs each run → product_id, price, stock, timestamp. Enables history plotting + alerts.

### 3. UI (`ui/`)

- Built with Next.js 14+ App Router.
- `/app/page.tsx` – Dashboard.
- `/app/api/prices/[productId]/route.ts` – API route to fetch price history.
- `/components/PriceChart.tsx` – Plots historical price with Recharts.
- Frontend only reads from Supabase – no backend server required.

### 4. Alerts

- Implemented in `tracker/alerts.py`.
- Uses Telegram Bot API.
- **Conditions:**
  - Stock available → notify.
  - Price ≤ threshold → notify.
- Configurable per product.

## 🔹 Data Flow

1. Scraper fetches product page
2. HTML parsed → extract title, price, in_stock
3. Data written to Supabase
   - Insert/update product in products
   - Insert price log in prices
4. Alert triggered (if conditions met)
   - Send Telegram message
5. UI fetches from Supabase
   - API route queries prices
   - Chart updates dynamically

## 🔹 Deployment

- **Tracker:** Runs on GitHub Actions (no server cost)
- **DB:** Supabase (cloud Postgres, free tier)
- **UI:** Deploy on Vercel, reads Supabase directly

## 🔹 Extensibility

- Add more e-commerce sites → new parser in `parsers.py`
- Change alert mechanism → add Slack, Email, Discord in `alerts.py`
- Switch DB → Postgres/MySQL by editing `utils.py`
- Scale tracker → run every 5 min instead of 30 min

## 🔹 Trade-offs & Choices

- **Supabase chosen:** free Postgres + auth + API → easy UI integration
- **GitHub Actions:** avoids server/VPS costs
- **Telegram over SMTP:** faster, reliable, no spam filters
- **SQLite dropped:** not scalable across multiple deployments
