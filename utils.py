from pathlib import Path

class Utils(object):
    def __init__(self) -> None:
        pass
        
    @staticmethod
    def get_root_directory():
        return Path(__file__).parent