import os
import logging
import asyncio
from flask import Flask, request

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
TOKEN = os.getenv("TELEGRAM_TOKEN")

# --- Bot Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hello, {user.mention_html()}! I'm running on Vercel."
    )

# --- Flask App Setup ---
app = Flask(__name__)

# Build the bot application
ptb_app = Application.builder().token(TOKEN).build()
ptb_app.add_handler(CommandHandler("start", start))


@app.route("/", methods=["POST"])
async def process_update():
    """Main webhook endpoint to process updates from Telegram."""
    try:
        # Convert the incoming Flask request json to a an Update object
        update_data = request.get_json(force=True)
        update = Update.de_json(update_data, ptb_app.bot)

        # Process the update with the bot
        await ptb_app.process_update(update)
        
        return {"status": "ok"}, 200

    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return {"status": "error"}, 500

# A simple health check endpoint
@app.route("/", methods=["GET"])
def health_check():
    return "Bot is running...", 200
