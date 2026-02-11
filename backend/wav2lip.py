import os
import subprocess
import sys
import shutil

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "../models")
W2L_DIR = os.path.join(MODELS_DIR, "Wav2Lip")
W2L_REPO_URL = "https://github.com/Rudrabha/Wav2Lip.git"

def setup_wav2lip():
    """Clones Wav2Lip and downloads the required weights automatically."""
    os.makedirs(MODELS_DIR, exist_ok=True)

    # 1. Clone Repo if missing
    if not os.path.exists(W2L_DIR):
        print(f"Downloading Wav2Lip to {W2L_DIR}...")
        subprocess.run(["git", "clone", W2L_REPO_URL, W2L_DIR], check=True)

    # 2. Download Main Model (Wav2Lip GAN)
    # Using a public mirror since the original GDrive link often fails
    model_path = os.path.join(W2L_DIR, "checkpoints/wav2lip_gan.pth")
    if not os.path.exists(model_path):
        print("Downloading Wav2Lip GAN Model...")
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        subprocess.run([
            "wget", "https://huggingface.co/camenduru/Wav2Lip/resolve/main/checkpoints/wav2lip_gan.pth",
            "-O", model_path
        ], check=True)

    # 3. Download Face Detector (Required dependency)
    detector_path = os.path.join(W2L_DIR, "face_detection/detection/sfd/s3fd.pth")
    if not os.path.exists(detector_path):
        print("Downloading Face Detector...")
        os.makedirs(os.path.dirname(detector_path), exist_ok=True)
        subprocess.run([
            "wget", "https://huggingface.co/camenduru/Wav2Lip/resolve/main/face_detection/detection/sfd/s3fd.pth",
            "-O", detector_path
        ], check=True)

def run_wav2lip(avatar_path, audio_path, output_path):
    """Runs the Wav2Lip inference."""
    setup_wav2lip()
    
    # Ensure absolute paths
    avatar_path = os.path.abspath(avatar_path)
    audio_path = os.path.abspath(audio_path)
    output_path = os.path.abspath(output_path)
    
    # Construct command
    # --resize_factor 2 reduces resolution for speed (use 1 for best quality)
    cmd = [
        sys.executable, "inference.py",
        "--checkpoint_path", "checkpoints/wav2lip_gan.pth",
        "--face", avatar_path,
        "--audio", audio_path,
        "--outfile", output_path,
        "--resize_factor", "1", 
        "--nosmooth"
    ]
    
    print("Running Wav2Lip Inference...")
    try:
        subprocess.run(cmd, cwd=W2L_DIR, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Wav2Lip Error: {e}")
        raise RuntimeError("Wav2Lip generation failed. Check logs.")