import logging
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters
from config import TELEGRAM_TOKEN
from handlers import universal_handler, button_click_handler

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    logging.info("Starting Telegram bot...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, universal_handler))
    app.add_handler(CallbackQueryHandler(button_click_handler))
    logging.info("Bot is running. Waiting for messages...")
    app.run_polling()
    logging.info("Bot stopped.")
