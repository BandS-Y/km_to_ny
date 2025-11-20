# bot/handlers.py

from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from loguru import logger
from resources.messages import MESSAGES
from bot.ng_calculator import (
    get_city_info,
    get_city_localtime,
    format_result,
    save_user_city
)

# ------------------------ #
# Централизованные функции #
# ------------------------ #

def get_msg(key, lang="ru", *args):
    """
    Универсальный геттер текстов. Если не найден язык — fallback на русский.
    """
    text = MESSAGES[key].get(lang, MESSAGES[key]["ru"])
    return text.format(*args) if args else text

def get_user_lang(context):
    # Можно сделать определение языка по Telegram (или хранить в базе пользователя)
    # Пока — по user_data
    return context.user_data.get("lang", "ru")

# --------------------- #
# Стандартные команды   #
# --------------------- #

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(context)
    await update.message.reply_text(get_msg("start", lang))
    logger.info(f"/start user {update.effective_user.id}")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(context)
    await update.message.reply_text(get_msg("help", lang))
    logger.info(f"/help user {update.effective_user.id}")

async def echo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(context)
    text = " ".join(context.args) if context.args else get_msg("echo_empty", lang)
    await update.message.reply_text(get_msg("echo_prefix", lang, text))
    logger.info(f"/echo user {update.effective_user.id}: {text}")

async def cities_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(context)
    logger.info(f"/help user {update.effective_user.id}")


# --------------------------- #
# Смена языка (команды)       #
# --------------------------- #

async def lang_ru_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["lang"] = "ru"
    await update.message.reply_text(get_msg("lang_ru", "ru"))

async def lang_en_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["lang"] = "en"
    await update.message.reply_text(get_msg("lang_en", "en"))

# --------------------- #
# Команды ngdistance    #
# --------------------- #

ASK_LAT, CONFIRM_SAVE = range(2)

async def ngdistance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(context)
    user_id = update.effective_user.id
    city_arg = " ".join(context.args) if context.args else None
    city = get_city_info(user_id, city_arg)
    if city:
        now = get_city_localtime(city)
        result = format_result(city, now, lang=lang)
        await update.message.reply_text(result)
        logger.info(f"/ngdistance for user {user_id}, city: {city['name']}")
        return ConversationHandler.END
    else:
        await update.message.reply_text(get_msg("city_not_found", lang))
        return ASK_LAT

async def ask_latitude(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(context)
    try:
        lat = float(update.message.text.replace(",", "."))
        context.user_data["latitude"] = lat
        await update.message.reply_text(get_msg("ask_city_name", lang))
        return CONFIRM_SAVE
    except Exception:
        await update.message.reply_text(get_msg("incorrect_latitude", lang))
        return ASK_LAT

async def save_city_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(context)
    name = update.message.text.strip()
    lat = context.user_data.get("latitude")
    tz_shift = 0  # можно доработать
    user_id = update.effective_user.id
    save_user_city(user_id, name, lat, tz_shift)
    city = get_city_info(user_id)
    now = get_city_localtime(city)
    result = format_result(city, now, lang=lang)
    await update.message.reply_text(get_msg("city_saved", lang, result))
    logger.info(f"User {user_id} saved city {name} ({lat})")
    return ConversationHandler.END

def get_ngdistance_conv_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("ngdistance", ngdistance_cmd)],
        states={
            ASK_LAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_latitude)],
            CONFIRM_SAVE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_city_name)],
        },
        fallbacks=[],
    )

# --------------------- #
# Регистрация команд    #
# --------------------- #

def register_handlers(app):
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    # app.add_handler(CommandHandler("echo", echo_cmd))
    app.add_handler(CommandHandler("echo", cities_cmd))
    app.add_handler(CommandHandler("lang_ru", lang_ru_cmd))
    app.add_handler(CommandHandler("lang_en", lang_en_cmd))
    app.add_handler(get_ngdistance_conv_handler())
