import uuid
import os
import subprocess
from tts import text_to_speech
from wav2lip import run_wav2lip
# from enhance import enhance_face  <-- 1. Comment out this import

def generate_pipeline(script, avatar_path):
    job = str(uuid.uuid4())
    
    # Ensure directories exist
    os.makedirs("temp", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    audio = f"temp/{job}.wav"
    lipsynced = f"temp/{job}_lips.mp4"
    # enhanced = f"temp/{job}_enhanced.mp4" <-- 2. Comment out enhanced path
    final_video = f"outputs/{job}.mp4"

    print(f"--- Starting Job {job} ---")

    # 1. TTS - Generate Audio
    print("1. Generating Audio...")
    text_to_speech(script, audio)

    # 2. Lip Sync (Wav2Lip)
    print("2. Running Lip Sync (Wav2Lip)...")
    run_wav2lip(avatar_path, audio, lipsynced)

    # 3. Enhance Video Quality (DISABLED FOR CPU/COMPATIBILITY)
    # print("3. Enhancing Face...")
    # enhance_face(lipsynced, enhanced)

    # 4. Final Merge: Audio + Video
    print("4. Merging Audio...")
    cmd = [
        "ffmpeg", "-y",           
        "-i", lipsynced,          # <--- 3. CHANGED: Use 'lipsynced' as input
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