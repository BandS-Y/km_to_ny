import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        'TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),
        'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
        'LOG_FILE': os.getenv('LOG_FILE', 'logs/bot.log')
    }
