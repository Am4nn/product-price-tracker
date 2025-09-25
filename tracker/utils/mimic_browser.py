import requests
import random
import time
try:
    from getuseragent import UserAgent
    ua_provider = UserAgent()
except ImportError:
    ua_provider = None

# List of common user agents (Chrome, Firefox, Edge, Safari, Mobile)
USER_AGENTS = [
    # Chrome (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    # Firefox (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    # Edge (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    # Chrome (Mac)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    # Safari (Mac)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    # Chrome (Android)
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    # Safari (iPhone)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
]

# Common headers to mimic a real browser
COMMON_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
    "Referer": "https://www.google.com/",
}

def mimic_browser_get(url, delay_range=(1, 4), max_redirects=10):
    """
    Perform a GET request mimicking a real browser as closely as possible.
    Follows all HTTP redirects, meta-refresh, and JS-based redirects (best effort).
    """
    headers = COMMON_HEADERS.copy()
    if ua_provider:
        headers["User-Agent"] = str(ua_provider.Random())
    else:
        headers["User-Agent"] = random.choice(USER_AGENTS)

    accept_languages = [
        "en-US,en;q=0.9",
        "en-GB,en;q=0.8",
        "en-US,en;q=0.7,fr;q=0.3",
        "en-US,en;q=0.9,hi;q=0.8",
        "en-US,en;q=0.9,es;q=0.8",
    ]
    headers["Accept-Language"] = random.choice(accept_languages)

    referers = [
        "https://www.google.com/",
        "https://www.bing.com/",
        "https://duckduckgo.com/",
        "https://search.yahoo.com/",
        url.split("/")[0] + "//" + url.split("/")[2] + "/" if url.startswith("http") else "",
        ""
    ]
    headers["Referer"] = random.choice(referers)

    time.sleep(random.uniform(*delay_range))

    session = requests.Session()
    session.headers.update(headers)
    current_url = url
    for _ in range(max_redirects):
        response = session.get(current_url, timeout=20, allow_redirects=True)
        # HTTP redirects are handled by requests
        # Check for meta-refresh
        if response.status_code in (301, 302, 303, 307, 308):
            current_url = response.headers.get('Location', current_url)
            continue
        html = response.text
        # Meta-refresh
        import re
        meta_refresh = re.search(r'<meta[^>]*http-equiv=["\']?refresh["\']?[^>]*content=["\']?\d+;\s*url=([^"\'>]+)', html, re.IGNORECASE)
        if meta_refresh:
            next_url = meta_refresh.group(1)
            if not next_url.startswith('http'):
                from urllib.parse import urljoin
                next_url = urljoin(current_url, next_url)
            current_url = next_url
            continue
        # JS-based window.location redirects (best effort)
        js_redirect = re.search(r'window\.location(?:\.href)?\s*=\s*["\']([^"\']+)["\']', html)
        if js_redirect:
            next_url = js_redirect.group(1)
            if not next_url.startswith('http'):
                from urllib.parse import urljoin
                next_url = urljoin(current_url, next_url)
            current_url = next_url
            continue
        # If no more redirects, return response
        return response
    raise RuntimeError(f"Too many redirects when trying to fetch {url}")
