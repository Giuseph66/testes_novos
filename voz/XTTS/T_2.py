from TTS.api import TTS

# Inicializa o modelo
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", gpu=False)

# Texto a ser falado
texto = "Morty, você já ouviu falar de uma IA chamada Giuseph? Ela é insana, Morty!"

# Caminho para o áudio de referência
referencia = "rick.wav"

# Gera e salva o áudio
tts.tts_to_file(
    text=texto,
    speaker_wav=referencia,
    language="pt-br",
    file_path="saida_your_tts.wav"
)
print("✅ Áudio gerado com sucesso!")