"""
Execute the bot in Push mode.
Push mode: the bot receives new messages from webhooks sent by Telegram.
"""
import json

from telegram import Update, Bot as TelegramBot
from telegram.ext import Dispatcher

import commands
from common import env_validator, logs

logger = logs.get_logger(__name__)

telegram_token = env_validator.get_or_throw('TELEGRAM_BOT_TOKEN')

telegram = TelegramBot(token=telegram_token)
dispatcher = Dispatcher(telegram, None, use_context=True)


def lambda_handler(event, context):
    try:
        commands.add_supported_commands(dispatcher)

        dispatcher.process_update(
            Update.de_json(json.loads(event["body"]), telegram)
        )

        return {"statusCode": 200}

    except Exception as e:
        logger.error(e)
        return {"statusCode": 500}
