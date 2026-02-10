import subprocess
import os

def run_liveportrait(image_path, audio_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    cmd = [
        "python",
        "../models/LivePortrait/inference.py",
        "--source", image_path,
        "--audio", audio_path,
        "--out_dir", output_dir,
        "--device", "cpu"
    ]

    subprocess.run(cmd, check=True)
