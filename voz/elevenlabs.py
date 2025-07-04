from elevenlabs import stream
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
    api_key="sk_e85f017bb513c9421f2cf1f5f4258da4593e23d5336b911e",
)

voice_id = "2EiwWnXFnvU5JabPnv8n"  # Clyde
model_id = "eleven_flash_v2_5"  # mais rápido e dinâmico

texto = """
Ugh... sério isso, Morty? Eu paguei... tipo... DUZENTOS anos de aluguel... nesse maldito iPhone, e ele... *argh*... nem APK instala?! Tipo... qual é, universo!?
"""

# Inicia o streaming
audio_stream = client.text_to_speech.stream(
    text=texto,
    voice_id=voice_id,
    model_id=model_id,
    output_format="mp3_44100_128"
)

# Reproduz localmente (opcional)
stream(audio_stream)

# Recomeça o streaming (é um generator, precisa ser recriado pra salvar)
audio_stream = client.text_to_speech.stream(
    text=texto,
    voice_id=voice_id,
    model_id=model_id,
    output_format="mp3_44100_128"
)

# Salva o áudio em disco
with open("voz_rick_style.mp3", "wb") as f:
    for chunk in audio_stream:
        if isinstance(chunk, bytes):
            f.write(chunk)

print("✅ Áudio salvo com sucesso como 'voz_rick_style.mp3'")
