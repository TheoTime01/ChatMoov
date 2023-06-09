"""
This module contains the Speech_To_Text class, which is used to convert audio to text
"""

import openai
import wave
import logging
import numpy as np
import pyaudio
import os
from API.api import GPT_API
import json

logging.basicConfig(level=logging.INFO)

class Recording:
    def __init__(self, threshold=0.01, chunk_size=1024, format=pyaudio.paInt16,
                 channels=1, rate=44100, max_duration=6):
        """
        :param threshold: minimum amplitude to trigger recording
        :param chunk_size: number of samples to read at a time
        :param format: audio format (check pyaudio docs)
        :param channels: number of audio channels
        :param rate: sampling frequency
        :param max_duration: maximum duration of the recording
        """

        self.threshold = threshold
        self.chunk_size = chunk_size
        self.format = format
        self.channels = channels
        self.rate = rate
        self.max_duration = max_duration
        self.frames = []
        self.recording_started = False

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk_size)

    def start(self):
        """
        Start recording
        :return: None
        """
        logging.info("Listening...")

        while True:
            data = self.stream.read(self.chunk_size)
            audio_np = np.frombuffer(data, dtype=np.int16)
            amplitude = np.abs(audio_np).mean()

            if amplitude > self.threshold and not self.recording_started:
                logging.info("Recording started.")
                self.recording_started = True

            if self.recording_started:
                self.frames.append(data)

            if self.recording_started and (
                    len(self.frames) * self.chunk_size) >= (self.rate * self.max_duration) or (
                    self.recording_started and amplitude < self.threshold):
                logging.info("Recording stopped.")
                break

    def stop(self):
        """
        Stop recording
        :return: None
        """

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def save_as_wav(self, filename):
        """
        Save the recorded audio as a WAV file
        :param filename: name of the file
        :return: None
        """

        try:
            wf = wave.open(filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            logging.info("Audio saved as %s", filename)
        except Exception as e:
            raise ValueError("Error saving audio: " + str(e))

    def run(self):
        """
        Run the recording
        :return: None
        """

        try:
            r = Recording()
            r.start()
            r.stop()
            r.save_as_wav("audio.wav")
        except ValueError as ve:
            logging.error(ve)
        except Exception as e:
            logging.error("An error occurred: " + str(e))

class Speech_To_Text:
    def __init__(self, audio="audio.wav"):
        """
        Initialize the API

        :param audio: audio file to convert to text
        :return: None
        """
        self._audio = audio
        self._api = GPT_API()
        self._api.init_api()
        logging.info("api initialize correctly")


    def convert_audio_text(self):
        """
        Convert audio to text

        :return: answer of the api of openAI
        """
        try:
            audio_file:str = open(self._audio,"rb")
            transcript:str = openai.Audio.transcribe("whisper-1", audio_file)
            answer:str = transcript["text"]
            return answer
        except Exception as e:
            raise ValueError("\nError converting audio to text: " + str(e))

class GPT_Speech_to_Text:
    def __init__(self):
        """
        Initialize the API
        :return: None
        """

        self._recording = Recording()
        self._speech_to_text = Speech_To_Text()

    def run(self):
        """
        
        :return: answer of the api of openAI
        """
        
        try :
            self._recording.run()
            answer:str = self._speech_to_text.convert_audio_text()

            #write it in a json file
            with open("answer.txt", "w") as f:
                f.write(answer)
            return answer
        except Exception as e:
            raise ValueError("Error " + str(e))


if __name__ == "__main__":
    gpt_speech_to_text = GPT_Speech_to_Text()
    e=gpt_speech_to_text.run()



        