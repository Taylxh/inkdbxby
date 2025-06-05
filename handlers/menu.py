from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, MessageHandler, filters, CallbackQueryHandler
from logic import TRIGGERS

# Menu button layout
def build_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Taster Menu", callback_data="menu_taster")],
        [InlineKeyboardButton("Vault Bundle Menu", callback_data="menu_vault")],
        [InlineKeyboardButton("Custom Menu", callback_data="menu_custom")]
    ])

# Triggered when user sends a text like "menu", "send prices", etc
async def handle_menu_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.lower()
    for trigger in TRIGGERS["menu"]:
        if trigger in message_text:
            keyboard = build_menu_keyboard()
            await update.message.reply_photo(
                photo=open("media/content_menu.jpg", "rb"),
                caption="What are you craving? Choose a menu below to see what’s on offer.",
                reply_markup=keyboard
            )
            return

# Triggered when user taps one of the 3 buttons
async def handle_menu_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == "menu_taster":
        await query.message.reply_photo(
            photo=open("media/taster_menu.jpg", "rb"),
            caption="Here’s your Taster Menu. A little taste before the deeper cravings hit..."
        )
    elif choice == "menu_vault":
        await query.message.reply_photo(
            photo=open("media/vault_menu.jpg", "rb"),
            caption="Here’s your Mystery Vault Bundle Menu... Each tier gets naughtier the higher you go."
        )
    elif choice == "menu_custom":
        await query.message.reply_photo(
            photo=open("media/custom_menu.jpg", "rb"),
            caption="Feeling specific? This Custom Menu is all about *you* — but make it worth my time."
        )

# Handler setup to connect with main.py
menu_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_request)
menu_button_handler = CallbackQueryHandler(handle_menu_button)
