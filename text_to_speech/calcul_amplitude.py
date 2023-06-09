import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

def normalize_audio(signal):
    # Calculate the maximum amplitude
    max_amp = np.max(np.abs(signal))
    # Normalize the signal
    normalized_signal = signal / max_amp

    return normalized_signal

# Load the audio file
sample_rate, audio_data = wav.read('audio.wav')

# Obtenir la durée du signal en secondes
duration = len(audio_data) / sample_rate

# Créer un tableau de temps correspondant au signal audio
time = np.arange(0, duration, 1/sample_rate)

# Normalize the audio signal
normalized_audio = normalize_audio(audio_data)



print("Normalized audio signal:")
print(normalized_audio)

print("\nMain amplitudes:")
print(main_amplitudes)

# Display the normalize signal and the signal on se same figure
plt.figure(figsize=(10, 4))
plt.plot(time, normalized_audio, color='b', label='Normalized signal')
plt.plot(main_amplitudes, color='r', label='Signal')
plt.xlabel('Temps (s)')
plt.ylabel('Amplitude')
plt.title('Signal audio')
plt.grid(True)
plt.legend()
plt.show()