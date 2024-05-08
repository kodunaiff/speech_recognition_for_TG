from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from environs import Env
import logging
from google.cloud import dialogflow

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте!")


def detect_intent_texts(texts, project_id, session_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=texts, language_code='RU')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


def get_dialogue(update: Update, context: CallbackContext):
    text = update.message.text
    project_id = context.bot_data["project_id"]
    session_id = context.bot_data["session_id"]
    texts = detect_intent_texts(text, project_id, session_id)
    update.message.reply_text(texts)


def main():
    env = Env()
    env.read_env()
    tg_token = env.str("TELEGRAM_BOT_TOKEN")
    project_id = env.str("PROJECT_ID")
    session_id = env.str("TG_USER_ID")

    updater = Updater(token=tg_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data["project_id"] = project_id
    dispatcher.bot_data["session_id"] = session_id
    dispatcher.update_persistence()

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), get_dialogue))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
