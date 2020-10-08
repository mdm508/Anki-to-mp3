import librosa
import soundfile as sf

y, sr = librosa.load("test_song.mp3")
y_slow = librosa.effects.time_stretch(y, 0.6)
sf.write("slow_wav.mp3", y_slow, sr, format="WAV")



