import json


class JsonHandlerPlugin:
    @staticmethod
    def handle(json_string):
        try:
            json_data = json.loads(json_string)
            return json_data["end_session"]
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
