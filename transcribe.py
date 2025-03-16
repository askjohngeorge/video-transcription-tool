#!/usr/bin/env python3
import argparse
import whisper

def main():
    parser = argparse.ArgumentParser(
        description="Transcribe the audio from an MP4 file using Whisper."
    )
    parser.add_argument("input_file", type=str, help="Path to the MP4 file")
    args = parser.parse_args()

    # Load a Whisper model (you can change "base" to another model if needed)
    model = whisper.load_model("base")

    # Transcribe the audio directly from the MP4 file.
    result = model.transcribe(args.input_file)
    
    # Print the transcription.
    print("Transcription:\n")
    print(result["text"])

if __name__ == "__main__":
    main()
