import noisereduce as nr
import librosa
import soundfile as sf

# Caminho para o seu áudio original
arquivo_entrada = "rick.wav"
arquivo_saida = "saida_sem_ruido.wav"

# Carrega o áudio
audio, sr = librosa.load(arquivo_entrada, sr=None)

# Aplica a redução de ruído
# Assume que os primeiros 0.5 segundos sejam apenas ruído (ajuste se necessário)
ruido_sample = audio[0:int(sr * 0.1)]  # 0.5 segundos de ruído
audio_limpo = nr.reduce_noise(y=audio, sr=sr, y_noise=ruido_sample)

# Salva o áudio limpo
sf.write(arquivo_saida, audio_limpo, sr)

print("✅ Redução de ruído concluída!")
