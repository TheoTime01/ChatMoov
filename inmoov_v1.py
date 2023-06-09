"""
This is the main program for the InMoov robot. It launches the face detector
"""
import subprocess
import signal
import os

processes = []  # Store references to the launched processes

def launch_program(command):
    """
    Launch a program in a subprocess
    """
    process = subprocess.Popen(["env_inmoov/Scripts/python.exe", command])
    processes.append(process)

def signal_handler(sig, frame):
    """
    Signal handler for SIGINT
    """
    print("Program interrupted. Terminating launched processes...")
    for process in processes:
        process.terminate()
    os.kill(os.getpid(), signal.SIGINT)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Launch face_detector.py
launch_program("face_detector.py")

# Launch conversation.py
launch_program("conversation.py")
