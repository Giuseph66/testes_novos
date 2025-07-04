import torch.serialization

from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig

torch.serialization.add_safe_globals([
    XttsConfig,
    XttsAudioConfig,
    XttsArgs,
    BaseDatasetConfig
])

from TTS.api import TTS

tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

texto = "Oi minha vida linda, tudo bem? Eu te amo muito, você é a melhor coisa que já me aconteceu na vida. Você é a razão do meu sorriso, da minha felicidade. Eu te amo mais que tudo nesse mundo, você é tudo pra mim."
audio_base = "vida.wav"

tts.tts_to_file(
    text=texto,
    speaker_wav=audio_base,
    language="pt",
    file_path="vida_clone.wav"
)
