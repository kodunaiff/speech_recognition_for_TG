import logging

from environs import Env
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters

from checked_result import TelegramLogsHandler
from d_f_handler import detect_intent_texts

logger = logging.getLogger()


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте!!! Это бот - Поддержки!")


def get_dialogue(update: Update, context: CallbackContext):
    text = update.message.text
    project_id = context.bot_data["project_id"]
    session_id = context.bot_data["session_id"]
    texts = detect_intent_texts(text, project_id, session_id)
    update.message.reply_text(texts.query_result.fulfillment_text)


def main():
    env = Env()
    env.read_env()
    tg_token = env.str("TELEGRAM_BOT_TOKEN")
    telegram_logging_token = env.str("TELEGRAM_LOGGING_BOT_TOKEN")
    project_id = env.str("PROJECT_ID")
    tg_user_id = env.str("TG_USER_ID")

    updater = Updater(token=tg_token)
    dispatcher = updater.dispatcher

    logger.setLevel(logging.INFO)
    logger_bot = Updater(telegram_logging_token).dispatcher.bot
    logger.addHandler(TelegramLogsHandler(logger_bot, tg_user_id))
    logger.info("ТГ Бот запущен!")

    dispatcher.bot_data["project_id"] = project_id
    dispatcher.bot_data["session_id"] = tg_user_id
    dispatcher.update_persistence()

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), get_dialogue))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
