from gtts import gTTS
from playsound import playsound
import os
import queue
import threading
import logging

logging.basicConfig(level=logging.INFO)


class AudioPlayer:
    def __init__(self):
        self.audio_queue = queue.Queue()

    def play_audio(self, file_path):
        """
        Play the audio and signal completion

        :param file_path: path to the audio file
        :return: None
        """
        try:
            playsound(file_path)
        except Exception as e:
            raise ValueError("\nError playing audio: " + str(e))
        self.audio_queue.put(True)


class TextToSpeechConverter:
    def __init__(self, audio_player):
        self.audio_player = audio_player

    def convert_text_audio(self, text:str):
        """
        Convert text to audio

        :param text: text to be converted
        :return: None
        """
        try:
            # Language in which you want to convert
            language:str = 'ca'

            # Passing the text and language to the engine
            myobj = gTTS(text=text, lang=language, slow=False)

            # Saving the converted audio in an mp3 file named "audio"
            myobj.save("audio.mp3")
        except Exception as e:
            raise ValueError("\nError converting text to audio: " + str(e))

    def text_to_speech(self):
        while True:
            try:
                # The text that you want to convert to audio
                mytext:str = input("Sentence:\n")

                # Create separate threads to save and play the audio
                t1 = threading.Thread(target=self.convert_text_audio, args=(mytext,))
                t2 = threading.Thread(target=self.audio_player.play_audio, args=("audio.mp3",))

                # Start the threads
                t1.start()
                t1.join()

                t2.start()
                t2.join()

                # Wait for the audio to finish playing
                self.audio_player.audio_queue.get()
                self.audio_player.audio_queue.task_done()

                # Remove the audio file
                os.remove("audio.mp3")
            except KeyboardInterrupt:
                logging.info("\nExiting text_to_speech...")
                break
            except ValueError as ve:
                logging.error(ve)
            except Exception as e:
                logging.error("An error occurred: " + str(e))


# Create an instance of the AudioPlayer class
audio_player = AudioPlayer()

# Create an instance of the TextToSpeechConverter class
text_to_speech_converter = TextToSpeechConverter(audio_player)

# Call the text_to_speech method
text_to_speech_converter.text_to_speech()
