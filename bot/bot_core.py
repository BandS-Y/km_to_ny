import os

from loguru import logger
# from telegram import Update
from telegram.ext import (
    Application, CommandHandler #, ContextTypes
)
from bot.handlers import (
    start_cmd, help_cmd, echo_cmd,
    get_ngdistance_conv_handler
)

class TelegramBot:
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    def __init__(self, config):
        self.token = config['TOKEN']
        self.log_level = config['LOG_LEVEL']
        self.log_file = config['LOG_FILE']
        self.app = Application.builder().token(self.token).build()

    def setup_logging(self):
        logger.remove()
        logger.add(self.log_file, rotation="10 MB", level=self.log_level)
        logger.info("Логирование инициализировано")

    def register_handlers(self):
        self.app.add_handler(CommandHandler("start", start_cmd))
        self.app.add_handler(CommandHandler("help", help_cmd))
        self.app.add_handler(CommandHandler("echo", echo_cmd))
        self.app.add_handler(get_ngdistance_conv_handler())
        logger.info("Обработчики команд зарегистрированы")

    def run(self):
        logger.info("Запуск бота")
        self.app.run_polling()
