import os
from logging import Handler

import requests
import environ
from django.conf import settings

env = environ.Env()
environ.Env.read_env(os.path.join(settings.BASE_DIR, ".env"))

TELEGRAM_BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = env.str("TELEGRAM_CHAT_ID")


class TelegramLogger(Handler):
    def emit(self, record):
        log_entry = self.format(record)
        self.send_telegram_message(log_entry)

    @staticmethod
    def send_telegram_message(log_entry):
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        params = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': log_entry,
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error sending Telegram message: {response.text}")
