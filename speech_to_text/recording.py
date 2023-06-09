import pyaudio
import wave
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

class Recording:
    def __init__(self, threshold=0.01, chunk_size=1024, format=pyaudio.paInt16,
                 channels=1, rate=44100, max_duration=10):
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
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def save_as_wav(self, filename):
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
        try:
            r = Recording()
            r.start()
            r.stop()
            r.save_as_wav("audio.wav")
        except ValueError as ve:
            logging.error(ve)
        except Exception as e:
            logging.error("An error occurred: " + str(e))


if __name__ == "__main__":
    r = Recording()
    r.run()


