from telegram.ext import ApplicationBuilder
from handlers.menu import menu_handler, menu_button_handler
from handlers.custom import custom_handler
from handlers.message import message_handler
from constants import BOT_TOKEN

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Button menus and custom commands
    app.add_handler(menu_handler)
    app.add_handler(menu_button_handler)
    app.add_handler(custom_handler)

    # Fallback handler (Nova’s main chat logic)
    app.add_handler(message_handler)

    print("Nova is now running as the Inkdbxby bot...")
    app.run_polling()

if __name__ == "__main__":
    main()
