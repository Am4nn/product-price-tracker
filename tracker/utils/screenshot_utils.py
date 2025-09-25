"""
Utility to render HTML and return an image object (PIL Image) for direct use with Telegram bot.
Requires: selenium, pillow, and a compatible webdriver (e.g., ChromeDriver).
"""
import os
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def html_to_image(html, width=1200, height=800):
    """
    Renders the given HTML string and returns a PIL Image object.
    """
    # Write HTML to a temporary file
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html)
        temp_html_path = f.name
    # Setup headless Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(f'--window-size={width},{height}')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f'file://{temp_html_path}')
    # Take screenshot as PNG bytes
    png = driver.get_screenshot_as_png()
    driver.quit()
    os.remove(temp_html_path)
    return png
