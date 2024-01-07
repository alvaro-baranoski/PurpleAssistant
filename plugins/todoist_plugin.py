import os
from todoist_api_python.api import TodoistAPI


class TodoistPlugin:
    def __init__(self) -> None:
        self.api = TodoistAPI(os.getenv("TODOIST_KEY"))
    
    def handle(self, response):
        self.api.add_task(
            content=response["body"]["content"],
            due_string=response["body"]["due_string"],
            project_id=self.parse_project_id(response["body"]["project"]))
        
        print("done!")
        return
    
    def parse_project_id(self, project_name):
        if project_name == "personal":
            return "2197462211"
        elif project_name == "professional":
            return "2293524139"
        elif project_name == "study":
            return "2221860189"
        else:
            pass