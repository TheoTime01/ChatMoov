"""
Analyze an audio file and send the data to the Arduino
"""

import numpy as np
import librosa
import serial

class AudioSerialAnalyzer:
    def __init__(self, audio_file_path="audio.mp3", com_port="COM5"):
        """
        Initialize the AudioSerialAnalyzer
        :param audio_file_path: Path to the audio file to analyze
        :param com_port: COM port to use to send the data to the Arduino
        :return: None
        """
        self.audio_file_path = audio_file_path
        self.com_port = com_port
        self.ser = serial.Serial(self.com_port, 9600,timeout=1)

    def analyze_and_send(self):
        """
        Analyze the audio file and send the data to the Arduino
        :return: None
        """

        # Charger le fichier audio MP3
        signal, fs = librosa.load(self.audio_file_path)

        # On normalise le signal
        signal = signal / np.max(np.abs(signal))

        #mettre signal au carré
        signal = signal ** 2

        #racine carrée du signal
        signal = np.sqrt(signal)

        # conversion des valeurs de signal avec l'equation y = 130x+50
        signal_2 = 130 * signal + 50

        # Obtenir la durée du signal en secondes
        duration = len(signal_2) / fs

        # Créer un tableau de temps correspondant au signal audio
        time = np.arange(0, duration, 1/fs)

        # Calculer la durée du signal
        t = time[-1] - time [0]

        # Defini une liste
        my_list = signal_2.tolist()     

        # Convert the list to a string
        list_string = ','.join(str(i) for i in my_list)

        list_send = list_string.encode()

        # Send the string to Arduino
        self.ser.write(list_send)

        time.sleep(0.1)


if __name__ == "__main__":
    audio_serial_analyzer = AudioSerialAnalyzer()
    audio_serial_analyzer.analyze_and_send()