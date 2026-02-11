import uuid
import os
import subprocess
from tts import text_to_speech
from musetalk import run_musetalk  # CHANGED: Import MuseTalk instead of InfiniteTalk
from enhance import enhance_face

def generate_pipeline(script, avatar_path):
    job = str(uuid.uuid4())
    
    # Ensure directories exist
    os.makedirs("temp", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    audio = f"temp/{job}.wav"
    lipsynced = f"temp/{job}_lips.mp4"
    enhanced = f"temp/{job}_enhanced.mp4"
    final_video = f"outputs/{job}.mp4"

    print(f"--- Starting Job {job} ---")

    # 1. Generate Speech (TTS)
    print("1. Generating Audio...")
    text_to_speech(script, audio)

    # 2. Lip Sync (MuseTalk)
    # Using MuseTalk as it is more likely to run without specific GPU kernels compared to xfuser
    print("2. Running Lip Sync (MuseTalk)...")
    try:
        run_musetalk(avatar_path, audio, lipsynced)
    except Exception as e:
        print(f"MuseTalk Failed: {e}")
        raise

    # 3. Enhance Video Quality
    print("3. Enhancing Face...")
    enhance_face(lipsynced, enhanced)

    # 4. Final Merge: Audio + Video
    print("4. Merging Audio...")
    cmd = [
        "ffmpeg", "-y",           
        "-i", enhanced,           
        "-i", audio,              
        "-c:v", "copy",           
        "-c:a", "aac",            
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",              
        final_video
    ]
    subprocess.run(cmd, check=True)

    print(f"--- Job Complete: {final_video} ---")
    return final_video