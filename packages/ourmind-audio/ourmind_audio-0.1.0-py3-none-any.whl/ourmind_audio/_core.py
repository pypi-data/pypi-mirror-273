from __future__ import annotations
from pathlib import Path
import subprocess
import json
import numpy as np
import tempfile
from logging import getLogger
from numpy.typing import NDArray

logger = getLogger(__name__)


def _convert_16kHz_wav(input_path: Path, output_path: Path) -> None:
    """
    Processes an audio file using ffmpeg to the specified output format.

    Args:
    - input_path: Path to the input audio file.
    - output_path: Path to the output audio file.

    Raises:
    - subprocess.CalledProcessError if the ffmpeg command fails.
    """
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-ac",
        "1",
        "-ar",
        "16000",
        "-acodec",
        "pcm_s16le",
        str(output_path),
    ]

    subprocess.run(cmd, check=True)


def _is_audio_16kHz_wav(file_path: Path) -> bool:
    """
    Checks if the audio file is in the desired format.

    Desired format:
    - Sample rate: 16000 Hz
    - Channels: Mono (1 channel)
    - Codec: pcm_s16le

    Args:
    - file_path: Path to the audio file.

    Returns:
    - True if the audio is in the desired format, False otherwise.
    """
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "a:0",
        "-show_entries",
        "stream=sample_rate,channels,codec_name",
        "-of",
        "json",
        str(file_path),
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        audio_data = data.get("streams", [{}])[0]
        sample_rate = int(audio_data.get("sample_rate", 0))
        channels = int(audio_data.get("channels", 0))
        codec_name = audio_data.get("codec_name", "")

        return sample_rate == 16000 and channels == 1 and codec_name == "pcm_s16le"
    except subprocess.CalledProcessError:
        logger.exception("failed to run ffmpeg")
        return False


def _file2array(file_path: Path) -> NDArray[np.float32]:
    with open(file_path, "rb") as f:
        audio_content = f.read()
    audio = (
        np.frombuffer(audio_content, np.int16).flatten().astype(np.float32) / 32768.0
    )
    return audio


def process_audio_file(file_path: Path) -> NDArray[np.float32]:
    is_wav = file_path.suffix.lower() == ".wav"
    is_correct_format = _is_audio_16kHz_wav(file_path) if is_wav else False

    # If it's a WAV file and already in the correct format, return the array
    if is_wav and is_correct_format:
        return _file2array(file_path)

    # Otherwise, convert to the correct format
    output_path = Path(tempfile.mktemp(suffix=".wav"))
    _convert_16kHz_wav(file_path, output_path)
    return _file2array(output_path)


WEBM_SIGNATURE = b"\x1a\x45\xdf\xa3"
SIGNATURE_LENGTH = len(WEBM_SIGNATURE)


def _find_webm_start(file_path: Path) -> int:
    with file_path.open("rb") as file:
        offset = 0

        while True:
            buffer = file.read(SIGNATURE_LENGTH)
            if len(buffer) < SIGNATURE_LENGTH:
                break

            if buffer == WEBM_SIGNATURE:
                return offset

            file.seek(offset + 1)
            offset += 1

    return -1  # Signature not found


def _repair_webm_file_at_index(
    input_file: Path, output_file: Path, start_index: int
) -> None:
    with input_file.open("rb") as file:
        file.seek(start_index)
        signature = file.read(SIGNATURE_LENGTH)

        if signature != WEBM_SIGNATURE:
            raise ValueError(
                f"No WebM signature found at the given index: {start_index}"
            )

        file.seek(start_index)
        webm_data = file.read()

    with output_file.open("wb") as file:
        file.write(webm_data)


def search_and_repair_webm_file(input_file: Path, output_file: Path) -> None:
    start_index = _find_webm_start(input_file)

    if start_index == -1:
        raise ValueError("WebM signature not found in the file.")

    _repair_webm_file_at_index(input_file, output_file, start_index)
