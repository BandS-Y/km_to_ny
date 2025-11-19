# bot/messages.py

MESSAGES = {
    "start": {
        "ru": "Привет! Я Telegram-бот.\nИспользуйте /help для получения списка команд.",
        "en": "Hello! I'm a Telegram bot.\nUse /help to see available commands.",
    },
    "help": {
        "ru": (
            "Доступные команды:\n"
            "/start — приветствие\n"
            "/help — помощь\n"
            "/echo <текст> — повторить сообщение\n"
            "/ngdistance <город> — расстояние до Нового Года\n"
            "/lang_en — переключить на английский язык"
        ),
        "en": (
            "Available commands:\n"
            "/start — greeting\n"
            "/help — help\n"
            "/echo <text> — echo message\n"
            "/ngdistance <city> — distance to New Year\n"
            "/lang_ru — switch to Russian"
        ),
    },
    "echo_empty": {
        "ru": "Пустое сообщение.",
        "en": "Empty message."
    },
    "echo_prefix": {
        "ru": "Эхо: {}",
        "en": "Echo: {}"
    },
    # --- ngdistance ---
    "city_not_found": {
        "ru": "Город не найден.\nПожалуйста, укажите широту вашего города (например, 55.75):",
        "en": "City not found.\nPlease enter your city's latitude (for example, 55.75):"
    },
    "ask_city_name": {
        "ru": "Укажите название города (или просто введите его):",
        "en": "Please enter your city name:"
    },
    "incorrect_latitude": {
        "ru": "Некорректный ввод широты. Введите число.",
        "en": "Incorrect latitude. Please enter a number."
    },
    "city_saved": {
        "ru": "Город сохранён!\n\n{}",
        "en": "City saved!\n\n{}"
    },
    # --- language switching ---
    "lang_ru": {
        "ru": "Язык установлен: русский.",
        "en": "Language set: Russian."
    },
    "lang_en": {
        "ru": "Язык установлен: английский.",
        "en": "Language set: English."
    },
    # --- Error / Default ---
    "general_error": {
        "ru": "Произошла ошибка. Попробуйте ещё раз.",
        "en": "An error occurred. Please try again."
    },
}
