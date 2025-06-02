from telegram.ext import ApplicationBuilder
from handlers import register_handlers
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    register_handlers(app)
    print("Nova is now live.")
    app.run_polling()

if __name__ == "__main__":
    main()
