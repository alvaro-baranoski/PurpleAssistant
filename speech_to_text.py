from openai import OpenAI
from dotenv import load_dotenv

class SpeechToText(object):
    def __init__(self) -> None:
        load_dotenv()
        self.client = OpenAI()

    def transcript_audio_file(self, file):
        audio_file = open(file, "rb")
        transcript = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )

        print("transcription done!")
        return transcript
