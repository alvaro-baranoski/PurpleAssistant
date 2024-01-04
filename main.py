import argparse
from recording import Recording

parser = argparse.ArgumentParser(add_help=False)

try:
    recording = Recording()
    recording.start_recording()
except KeyboardInterrupt:
    print('\nRecording finished: ')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))