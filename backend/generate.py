import uuid
from tts import text_to_speech
from musetalk import run_musetalk
from liveportrait import run_liveportrait

def generate_pipeline(script, avatar_path):
    uid = str(uuid.uuid4())

    audio = f"temp/{uid}.wav"
    driving_video = f"temp/{uid}_talk.mp4"
    lp_dir = f"outputs/{uid}"

    # 1. TEXT → AUDIO
    text_to_speech(script, audio)

    # 2. AUDIO → TALKING VIDEO (MuseTalk)
    run_musetalk(avatar_path, audio, driving_video)

    # 3. TALKING VIDEO → REFINED VIDEO (LivePortrait)
    run_liveportrait(avatar_path, driving_video, lp_dir)

    # Final output
    return f"/outputs/{uid}/result.mp4"
