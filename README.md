# Распознаем речь (бот-помощник)

В проекте представленны TG и VK боты, которые отвечают на самые распрастраненные 
вопросы через сервис [Dialogflow](https://cloud.google.com/dialogflow/docs).

## Как установить

Сперва склонируйте репозиторий:

~~~
git@github.com:kodunaiff/speech_recognition_for_TG.git
~~~

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:

 ~~~ 
 pip install -r requirements.txt 
 ~~~

## Переменное окружение

Создайте файл .env в корне проекта с таким содержимым:

~~~

PROJECT_ID = id проекта на Google Cloud

TELEGRAM_BOT_TOKEN = Токен от вашего ТГ-бота 

TELEGRAM_LOGGING_BOT_TOKEN = Токен от вашего ТГ-бота (для мониторинга ошибок)

TG_USER_ID = ваш Chat-id

VK_TOKEN = Токен от вашего VK -бота

GOOGLE_APPLICATION_CREDENTIALS = путь до файла credentials.json

~~~

## Пример запуска

~~~
python3 vk_bot.py

python3 tele_bot.py
~~~

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для 
веб-разработчиков [dvmn.org](https://dvmn.org/).





