from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from model_config import get_model_response
import os
from dotenv import load_dotenv

# load .env file
load_dotenv()

TOKEN = os.getenv("TOKEN")

# Telegram max message limit
MAX_LENGTH = 4000


async def send_long_message(update, text):
    """Split long messages and send with Markdown formatting"""
    for i in range(0, len(text), MAX_LENGTH):
        await update.message.reply_text(
            text[i:i + MAX_LENGTH],
            parse_mode=ParseMode.MARKDOWN
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    # Show typing indicator
    await update.message.chat.send_action("typing")

    try:
        # Get response from LLM
        chat_id = update.message.chat.id
        response = get_model_response(user_text, chat_id)

        # Send response safely
        await send_long_message(update, response.content)

    except Exception as e:
        print("Error:", e)
        await update.message.reply_text(
            "⚠️ Something went wrong while processing your request."
        )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()