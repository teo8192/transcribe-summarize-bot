import azure.cognitiveservices.speech as speechsdk

import config
import time

class BinaryFileReaderCallback(speechsdk.audio.PullAudioInputStreamCallback):
    def __init__(self, filename: str):
        super().__init__()
        self._file_h = open(filename, "rb")

    def read(self, buffer: memoryview) -> int:
        # print('trying to read {} frames'.format(buffer.nbytes))
        try:
            size = buffer.nbytes
            frames = self._file_h.read(size)

            buffer[:len(frames)] = frames
            # print('read {} frames'.format(len(frames)))

            return len(frames)
        except Exception as ex:
            print('Exception in `read`: {}'.format(ex))
            raise

    def close(self) -> None:
        # print('closing file')
        try:
            self._file_h.close()
        except Exception as ex:
            print('Exception in `close`: {}'.format(ex))
            raise

def compressed_stream_helper(compressed_format, mp3_file_path, default_speech_auth):
    callback = BinaryFileReaderCallback(mp3_file_path)
    stream = speechsdk.audio.PullAudioInputStream(stream_format=compressed_format, pull_stream_callback=callback)

    speech_config = speechsdk.SpeechConfig(**default_speech_auth)
    speech_config.speech_recognition_language=config.LANGUAGE
    audio_config = speechsdk.audio.AudioConfig(stream=stream)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    result = []

    def recognized(evt):
        print('RECOGNIZED: {}'.format(evt))
        nonlocal result
        result.append(evt.result.text)

    # Connect callbacks to the events fired by the speech recognizer
    # speech_recognizer.recognizing.connect(lambda evt: pass)
    speech_recognizer.recognized.connect(recognized)
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()

    return result

def pull_audio_input_stream_compressed_mp3(mp3_file_path: str,
        default_speech_auth):
    # Create a compressed format
    compressed_format = speechsdk.audio.AudioStreamFormat(compressed_stream_format=speechsdk.AudioStreamContainerFormat.MP3)
    return compressed_stream_helper(compressed_format, mp3_file_path, default_speech_auth)

def recognize_from_file(filename: str) -> list[str]:
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_auth = { "subscription": config.SPEECH_KEY, "region": config.SPEECH_REGION }
    return pull_audio_input_stream_compressed_mp3(filename, speech_auth)

if __name__ == "__main__":
    testfile = "./recordings/"
    text = recognize_from_file(testfile)
    print("\n".join(text))
