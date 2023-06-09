"""
This file is used to run the speech_to_text.py and text_to_speech_chatgpt.py files in parallel.
"""

import subprocess
import speech_to_text
import text_to_speech_chatgpt

STT = speech_to_text.GPT_Speech_to_Text()
TTS = text_to_speech_chatgpt.ChatGPT_Text_to_Speech()

while True:
    # Create subprocess for STT
    p1 = subprocess.Popen(['env_inmoov/Scripts/python.exe', 'speech_to_text.py'])
    p1.wait()

    # Create subprocess for TTS
    p2 = subprocess.Popen(['env_inmoov/Scripts/python.exe', 'text_to_speech_chatgpt.py'])
    p2.wait()

    # Both subprocesses finished
    print("Iteration completed!")
