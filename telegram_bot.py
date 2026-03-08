from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from model_config import get_model_response
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TOKEN")

# Telegram message length limit
MAX_LENGTH = 4000


async def send_long_message(update, text):
    """
    Send long messages in chunks if they exceed Telegram limits.
    """
    for i in range(0, len(text), MAX_LENGTH):
        await update.message.reply_text(
            text[i:i + MAX_LENGTH],
            parse_mode=ParseMode.MARKDOWN
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text
    chat_id = update.message.chat.id

    # Send thinking message
    msg = await update.message.reply_text("🤖 Thinking...")

    try:
        # Show typing indicator
        await update.message.chat.send_action("typing")

        # Get response from LLM
        response = get_model_response(user_text, chat_id)

        text = response.content

        # If response fits in one message → edit thinking message
        if len(text) <= MAX_LENGTH:
            await msg.edit_text(
                text,
                parse_mode=ParseMode.MARKDOWN
            )

        # If response is long → edit first message + send remaining chunks
        else:
            await msg.edit_text(
                text[:MAX_LENGTH],
                parse_mode=ParseMode.MARKDOWN
            )

            for i in range(MAX_LENGTH, len(text), MAX_LENGTH):
                await update.message.reply_text(
                    text[i:i + MAX_LENGTH],
                    parse_mode=ParseMode.MARKDOWN
                )

    except Exception as e:
        print("Error:", e)

        await msg.edit_text(
            "⚠️ Something went wrong while processing your request."
        )


# Create Telegram application
app = ApplicationBuilder().token(TOKEN).build()

# Add message handler
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
)

print("Bot is running...")

# Start bot
app.run_polling()