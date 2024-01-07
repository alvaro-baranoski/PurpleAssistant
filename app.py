from flask import Flask
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter

from handlers.launch_request_handler import LaunchRequestHandler
from handlers.hello_world_intent_handler import HelloWorldIntentHandler
from handlers.help_intent_handler import HelpIntentHandler
from handlers.cancel_and_stop_intent_handler import CancelAndStopIntentHandler
from handlers.session_ended_request_handler import SessionEndedRequestHandler
from handlers.all_exceptions_handler import AllExceptionHandler
from handlers.gpt_query_intent_handler import GptQueryIntentHandler

app = Flask(__name__)
skill_builder = SkillBuilder()


skill_builder.add_request_handler(LaunchRequestHandler())
skill_builder.add_request_handler(HelloWorldIntentHandler())
skill_builder.add_request_handler(GptQueryIntentHandler())
skill_builder.add_request_handler(HelpIntentHandler())
skill_builder.add_request_handler(CancelAndStopIntentHandler())
skill_builder.add_request_handler(SessionEndedRequestHandler())

skill_builder.add_exception_handler(AllExceptionHandler())


skill_adapter = SkillAdapter(
    skill=skill_builder.create(),
    skill_id="amzn1.ask.skill.5768a355-9c15-4614-8cbd-50c4d8febc77", 
    app=app)


@app.route("/", methods=["GET", "POST"])
def invoke_skill():
    return skill_adapter.dispatch_request()


if __name__ == '__main__':
    app.run(debug=True)
