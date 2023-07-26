# Substitua 'YOUR_TELEGRAM_BOT_TOKEN' pelo token do seu bot fornecido pelo @BotFather
import requests
import os

TOKEN = os.environ.get("TOKEN")

#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Só coisa boa? {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_html("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    user = update.effective_user
    print("echo ", user.mention_html())
    await update.message.reply_text(update.message.text)


async def noticia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    r = requests.get("http://web:8000/items")
    await update.message.reply_text(r.json()[0]["title"])
    await update.message.reply_html("<a>adfasdfasd</a>")
    # await update.message.reply_text(r.json()[0]['title'])
    # await update.message.reply_html(r.json()[0]['link'])
    await update.message.reply_text("A primeira notícia da API do Gustavo")
    await update.message.reply_text("-------------------")


async def noticia_t(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    r = requests.get("http://web:8000/items")
    # print("gustavo",r.json()[0])
    for i in range(3):
        await update.message.reply_text(r.json()[i]["title"])
    await update.message.reply_text("Todas as noticias da API do Gustavo")
    await update.message.reply_text("-------------------")


async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    r = requests.get("http://web:8000/items")
    # print("gustavo",r.json()[0])
    for i in range(len(r.json())):
        await update.message.reply_text(r.json()[i]["title"])
        await update.message.reply_text(r.json()[i]["link"])
    await update.message.reply_text("Todas as noticias da API do Gustavo")
    await update.message.reply_text("-------------------")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("gugu", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("noticia", noticia))
    application.add_handler(CommandHandler("noticias", noticias))
    application.add_handler(CommandHandler("noticia_t", noticia_t))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
