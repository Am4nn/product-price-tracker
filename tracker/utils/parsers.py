from bs4 import BeautifulSoup
import re

def parse_flipkart(html):
    soup = BeautifulSoup(html, "html.parser")
    price_el = soup.select_one(".CxhGGd")
    price = int(re.sub(r"[^\d]", "", price_el.get_text(strip=True))) if price_el else None
    in_stock = "add to cart" in html.lower() or "buy now" in html.lower()
    if "out of stock" in html.lower():
        in_stock = False
    title = soup.title.string.strip() if soup.title and soup.title.string else None
    return {"price": price, "in_stock": in_stock, "title": title}

def parse_amazon(html):
    soup = BeautifulSoup(html, "html.parser")
    price_el = soup.select_one("#priceblock_ourprice") or soup.select_one("#priceblock_dealprice") or soup.select_one(".a-price .a-offscreen")
    price = int(re.sub(r"[^\d]", "", price_el.get_text(strip=True))) if price_el else None
    in_stock = not bool(re.search(r"currently unavailable|out of stock|temporarily out of stock|Coming Soon", html, flags=re.I))
    title_el = soup.select_one("#productTitle")
    title = title_el.get_text(strip=True) if title_el else (soup.title.string.strip() if soup.title and soup.title.string else None)
    return {"price": price, "in_stock": in_stock, "title": title}

def parse_generic(html):
    m = re.search(r"₹\s?[\d,]{2,}|\bINR[\s-]?[\d,]{2,}", html)
    price = int(re.sub(r"[^\d]", "", m.group(0))) if m else None
    in_stock = not bool(re.search(r"out of stock|unavailable|currently unavailable|sold out|Coming Soon", html, flags=re.I))
    return {"price": price, "in_stock": in_stock, "title": None}
