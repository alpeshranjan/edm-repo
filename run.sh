#!/bin/bash
# Quick launcher script for EDM Track Recognizer

cd "/Users/alpesh/Downloads/untitled folder 2"
source venv/bin/activate

if [ -z "$1" ]; then
    echo "Usage: ./run.sh <audio_file>"
    echo "Example: ./run.sh ~/Downloads/mix.mp3"
    exit 1
fi

python -m src.cli "$1" --output tracklist.md --verbose
