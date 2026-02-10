import subprocess
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GFPGAN = os.path.join(ROOT_DIR, "models", "GFPGAN", "inference_gfpgan.py")

def enhance_face(video_in, video_out):
    if not os.path.exists(GFPGAN):
        raise FileNotFoundError(
            f"GFPGAN inference script was not found at '{GFPGAN}'. "
            "Please install/copy GFPGAN into models/GFPGAN."
        )

    cmd = [
        "python", GFPGAN,
        "-i", video_in,
        "-o", video_out,
        "--upscale", "2"
    ]
    subprocess.run(cmd, check=True)
