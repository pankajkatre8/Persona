import subprocess
import os

def run_liveportrait(source_image, driving_video, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    cmd = [
        "python",
        "../models/LivePortrait/inference.py",
        "--source", source_image,
        "--driving", driving_video,
        "--output-dir", output_dir,
        "--flag-force-cpu"
    ]

    subprocess.run(cmd, check=True)
