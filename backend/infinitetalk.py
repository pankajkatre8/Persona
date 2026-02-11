import subprocess
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IT_SCRIPT = os.path.join(PROJECT_ROOT, "models", "InfiniteTalk", "generate_infinitetalk.py")
IT_PYTHON = os.environ.get(
    "INFINITETALK_PYTHON",
    os.path.join(PROJECT_ROOT, "venv-infinitetalk", "bin", "python"),
)

def run_infinitetalk(video_in, audio, video_out):
    # Use absolute paths to prevent "file not found" errors in subprocess
    video_in = os.path.abspath(video_in)
    audio = os.path.abspath(audio)
    video_out = os.path.abspath(video_out)

    if not os.path.exists(IT_PYTHON):
        raise FileNotFoundError(
            f"InfiniteTalk Python not found at {IT_PYTHON}. "
            "Set INFINITETALK_PYTHON to a valid interpreter path."
        )

    cmd = [
        IT_PYTHON, IT_SCRIPT,
        "--video", video_in,
        "--audio", audio,
        "--output", video_out
    ]
    
    print(f"Running InfiniteTalk command...")
    try:
        subprocess.run(cmd, check=True, cwd=PROJECT_ROOT)
    except subprocess.CalledProcessError as e:
        print(f"InfiniteTalk failed: {e}")
        raise
