from openai import OpenAI
from dotenv import load_dotenv
from utils import Utils

class Completions(object):
    def __init__(self) -> None:
        load_dotenv()
        self.client = OpenAI()
        
        assistant_description = ""
        with open(f"{Utils.get_root_directory()}/assets/prompts/assistant_description.txt") as f:
            assistant_description = f.read()
        
        print(assistant_description)
        
        self.messages = [
            {"role": "system", "content": assistant_description},
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