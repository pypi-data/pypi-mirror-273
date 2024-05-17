#!/bin/bash

if ! command -v ffmpeg &> /dev/null
then
    echo "ffmpeg could not be found"
    exit
fi

# Check for input
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_audio_file>"
    exit 1
fi

# Input file
INPUT_FILE="$1"
BASENAME=$(basename -- "$INPUT_FILE")
FILENAME_NO_EXT="${BASENAME%.*}"

# Convert to various formats
ffmpeg -i "$INPUT_FILE" "${FILENAME_NO_EXT}_conv.aac"
ffmpeg -i "$INPUT_FILE" "${FILENAME_NO_EXT}_conv.alac"
ffmpeg -i "$INPUT_FILE" "${FILENAME_NO_EXT}_conv.flac"
ffmpeg -i "$INPUT_FILE" "${FILENAME_NO_EXT}_conv.m4a"
ffmpeg -i "$INPUT_FILE" -codec:a libmp3lame "${FILENAME_NO_EXT}_conv.mp3"
ffmpeg -i "$INPUT_FILE" "${FILENAME_NO_EXT}_conv.opus"
ffmpeg -i "$INPUT_FILE" -codec:a libvorbis "${FILENAME_NO_EXT}_conv.ogg"
ffmpeg -i "$INPUT_FILE" "${FILENAME_NO_EXT}_conv.wav"
ffmpeg -i "$INPUT_FILE" -ac 1 -ar 16000 "${FILENAME_NO_EXT}_conv_16k_mono.wav"
ffmpeg -i "$INPUT_FILE" -c:a libvorbis "${FILENAME_NO_EXT}_conv.webm"
ffmpeg -i "$INPUT_FILE" "${FILENAME_NO_EXT}_conv.wma"
ffmpeg -i "$INPUT_FILE" "${FILENAME_NO_EXT}_conv.ac3"

echo "Conversion done!"