import os
import sys
import soundfile as sf
import sounddevice as sd
import queue
import numpy as np
from time import sleep
from pathlib import Path
from audio_analysis import AudioAnalysis
from speech_to_text import SpeechToText
from text_to_speech import TextToSpeech
from completions import Completions


class Recording(object):
    def __init__(self) -> None:
        self.speaking_status = "not speaking"
        self.stop_recording_flag = False
        self.q = queue.Queue()
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.completions = Completions()
        self.audio_analysis = AudioAnalysis()
        self.audio_file = Path(__file__).parent / "assets/audios/input.mp3"
        self.channels = 2
        self.samplerate = 44100
        self.silence_threshold = 0.001

    def __start_stop_recording(self, indata):
        rms = np.sqrt(np.mean(indata**2))

        if rms > self.silence_threshold:
            if self.speaking_status == "not speaking":
                self.speaking_status = "speaking"
                print("started speaking!")

        elif self.speaking_status == "speaking":
            self.speaking_status = "not speaking"
            print("stopped speaking!")
            sleep(1)
            self.stop_recording_flag = True
            
            if not self.audio_analysis.has_human_voice(self.audio_file):
                sleep(1)
                # self.start_recording()
                return

            transcript = self.stt.transcript_audio_file(self.audio_file)
            response = self.completions.send_message(transcript)
            response_audio_file = self.tts.generate_audio_from_text(response)
            self.__read_aloud_audio_file(response_audio_file)

    def start_recording(self):
        if os.path.exists(self.audio_file):
            os.remove(self.audio_file)

        with sf.SoundFile(self.audio_file, mode="x", samplerate=self.samplerate, channels=self.channels) as file:
            with sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=self.__callback):
                print('#' * 80)
                print('press Ctrl+C to stop the recording')
                print('#' * 80)
                while True:
                    file.write(self.q.get())
                    print(self.q.get())
                    if self.stop_recording_flag:
                        print("breaking")
                        break

    def __callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(indata.copy())

        self.__start_stop_recording(indata)

    def __read_aloud_audio_file(self, response_audio_file):
        data, fs = sf.read(response_audio_file, dtype='float32')
        sd.play(data, fs)
        sd.wait()
