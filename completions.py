from openai import OpenAI
from dotenv import load_dotenv


class Completions(object):
    def __init__(self) -> None:
        load_dotenv()
        self.client = OpenAI()
        self.messages = [
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        ]

    def send_message(self, message):
        self.messages.append({"role": "user", "content": message})
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )

        result = self.__sanitize_response(completion.choices[0].message.content)
        self.messages.append({"role": "assistant", "content": result})
        return result

    def __sanitize_response(self, response):
        return response.replace("\n", " ")