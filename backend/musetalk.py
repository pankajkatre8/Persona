import subprocess
import os


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSETALK_SCRIPT = os.path.join(ROOT_DIR, "models", "MuseTalk", "inference.py")

def run_musetalk(image_path, audio_path, output_video):
    os.makedirs(os.path.dirname(output_video), exist_ok=True)

    if not os.path.exists(MUSETALK_SCRIPT):
        raise FileNotFoundError(
            f"MuseTalk inference script was not found at '{MUSETALK_SCRIPT}'. "
            "Please install/copy MuseTalk into models/MuseTalk."
        )

    cmd = [
        "python",
        MUSETALK_SCRIPT,
        "--source_image", image_path,
        "--audio", audio_path,
        "--output", output_video
    ]

    subprocess.run(cmd, check=True)
