import random
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from constants import TRIGGERS, PRICES, VAULT_TIERS, TABOO_WORDS
from memory import get_fan_memory, update_fan_memory, get_fan_rank, check_proof_sheet
from sheets import get_vault_preview
from utils import is_silent_hours, random_response

def handle_message(update, context):
    text = update.message.text.lower()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message = None

    # Block taboo words
    if any(word in text for word in TABOO_WORDS):
        update.message.reply_text("Sorry babe, that kink’s off limits here.")
        return

    # Check silent hours
    if is_silent_hours():
        return

    # Menu triggers
    if any(trigger in text for trigger in TRIGGERS["menu"]):
        send_menu(update, context)
        return

    # Vault previews
    if any(trigger in text for trigger in TRIGGERS["preview"]):
        tier = detect_vault_tier(text)
        if tier:
            preview = get_vault_preview(tier)
            if preview:
                context.bot.send_message(chat_id=chat_id, text=preview)
            else:
                context.bot.send_message(chat_id=chat_id, text="That vault isn’t ready yet.")
        else:
            context.bot.send_message(chat_id=chat_id, text="Which vault do you want a preview of?")
        return

    # Custom request
    if any(trigger in text for trigger in TRIGGERS["custom"]):
        update.message.reply_text("Tell me exactly what you want, babe... customs start at $100 and must be paid upfront.")
        return

    # Memory request
    if any(trigger in text for trigger in TRIGGERS["memory"]):
        memory = get_fan_memory(user_id)
        if memory:
            update.message.reply_text(f"Here's what I remember about you: {memory}")
        else:
            update.message.reply_text("Hmm, I don’t know your kinks yet. Tell me more and I’ll remember.")
        return

    # Tip triggers
    if any(trigger in text for trigger in TRIGGERS["tip"]):
        update.message.reply_text("A little something for your girl? Send a screenshot of your tip and I’ll make it worth it.")
        return

    # Payment proof
    if any(trigger in text for trigger in TRIGGERS["proof"]):
        confirmed = check_proof_sheet(user_id)
        if confirmed:
            update.message.reply_text("Got it baby. Your payment’s confirmed. I’ll deliver soon 💌")
        else:
            update.message.reply_text("I need a clear screenshot showing the amount, date, and where you sent it.")
        return

    # Bundle teasing
    if any(trigger in text for trigger in TRIGGERS["bundle"]):
        update.message.reply_text("Each mystery bundle’s packed with spicy surprises... let me know your vibe and budget and I’ll recommend the perfect one.")
        return
          # Aftercare
    if any(trigger in text for trigger in TRIGGERS["aftercare"]):
        update.message.reply_text(random_response([
            "You did so good for me... now relax, breathe, and let that body recover.",
            "Mmm I loved every second. Lay back and replay it in your mind… slowly.",
            "That was intense, baby. Hydrate and take care of that pretty body for me."
        ]))
        return

    # Save kink memory
    if any(trigger in text for trigger in TRIGGERS["kink"]):
        update_fan_memory(user_id, text)
        update.message.reply_text("Mmm noted. I’ll remember exactly what you like.")
        return

    # Default fallback
    update.message.reply_text(random_response([
        "Tell me what you’re craving...",
        "Be specific, babe. I’m listening...",
        "Wanna see something special? Ask for a menu."
    ]))

def send_menu(update, context):
    chat_id = update.effective_chat.id
    keyboard = [
        [InlineKeyboardButton("Taster Menu", callback_data="menu_taster")],
        [InlineKeyboardButton("Mystery Vault Bundle", callback_data="menu_bundle")],
        [InlineKeyboardButton("Custom Menu", callback_data="menu_custom")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=chat_id, text="Pick a menu to see what's on offer:", reply_markup=reply_markup)

def handle_callback(update, context):
    query = update.callback_query
    query.answer()
    data = query.data
    chat_id = query.message.chat_id

    if data == "menu_taster":
        context.bot.send_photo(chat_id=chat_id, photo=open("menu_files/taster_menu.jpg", "rb"))
    elif data == "menu_bundle":
        context.bot.send_photo(chat_id=chat_id, photo=open("menu_files/mystery_vault_bundle.jpg", "rb"))
    elif data == "menu_custom":
        context.bot.send_photo(chat_id=chat_id, photo=open("menu_files/custom_menu.jpg", "rb"))
    else:
        context.bot.send_message(chat_id=chat_id, text="Something went wrong. Try again.")
      
