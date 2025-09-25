# Utility for sending Telegram messages
from telegram import Bot
from utils.env_utils import get_env_var

TELEGRAM_TOKEN: str = get_env_var("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID: str = get_env_var("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)
	
async def send_telegram(message: str):
  async with bot:
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="HTML", disable_web_page_preview=False)

async def send_image_to_telegram(image_bytes, caption=None):
    async with bot:
        await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=image_bytes, caption=caption)
