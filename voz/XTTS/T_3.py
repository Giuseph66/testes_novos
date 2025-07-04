from TTS.api import TTS

# Inicializa o modelo
tts = TTS(model_name="tts_models/en/multi-dataset/tortoise-v2", gpu=False)

# Texto em inglês
text = "Morty, did you hear about this crazy AI called Giuseph? It's insane!"

# Áudio de referência
reference = "rick.wav"

# Gera e salva
tts.tts_to_file(
    text=text,
    speaker_wav=reference,
    file_path="saida_tortoise.wav"
)
print("✅ Audio generated successfully with Tortoise!")