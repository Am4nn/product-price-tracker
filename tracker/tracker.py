import sys
import yaml
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from parsers import parse_flipkart, parse_amazon, parse_generic
from urllib.parse import urlparse
import asyncio
from telegram import Bot
from supabase_utils import insert_product, log_price
from mimic_browser import mimic_browser_get
from dotenv import load_dotenv
load_dotenv()
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def load_config(path="./config/config.yml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def get_domain_parser(domain):
    if "flipkart" in domain:
        return parse_flipkart
    if "amazon" in domain:
        return parse_amazon
    return parse_generic

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def fetch(url):
    resp = mimic_browser_get(url)
    return resp.text

async def send_telegram(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    async with bot:
      await bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML", disable_web_page_preview=False)

def main():
    cfg = load_config()
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logging.error("Telegram token/chat_id not set")
        sys.exit(1)

    for p in cfg.get("products", []):
        pid = p["id"]
        name = p.get("name") or p["url"]
        url = p["url"]
        domain = p.get("domain") or urlparse(url).netloc
        parser = get_domain_parser(domain)
        logging.info("Checking %s (%s)", name, pid)

        try:
            html = fetch(url)
        except Exception as e:
            logging.exception("Failed to fetch %s: %s", url, e)
            continue

        parsed = parser(html)
        price = parsed.get("price")
        in_stock = parsed.get("in_stock", False)
        title = parsed.get("title") or name

        # Always notify if price <= target or in stock
        notify_messages = []
        target = p.get("target_price")
        if p.get("check_price", True) and price is not None and target is not None and price <= target:
            notify_messages.append(f"<b>{title}</b>\nPrice: ₹{price:,}\nTarget: ₹{target:,}\n{url}")
        if p.get("notify_if_in_stock", True) and in_stock:
            notify_messages.append(f"<b>{title}</b>\nIN STOCK ✅\nPrice: {('₹%s' % format(price, ',')) if price else 'Unknown'}\n{url}")

        if notify_messages:
            try:
                asyncio.run(send_telegram(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, "\n\n".join(notify_messages)))
                logging.info("Sent alert for %s", pid)
            except Exception:
                logging.exception("Failed to send telegram")

        # Insert/update product
        insert_product(pid, title, url)
        # Log every price check
        log_price(pid, price, in_stock)

if __name__ == "__main__":
    main()
