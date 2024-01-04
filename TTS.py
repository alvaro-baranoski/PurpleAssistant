from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv


class TTS(object):
    def __init__(self) -> None:
        load_dotenv()
        self.client = OpenAI()

    def generate_audio_from_text(self, text):
        print("TTS")
        print("Received following text:")
        print(text)
        
        speech_file_path = Path(__file__).parent / "audios/response.mp3"
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )

        response.stream_to_file(speech_file_path)
        print("file saved successfully")
