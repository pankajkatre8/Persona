import subprocess
import os

def run_musetalk(image_path, audio_path, output_video):
    os.makedirs(os.path.dirname(output_video), exist_ok=True)

    cmd = [
        "python",
        "../models/MuseTalk/inference.py",
        "--source_image", image_path,
        "--audio", audio_path,
        "--output", output_video
    ]

    subprocess.run(cmd, check=True)
