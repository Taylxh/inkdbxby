# main.py
import os
from telegram.ext import ApplicationBuilder
from handlers.handlers import register_handlers
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    register_handlers(application)
    application.run_polling()

if __name__ == "__main__":
    main()
