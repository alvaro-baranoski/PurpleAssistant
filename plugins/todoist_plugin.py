class TodoistPlugin:
    def __init__(self) -> None:
        pass
    
    def handle(self, response):
        print("received response")
        print(response)
        return