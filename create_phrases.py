import argparse
import json

from environs import Env
from google.api_core.exceptions import InvalidArgument
from google.cloud import dialogflow
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def specify_path_file():
    parser = argparse.ArgumentParser(
        description='Скрипт для обучения новым фразам'
    )
    parser.add_argument('filename', help='path to file', nargs='?', type=str, default='questions.json')
    args = parser.parse_args()
    return args.filename


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def open_file(path):
    with open(path, "r", encoding="UTF-8") as my_file:
        file_contents = my_file.read()

    training_phrases = json.loads(file_contents)
    return training_phrases


def main():
    env = Env()
    env.read_env()
    project_id = env.str("PROJECT_ID")

    path = specify_path_file()
    training_phrases = open_file(path)
    for intent, phrase in training_phrases.items():
        questions, answer = phrase.values()
        try:
            create_intent(project_id, intent, questions, (answer,))
        except InvalidArgument as error:
            logging.error(error)
            continue


if __name__ == '__main__':
    main()
