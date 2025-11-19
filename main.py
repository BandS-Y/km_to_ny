from bot.bot_core import TelegramBot
from config import load_config

def main():
    config = load_config()
    bot = TelegramBot(config)
    bot.setup_logging()
    bot.register_handlers()
    bot.run()

if __name__ == "__main__":
    main()
