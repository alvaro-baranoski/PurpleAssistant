from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
import ask_sdk_core.utils as ask_utils
from openai import OpenAI
from plugins.handler_plugin import HandlerPlugin

import json

class GptQueryIntentHandler(AbstractRequestHandler):
    def __init__(self) -> None:
        self.end_session_flag = False
        self.client = OpenAI()
        self.handler_plugin = HandlerPlugin()
        with open("assets\introduction.txt") as f:
            self.assistant_description = f.read()
        super().__init__()

    """Handler for Gpt Query Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GptQueryIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        query = handler_input.request_envelope.request.intent.slots["query"].value

        session_attr = handler_input.attributes_manager.session_attributes
        chat_history = session_attr["chat_history"]
        response = self.generate_gpt_response(chat_history, query)
        session_attr["chat_history"].append((query, response))

        return (
            handler_input.response_builder
            .speak(response)
            .ask("Any other questions?")
            .set_should_end_session(self.end_session_flag)
            .response
        )

    def generate_gpt_response(self, chat_history, new_question):
        try:
            messages = [
                {"role": "system", "content": self.assistant_description}]
            for question, answer in chat_history[-10:]:
                messages.append({"role": "user", "content": question})
                messages.append({"role": "assistant", "content": answer})
            messages.append({"role": "user", "content": new_question})
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                response_format={ "type": "json_object" },
                messages=messages,
                max_tokens=600,
                n=1,
                temperature=0.5
            )
            result = self.parse_gpt_response(
                response.choices[0].message.content)
            return result
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def parse_gpt_response(self, response_json):
        try:
            result = json.loads(response_json)
            self.end_session_flag = result["end_session"]
            self.handler_plugin.handle(result)
            return result["response"]
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
