from plugins.todoist_plugin import TodoistPlugin

class HandlerPlugin:
    def __init__(self) -> None:
        self.todoist_plugin = TodoistPlugin()
        pass
    
    def handle(self, response):
        if response["plugin"] == "todoist":
            self.todoist_plugin.handle(response)
            return
        elif response["plugin"] == "none":
            return
        else:
            return
