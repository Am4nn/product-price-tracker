import yaml
import logging
import asyncio
from urllib.parse import urlparse
from tenacity import retry, stop_after_attempt, wait_exponential
from utils.parsers import parse_flipkart, parse_amazon, parse_generic
from utils.telegram_utils import send_image_to_telegram, send_telegram
from utils.supabase_utils import insert_product, log_price
from utils.mimic_browser import mimic_browser_get
from utils.env_utils import check_required_envs
from utils.screenshot_utils import html_to_image

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

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

async def main():
    cfg = load_config()
    check_required_envs(["SUPABASE_URL", "SUPABASE_KEY", "TELEGRAM_TOKEN", "TELEGRAM_CHAT_ID"])

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

        # If no price found and out of stock, then send screenshot for manual check
        # if price is None:
        #     try:
        #         image_bytes = html_to_image(html)
        #         await send_image_to_telegram(image_bytes, caption=f"Check {title}\n{url}")
        #         logging.info("Sent screenshot for manual check for %s", pid)
        #     except Exception:
        #         logging.exception("Failed to send screenshot for %s", pid)

        # Always notify if price <= target or in stock
        notify_messages = []
        target = p.get("target_price")
        if p.get("check_price", True) and price is not None and target is not None and price <= target:
            notify_messages.append(f"<b>{title}</b>\nPrice: ₹{price:,}\nTarget: ₹{target:,}\n{url}")
        if p.get("notify_if_in_stock", True) and in_stock:
            notify_messages.append(f"<b>{title}</b>\nIN STOCK ✅\nPrice: {('₹%s' % format(price, ',')) if price else 'Unknown'}\n{url}")

        if notify_messages:
            try:
                await send_telegram("\n\n".join(notify_messages))
                logging.info("Sent alert for %s", pid)
            except Exception:
                logging.exception("Failed to send telegram")

        # Insert/update product
        insert_product(pid, title, url)
        # Log every price check
        log_price(pid, price, in_stock)

if __name__ == "__main__":
    asyncio.run(main())
