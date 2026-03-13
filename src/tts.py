import subprocess
import uuid
from pathlib import Path

# Root of the project
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Audio output folder
AUDIO_DIR = PROJECT_ROOT / "generated_audio"
AUDIO_DIR.mkdir(exist_ok=True)

# Piper paths (to make sure the user has piper on their system with the folder)
PIPER_DIR = PROJECT_ROOT / "piper"
PIPER_EXE = PIPER_DIR / "piper.exe"
PIPER_MODEL = PIPER_DIR / "en_US-lessac-high.onnx"


def generate_speech(text: str) -> str:
    text = text.strip()

    if not text:
        raise ValueError("No text provided for speech generation.")
    #where to save the audio clips to
    output_path = AUDIO_DIR / f"output_{uuid.uuid4()}.wav"

    result = subprocess.run(
        [
            str(PIPER_EXE),
            "--model",
            str(PIPER_MODEL),
            "--output_file",
            str(output_path),
        ],
        input=text,
        text=True,
        capture_output=True,
    )
    #adding handling for if Piper can't run for some reason
    if result.returncode != 0:
        raise RuntimeError(f"Piper failed:\n{result.stderr}")

    return str(output_path.resolve())