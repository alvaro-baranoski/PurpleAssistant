from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
import ask_sdk_core.utils as ask_utils
from dotenv import load_dotenv
from openai import OpenAI


class GptQueryIntentHandler(AbstractRequestHandler):
    def __init__(self) -> None:
        load_dotenv()
        self.client = OpenAI()
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
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=300,
                n=1,
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
