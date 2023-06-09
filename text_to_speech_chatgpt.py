"""
This script is used to run the chatbot using the GPT API and text to speech conversion
"""

from gtts import gTTS
from playsound import playsound
import os
import queue
import threading
import openai
import librosa
from API.api import GPT_API

class AudioSerialAnalyzer:
    def __init__(self, audio_file_path="audio.mp3", com_port="COM5"):
        self.audio_file_path = audio_file_path
        self.com_port = com_port

    def analyze_and_send(self):
        ser = serial.Serial(self.com_port, 128000)

        # Charger le fichier audio MP3
        signal, fs = librosa.load(self.audio_file_path)

        # Obtenir la durée du signal en secondes
        duration = len(signal) / fs

        # Créer un tableau de temps correspondant au signal audio
        time = np.arange(0, duration, 1/fs)

        for amp, t in zip(signal, time):
            if amp == 0:
                ser.write(((str(0) + "!").encode()))
            else:
                ser.write(((str(1) + "!").encode()))

class AudioPlayer:
    def __init__(self):
        """
        Initialize the audio queue
        """

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
        """
        Initialize the audio player
        :param audio_player: AudioPlayer object
        """
        
        self.audio_player = audio_player
        self._messages:list = []

    def convert_text_audio(self, text:str):
        """
        Convert text to audio

        :param text: text to be converted
        :return: None
        """
        try:
            # Language in which you want to convert
            language:str = 'fr'

            # Passing the text and language to the engine
            myobj = gTTS(text=text, lang=language, slow=False)

            # Saving the converted audio in an mp3 file named "audio"
            myobj.save("audio.mp3")
        except Exception as e:
            raise ValueError("\nError converting text to audio: " + str(e))

    def process_user_input(self, user_input):
        """
        Process the user input and generate a response
        :param user_input: user input
        :return: None
        """

        self._messages.append({"role": "user", "content": user_input})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self._messages,
            max_tokens=2000,
            temperature=0.2
        )

        chat_response:str = completion.choices[0].message.content
        print(f'ChatGPT: {chat_response}')
        self._messages.append({"role": "assistant", "content": chat_response})

        # Create separate threads to save and play the audio
        t1 = threading.Thread(target=self.convert_text_audio, args=(chat_response,))
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
        # os.remove("audio.mp3")

        # When the length of messages is equal to 4, remove the two first elements
        if len(self._messages) == 4:
            self._messages.pop(0)
            self._messages.pop(0)
        else:
            pass


class ChatGPT_Text_to_Speech:
    def __init__(self,):
        """
        Initialize the GPT API
        """
        self._gpt = GPT_API()
        self._gpt.init_api()
        self._input_user:str = ""

    def run_chat(self):
        """
        Run the chatbot
        :return: None
        """

        #verifie the existence of answer.json
        with open("answer.txt",'r') as f:
            self._input_user = f.read().strip()

        # Initialize the conversation messages list
        messages = []

        # Create an instance of the AudioPlayer class
        audio_player = AudioPlayer()

        # Create an instance of the TextToSpeechConverter class
        text_to_speech_converter = TextToSpeechConverter(audio_player)

        try:
            text_to_speech_converter.process_user_input(self._input_user)

        except KeyboardInterrupt:
            print("Exiting...")

        except Exception as e:
            print("\nAn error occurred:", str(e))


if __name__ == "__main__":
    chat = ChatGPT_Text_to_Speech()
    chat.run_chat()