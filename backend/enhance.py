import subprocess
import os
import shutil

GFPGAN_SCRIPT = "../models/GFPGAN/inference_gfpgan.py"

def enhance_face(video_in, video_out):
    # Create a temporary folder for GFPGAN output
    temp_dir = f"temp/gfpgan_{os.path.basename(video_in)}"
    os.makedirs(temp_dir, exist_ok=True)
    
    video_in = os.path.abspath(video_in)
    
    cmd = [
        "python", GFPGAN_SCRIPT,
        "-i", video_in,
        "-o", temp_dir,   # GFPGAN needs a FOLDER, not a file
        "-v", "1.3",      # Version 1.3 is standard
        "-s", "2",        # Upscale factor
        "--bg_upsampler", "realesrgan"
    ]
    
    print("Running GFPGAN enhancement...")
    subprocess.run(cmd, check=True)

    # GFPGAN outputs results deeply nested or with suffixes.
    # We need to find the generated mp4 and move it to our target path.
    found_video = None
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file.endswith(".mp4"):
                found_video = os.path.join(root, file)
                break
        if found_video: break
    
    if found_video:
        shutil.move(found_video, video_out)
        shutil.rmtree(temp_dir) # Cleanup temp folder
    else:
        raise FileNotFoundError("GFPGAN finished but no output video was found.")