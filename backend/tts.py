from TTS.api import TTS
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS("tts_models/en/vctk/vits")
tts.to(device)

# pick a default speaker (any valid one)
DEFAULT_SPEAKER = "p225"

def text_to_speech(text, output_wav):
    tts.tts_to_file(
        text=text,
        speaker=DEFAULT_SPEAKER,
        file_path=output_wav
    )
