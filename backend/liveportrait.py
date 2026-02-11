import subprocess
import os

def run_liveportrait(image_path, audio_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Use a default driving video from the model assets
    driving_video = "../models/LivePortrait/assets/examples/driving/d0.mp4"

    cmd = [
        "python",
        "../models/LivePortrait/inference.py",
        "-s", image_path,               # Corrected source flag
        "-d", driving_video,            # Corrected driving flag
        "-o", output_dir,               # Corrected output flag from your help text
        "--flag-force-cpu",             # FORCES CPU INFERENCE (Fixes the NVIDIA error)
        "--no-flag-use-half-precision", # Required for CPU stability
        "--flag-do-crop"                # Recommended flag from help text
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Subprocess failed: {e}")
        raise