import subprocess

GFPGAN = "../models/GFPGAN/inference_gfpgan.py"

def enhance_face(video_in, video_out):
    cmd = [
        "python", GFPGAN,
        "-i", video_in,
        "-o", video_out,
        "--upscale", "2"
    ]
    subprocess.run(cmd, check=True)
