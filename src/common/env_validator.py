import os


def get_telegram_token_or_throw() -> str:
    telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not telegram_token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not defined")
    return telegram_token
