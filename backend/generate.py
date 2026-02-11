import uuid
import os
from tts import text_to_speech
from liveportrait import run_liveportrait
from infinitetalk import run_infinitetalk
from enhance import enhance_face

def generate_pipeline(script, avatar_path):
    job = str(uuid.uuid4())
    
    audio = f"temp/{job}.wav"
    lp_dir = f"temp/{job}_lp"
    lipsynced = f"temp/{job}_lips.mp4"
    final_video = f"outputs/{job}.mp4"

    # 1. Generate Speech
    text_to_speech(script, audio)

    # 2. Generate Base Face Motion
    run_liveportrait(avatar_path, audio, lp_dir)
    
    # Locate the generated video from LivePortrait
    base_video = next(
        os.path.join(lp_dir, f) 
        for f in os.listdir(lp_dir) 
        if f.endswith(".mp4")
    )

    # 3. Apply Lip Sync
    run_infinitetalk(base_video, audio, lipsynced)

    # 4. Enhance Video Quality
    enhance_face(lipsynced, final_video)

    return final_video