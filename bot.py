import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Значения берутся из переменных окружения Render
TOKEN = os.environ["BOT_TOKEN"]
SUB_URL = os.environ["SUB_URL"]
SUPPORT_URL = os.environ["SUPPORT_URL"]
PUBLIC_URL = os.environ["RENDER_EXTERNAL_URL"]  # Render задаёт это сам
PORT = int(os.environ.get("PORT", "10000"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔑 Получить подписку", callback_data="sub")],
        [InlineKeyboardButton("🆘 Поддержка", url=SUPPORT_URL)],
    ])
    await update.message.reply_text(
        "NEXTPROJECT VPN\n\nНажмите «Получить подписку», чтобы получить ссылку.",
        reply_markup=kb,
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "sub":
        await q.message.reply_text(
            "Ваша ссылка подписки:\n\n"
            f"{SUB_URL}\n\n"
            "Скопируйте её и в Happ нажмите «+» → «Добавить из буфера»."
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=f"{PUBLIC_URL}/webhook",
    )

if __name__ == "__main__":
    main()
