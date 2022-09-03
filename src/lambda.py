import json
import logging

from telegram import Update, Bot
from telegram.ext import CommandHandler, Dispatcher, Filters, MessageHandler

import main
from common import env_validator

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

telegram_token = env_validator.get_telegram_token_or_throw()

bot = Bot(token=telegram_token)
dispatcher = Dispatcher(bot, None, use_context=True)


def lambda_handler(event, context):
    try:
        # supported commands
        dispatcher.add_handler(CommandHandler("start", main.start_command))
        dispatcher.add_handler(CommandHandler("help", main.help_command))
        dispatcher.add_handler(CommandHandler("price", main.price_command))
        dispatcher.add_handler(CommandHandler("return", main.return_command))
        dispatcher.add_handler(CommandHandler("vol", main.volatility_command))
        dispatcher.add_handler(CommandHandler("all", main.all_command))

        # handle unknown commands or text
        dispatcher.add_handler(
            MessageHandler(Filters.command | Filters.text, main.unknown_command)
        )

        dispatcher.process_update(
            Update.de_json(json.loads(event["body"]), bot)
        )

        return {"statusCode": 200}

    except Exception as e:
        logger.error(e)
        return {"statusCode": 500}
