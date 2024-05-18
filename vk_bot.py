import logging
import os
import random

import vk_api as vk
from environs import Env
from telegram.ext import Updater
from vk_api.longpoll import VkLongPoll, VkEventType

from checked_result import TelegramLogsHandler
from d_f_handler import detect_intent_texts

logger = logging.getLogger()


def get_dialogue(event, vk_api, project_id):
    user_id = event.user_id
    text = event.text
    dialogue_flow_response = detect_intent_texts(text, project_id, user_id)
    reply_text = dialogue_flow_response.query_result.fulfillment_text
    is_fallback = dialogue_flow_response.query_result.intent.is_fallback
    if not is_fallback:
        vk_api.messages.send(
            user_id=user_id,
            message=reply_text,
            random_id=random.randint(1, 1000)
        )


def main():
    env = Env()
    env.read_env()

    vk_token = env.str("VK_TOKEN")
    telegram_logging_token = env.str("TELEGRAM_LOGGING_BOT_TOKEN")
    tg_user_id = env.str("TG_USER_ID")
    project_id = env.str("PROJECT_ID")
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id

    logger.setLevel(logging.INFO)
    logger_bot = Updater(telegram_logging_token).dispatcher.bot
    logger.addHandler(TelegramLogsHandler(logger_bot, tg_user_id))
    logger.info("VK Бот запущен!")

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    get_dialogue(event, vk_api, project_id)
        except Exception as e:
            logger.exception(f"Бот поддержки VK упал с ошибкой:\n")
            continue


if __name__ == '__main__':
    main()
