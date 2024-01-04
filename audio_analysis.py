import librosa
import numpy as np

class AudioAnalysis(object):
    def __init__(self) -> None:
        pass
    
    def has_human_voice(self, file_path, threshold=0.0004):
        # Load the audio file
        audio_data, sr = librosa.load(file_path)

        # Extract the Mel-frequency cepstral coefficients (MFCCs)
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sr)

        # Calculate the mean energy along the time axis
        energy = np.mean(librosa.feature.rms(y=audio_data))

        # Use a simple threshold for voice detection
        if energy > threshold:
            print("Speech detected.")
            return True
        else:
            print("No speech detected.")
            return False