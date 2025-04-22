from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from googletrans import Translator

BOT_TOKEN = 'توکن ربات'
CHANNEL_ID = '@channelusername'  # یا -1001234567890

translator = Translator()

async def handle_forwarded(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.forward_date:
        return

    # اگر پیام متنی بود
    if update.message.text:
        original_text = update.message.text
        translation = translator.translate(original_text, dest='fa').text
        final_text = f"{translation}\n\n📝 ترجمه شده توسط ربات مترجم ما"
        await context.bot.send_message(chat_id=CHANNEL_ID, text=final_text)

    # اگر عکس بود
    elif update.message.photo:
        caption = update.message.caption or ""
        translated = translator.translate(caption, dest='fa').text if caption else ""
        await context.bot.send_photo(chat_id=CHANNEL_ID, photo=update.message.photo[-1].file_id,
                                     caption=f"{translated}\n\n🖼️ ترجمه شده")

    # اگر ویدیو بود
    elif update.message.video:
        caption = update.message.caption or ""
        translated = translator.translate(caption, dest='fa').text if caption else ""
        await context.bot.send_video(chat_id=CHANNEL_ID, video=update.message.video.file_id,
                                     caption=f"{translated}\n\n🎥 ترجمه شده")

    # اگر فایل بود (document)
    elif update.message.document:
        caption = update.message.caption or ""
        translated = translator.translate(caption, dest='fa').text if caption else ""
        await context.bot.send_document(chat_id=CHANNEL_ID, document=update.message.document.file_id,
                                        caption=f"{translated}\n\n📎 ترجمه شده")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.FORWARDED, handle_forwarded))

app.run_polling()
