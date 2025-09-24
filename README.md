# 📦 PriceTracker – iPhone & More (Flipkart/Amazon etc.)

A modular price & stock tracker with:

- 🔍 **Python Scraper** (tracks product stock & price in real-time)
- 💾 **Supabase (Postgres)** database for centralized history
- 📊 **Next.js UI** with charts for price history visualization
- 📢 **Telegram Alerts** for instant notifications when prices drop or stock returns
- ⚡ **GitHub Actions Scheduler** for automation (no server cost!)

---

## 🏗️ Project Architecture

```plaintext
price-tracker/
│── tracker/           # Python scraper
│   ├── tracker.py     # Main runner
│   ├── parsers.py     # Site-specific HTML parsers
│   ├── utils.py       # DB + helpers
│   ├── alerts.py      # Telegram integration
│   └── requirements.txt
│
│── ui/                # Next.js 14+ app (charts & API)
│   ├── app/
│   │   ├── page.tsx   # Dashboard
│   │   ├── api/       # API routes to fetch data from Supabase
│   │   └── components/
│   │       └── PriceChart.tsx
│   ├── package.json
│   └── tsconfig.json
│
│── .github/workflows/ # GitHub Actions for scheduling tracker
│   └── tracker.yml
│
│── .env.example       # Example env variables
│── README.md          # This file
```

---

## ⚙️ Features

- ✅ Track multiple products across sites
- ✅ Store full price history in Supabase
- ✅ Plot history with interactive chart UI (Next.js + Recharts)
- ✅ Get Telegram notifications for in-stock / price drops
- ✅ Fully automated with GitHub Actions (no server needed)
- ✅ Configurable via .env

---

## 🔑 Requirements

- Python 3.9+
- Node.js 18+ (for Next.js UI)
- Supabase account (free tier works)
- Telegram Bot (for alerts)

---

## 🚀 Getting Started

1. **Clone Repo**

   ```sh
   git clone https://github.com/yourname/price-tracker.git
   cd price-tracker
   ```

2. **Setup .env**

   Copy `.env.example` → `.env` and fill in:

   ```env
   # Supabase Postgres
   SUPABASE_DB_URL=postgres://user:pass@host:5432/dbname

   # Telegram Bot
   TELEGRAM_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id

   # Next.js (UI)
   NEXT_PUBLIC_SUPABASE_URL=https://xyzcompany.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
   ```

3. **Install Dependencies**

   *Python Tracker*

   ```sh
   cd tracker
   pip install -r requirements.txt
   ```

   *Next.js UI*

   ```sh
   cd ../ui
   npm install
   ```

4. **Run Locally**

   *Tracker (manual run)*

   ```sh
   cd tracker
   python tracker.py
   ```

   *UI*

   ```sh
   cd ../ui
   npm run dev
   ```

   Dashboard will be available at 👉 [http://localhost:3000](http://localhost:3000)

---

## ⚡ Deployment

### GitHub Actions (Tracker automation)

- Add secrets in GitHub Repo → Settings → Secrets:
  - SUPABASE_DB_URL
  - TELEGRAM_TOKEN
  - TELEGRAM_CHAT_ID
- Tracker will run every 30 min (configurable in `.github/workflows/tracker.yml`).

### Vercel (UI)

- Connect repo to Vercel
- Add env vars:
  - NEXT_PUBLIC_SUPABASE_URL
  - NEXT_PUBLIC_SUPABASE_ANON_KEY
- Deploy → Live price dashboard online!

---

## 📊 Database Schema

```sql
CREATE TABLE products (
    id TEXT PRIMARY KEY,
    title TEXT,
    url TEXT
);

CREATE TABLE prices (
    id BIGSERIAL PRIMARY KEY,
    product_id TEXT REFERENCES products(id),
    price INTEGER,
    in_stock BOOLEAN,
    checked_at TIMESTAMP DEFAULT NOW()
);
```

---

## 📢 Alerts

All alerts are sent via Telegram Bot. You will receive:

- Price drops (≤ your configured threshold)
- Back in stock notifications

---

## 🧩 Extending

- Add new parsers in `tracker/parsers.py` for more websites
- Modify UI to group products by category
- Export price history as CSV from Supabase

---

## 🌟 Example Use Cases

- Track iPhone 16 Pro price drops during Flipkart/Amazon BBD sales 📱
- Monitor GPU stock & prices 🎮
- Watchbook airfares or flash sale items ✈️

---

## 📝 License

MIT – free to use & modify.
