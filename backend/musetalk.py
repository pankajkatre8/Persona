import subprocess
import os
import sys
from pathlib import Path
import uuid

def get_musetalk_root() -> Path:
    backend_dir = Path(__file__).resolve().parent
    repo_root = backend_dir.parent
    return repo_root / "models" / "MuseTalk"

def get_musetalk_inference_script() -> Path:
    return get_musetalk_root() / "scripts" / "inference.py"

def _required_model_files(root: Path) -> list[Path]:
    return [
        root / "models" / "musetalkV15" / "unet.pth",
        root / "models" / "musetalkV15" / "musetalk.json",
        root / "models" / "whisper" / "config.json",
        root / "models" / "sd-vae" / "config.json",
    ]

def ensure_musetalk_available() -> Path:
    musetalk_root = get_musetalk_root()
    inference_script = get_musetalk_inference_script()

    if not inference_script.exists():
        raise FileNotFoundError(
            "MuseTalk inference script not found at: "
            f"{inference_script}. Please install MuseTalk under models/MuseTalk "
            "or update backend/musetalk.py to the correct script path."
        )

    missing_files = [str(p) for p in _required_model_files(musetalk_root) if not p.exists()]
    if missing_files:
        raise FileNotFoundError(
            "MuseTalk model files are missing. Run `bash models/MuseTalk/download_weights.sh` "
            "inside your backend venv. Missing files: "
            + ", ".join(missing_files)
        )

    return inference_script

def run_musetalk(image_path, audio_path, output_video):
    output_dir = os.path.dirname(output_video)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    inference_script = ensure_musetalk_available()
    musetalk_root = get_musetalk_root()
    image_abs = str(Path(image_path).resolve())
    audio_abs = str(Path(audio_path).resolve())

    # MuseTalk consumes a YAML task config.
    run_id = uuid.uuid4().hex
    inference_yaml = Path(output_dir or ".") / f"{run_id}_musetalk.yaml"
    inference_yaml.write_text(
        "task_0:\n"
        f" video_path: \"{image_abs}\"\n"
        f" audio_path: \"{audio_abs}\"\n",
        encoding="utf-8",
    )

    output_name = Path(output_video).name
    output_dir_abs = str(Path(output_dir or ".").resolve())

    cmd = [
        sys.executable,
        str(inference_script),
        "--inference_config", str(inference_yaml),
        "--result_dir", output_dir_abs,
        "--output_vid_name", output_name,
        "--version", "v15",
    ]
    try:
        subprocess.run(cmd, check=True, cwd=str(musetalk_root))
    finally:
        if inference_yaml.exists():
            inference_yaml.unlink()

    generated_video = Path(output_dir_abs) / "v15" / output_name
    if not generated_video.exists():
        raise FileNotFoundError(
            f"MuseTalk did not produce expected output video: {generated_video}"
        )

    target = Path(output_video)
    if generated_video.resolve() != target.resolve():
        generated_video.replace(target)
