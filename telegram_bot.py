from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from model_config import get_model_response
import os
from dotenv import load_dotenv

# load .env file
load_dotenv()

TOKEN = os.getenv("TOKEN")

# Telegram max message limit
MAX_LENGTH = 4000

# store bot message ids per chat
bot_messages = {}


async def send_long_message(update, text):
    """Split long messages and send with Markdown formatting"""
    chat_id = update.message.chat.id

    for i in range(0, len(text), MAX_LENGTH):
        msg = await update.message.reply_text(
            text[i:i + MAX_LENGTH],
            parse_mode=ParseMode.MARKDOWN
        )

        # store message id
        if chat_id not in bot_messages:
            bot_messages[chat_id] = []

        bot_messages[chat_id].append(msg.message_id)


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

        # If response fits in one message
        if len(text) <= MAX_LENGTH:

            edited_msg = await msg.edit_text(
                text,
                parse_mode=ParseMode.MARKDOWN
            )

            if chat_id not in bot_messages:
                bot_messages[chat_id] = []

            bot_messages[chat_id].append(edited_msg.message_id)

        else:
            await msg.edit_text(
                text[:MAX_LENGTH],
                parse_mode=ParseMode.MARKDOWN
            )

            if chat_id not in bot_messages:
                bot_messages[chat_id] = []

            bot_messages[chat_id].append(msg.message_id)

            for i in range(MAX_LENGTH, len(text), MAX_LENGTH):

                m = await update.message.reply_text(
                    text[i:i + MAX_LENGTH],
                    parse_mode=ParseMode.MARKDOWN
                )

                bot_messages[chat_id].append(m.message_id)

    except Exception as e:
        print("Error:", e)

        await msg.edit_text(
            "⚠️ Something went wrong while processing your request."
        )


async def clear_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear bot messages but keep LLM memory"""

    chat_id = update.message.chat.id

    if chat_id in bot_messages:

        for msg_id in bot_messages[chat_id]:
            try:
                await context.bot.delete_message(chat_id, msg_id)
            except:
                pass

        bot_messages[chat_id] = []

    await update.message.reply_text("🧹 Chat cleared.")


# Create Telegram application
app = ApplicationBuilder().token(TOKEN).build()

# Add message handler
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
)

# Add clear command
app.add_handler(CommandHandler("clear", clear_chat))

print("Bot is running...")

# Start bot
app.run_polling()