from bark.api import generate_audio
from bark.generation import preload_models, SAMPLE_RATE
import scipy.io.wavfile as wavfile
import numpy as np

# Texto no estilo Rick Sanchez
texto = "Ugh... sério isso, Morty? Eu paguei... tipo... um rim nesse iPhone, e ele... nem APK instala?!"

# Preload dos modelos (importante)
preload_models()

# Geração do áudio
audio = generate_audio(texto)

# Salvando como arquivo .wav
audio_int16 = np.int16(audio * 32767)
wavfile.write("estilo_rick.wav", SAMPLE_RATE, audio_int16)

print("✅ Áudio gerado com sucesso: estilo_rick.wav")
