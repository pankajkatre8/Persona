import subprocess
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IT = os.path.join(ROOT_DIR, "models", "InfiniteTalk", "inference.py")

def run_infinitetalk(video_in, audio, video_out):
    if not os.path.exists(IT):
        raise FileNotFoundError(
            f"InfiniteTalk inference script was not found at '{IT}'. "
            "Please install/copy InfiniteTalk into models/InfiniteTalk."
        )

    cmd = [
        "python", IT,
        "--video", video_in,
        "--audio", audio,
        "--output", video_out
    ]
    subprocess.run(cmd, check=True)
