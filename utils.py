from telegram import Update
from telegram.ext import CallbackContext

# Clean and normalize text for trigger matching
def normalize(text):
    return text.lower().strip()

# Check if a message matches a trigger category
def match_trigger(message, triggers):
    message = normalize(message)
    for keyword in triggers:
        if keyword in message:
            return True
    return False

# Send a plain text message
def send_text(update: Update, context: CallbackContext, message: str):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Send a photo from a file or URL
def send_photo(update: Update, context: CallbackContext, photo, caption=None):
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=caption)

# Send a document (for large files or vault content)
def send_document(update: Update, context: CallbackContext, file_path, caption=None):
    context.bot.send_document(chat_id=update.effective_chat.id, document=open(file_path, 'rb'), caption=caption)
