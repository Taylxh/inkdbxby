from telegram import Update

# Get Telegram user ID and username
def get_user_identity(update: Update):
    user = update.effective_user
    return str(user.id), user.username or "unknown"

# Build a standard formatted caption with optional extras
def build_caption(text):
    return text.strip()

# Send a photo from the /media/ folder
def send_photo(update: Update, filename, caption=None):
    with open(f"media/{filename}", "rb") as photo:
        return update.message.reply_photo(photo=photo, caption=caption)
