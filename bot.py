import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator

# توکن ربات و آیدی کانال از متغیر محیطی
BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']


# تابع برای ترجمه متن
def translate_text(text, target_language="fa"):
    translated = GoogleTranslator(source='auto', target=target_language).translate(text)
    return translated

# تابع برای ارسال پیام به کانال
async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # دریافت پیام فوروارد شده
    forwarded_text = update.message.text
    
    # ترجمه پیام
    translated_text = translate_text(forwarded_text)
    
    # اضافه کردن متن دلخواه به انتهای پیام ترجمه شده
    final_text = translated_text + "\n\n#ترجمه‌شده"

    # ارسال پیام به کانال
    await context.bot.send_message(chat_id=CHANNEL_ID, text=final_text)

# ساخت ربات و افزودن هندلر
async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # هندلر برای پیام‌های فوروارد شده
    forward_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, forward_message)
    application.add_handler(forward_handler)

    # اجرای ربات
    await application.run_polling()

import asyncio

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "event loop is running" in str(e):
            loop = asyncio.get_event_loop()
            loop.create_task(main())
            loop.run_forever()
        else:
            raise

