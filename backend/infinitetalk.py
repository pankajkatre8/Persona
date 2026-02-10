import subprocess

IT = "../models/InfiniteTalk/inference.py"

def run_infinitetalk(video_in, audio, video_out):
    cmd = [
        "python", IT,
        "--video", video_in,
        "--audio", audio,
        "--output", video_out
    ]
    subprocess.run(cmd, check=True)
