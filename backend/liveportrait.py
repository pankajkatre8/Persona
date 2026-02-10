import subprocess
import os


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVEPORTRAIT_SCRIPT = os.path.join(ROOT_DIR, "models", "LivePortrait", "inference.py")

def run_liveportrait(source_image, driving_video, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(LIVEPORTRAIT_SCRIPT):
        raise FileNotFoundError(
            f"LivePortrait inference script was not found at '{LIVEPORTRAIT_SCRIPT}'. "
            "Please install/copy LivePortrait into models/LivePortrait."
        )

    cmd = [
        "python",
        LIVEPORTRAIT_SCRIPT,
        "--source", source_image,
        "--driving", driving_video,
        "--output-dir", output_dir,
        "--flag-force-cpu"
    ]

    subprocess.run(cmd, check=True)
