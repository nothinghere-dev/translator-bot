import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from deep_translator import GoogleTranslator
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")  # کانال آیدی رو هم بذار تو محیط امن

async def handle_forwarded_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.forward_from_chat or update.message.forward_from:
        original_text = update.message.text
        if original_text:
            try:
                translated = GoogleTranslator(source='auto', target='en').translate(original_text)
                await context.bot.send_message(chat_id=CHANNEL_ID, text=translated)
            except Exception as e:
                await update.message.reply_text(f"Error: {e}")
        else:
            await update.message.reply_text("No text to translate.")

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    handler = MessageHandler(filters.FORWARDED & filters.TEXT, handle_forwarded_message)
    application.add_handler(handler)
    application.run_polling()

if __name__ == "__main__":
    main()
