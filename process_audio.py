import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# 🔊 Load your audio file (works for .mp3 or .wav)
file_path = "static/sounds/goro_goro.mp3"  # or .wav
y, sr = librosa.load(file_path, sr=22050)  # Resample to 22,050 Hz

# ✂️ Trim leading/trailing silence
y, _ = librosa.effects.trim(y)

# 📈 Normalize volume
y = y / np.max(np.abs(y))

plt.figure(figsize=(14, 5))
librosa.display.waveshow(y, sr=sr)
plt.title("Waveform")
plt.show()

# 🔍 Generate Spectrogram
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

plt.figure(figsize=(14, 5))
librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
plt.title('Spectrogram (dB)')
plt.colorbar(format='%+2.0f dB')
plt.tight_layout()
plt.show()

mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
print("MFCC shape:", mfccs.shape)

plt.figure(figsize=(10, 4))
librosa.display.specshow(mfccs, x_axis='time')
plt.colorbar()
plt.title('MFCC')
plt.tight_layout()
plt.show()
np.save("features/goro_goro_mfcc.npy", mfccs)
