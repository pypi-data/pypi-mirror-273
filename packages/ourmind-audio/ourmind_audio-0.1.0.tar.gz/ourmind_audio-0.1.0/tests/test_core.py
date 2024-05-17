from __future__ import annotations
import pytest
from pathlib import Path
from ourmind_audio._core import _convert_16kHz_wav, _is_audio_16kHz_wav
import tempfile

# Set the path to the example audio files
EXAMPLE_AUDIO_PATH = Path(__file__).parent / "example_audio" / "jfk"


def get_example_audio_files():
    """Helper function to retrieve all audio files from the example audio directory."""
    return [file for file in EXAMPLE_AUDIO_PATH.iterdir() if file.is_file()]


@pytest.mark.parametrize("audio_file", get_example_audio_files())
def test_convert_16kHz_wav(audio_file):
    temp_path = Path(tempfile.mktemp(suffix=".wav"))

    _convert_16kHz_wav(audio_file, temp_path)
    assert _is_audio_16kHz_wav(temp_path)

    # if temp_path.exists():
    #    temp_path.unlink()


@pytest.mark.parametrize("audio_file", get_example_audio_files())
def test_audio_format(audio_file):
    """
    Test that the _is_audio_16kHz_wav function correctly identifies audio files that are not in the desired format.
    """

    # Skip if contains the string "conv_16k_mono.wav"

    if "conv_16k_mono.wav" not in str(audio_file):
        assert not _is_audio_16kHz_wav(audio_file)
