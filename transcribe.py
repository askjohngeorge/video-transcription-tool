#!/usr/bin/env python3

import argparse
import os
import tempfile
import subprocess
import whisper


def download_video(url, output_path):
    """Download a video from a URL using yt-dlp."""
    # Construct the yt-dlp command
    command = [
        "yt-dlp",
        "-f",
        "mp4",  # Prefer MP4 format
        "-o",
        output_path,
        url,
    ]

    # Execute the command
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading video: {e}")
        return False


def is_likely_url(text):
    """Simple check to determine if the input is likely a URL."""
    return text.startswith(("http://", "https://", "www.", "youtube.com", "youtu.be"))


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio from a local file or download and transcribe from a URL using Whisper."
    )

    parser.add_argument(
        "input", type=str, help="Path to a local video file or URL to download and transcribe"
    )

    # Model selection
    parser.add_argument(
        "--model",
        type=str,
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model to use for transcription",
    )

    # Output options
    parser.add_argument(
        "--save-video", type=str, help="Path to save the downloaded video (URL mode only)"
    )
    parser.add_argument("--save-transcript", type=str, help="Path to save the transcription text")

    args = parser.parse_args()

    # Determine if the input is a local file or a URL
    if os.path.exists(args.input):
        # Process a local file
        print(f"Using local file: {args.input}")
        file_to_transcribe = args.input
        temp_dir = None
    elif is_likely_url(args.input):
        # It looks like a URL
        print(f"Detected URL input: {args.input}")

        # Determine where to save the video
        if args.save_video:
            video_path = args.save_video
            temp_dir = None  # We're not using a temp directory
        else:
            # Create a temporary directory to store the downloaded video
            temp_dir = tempfile.TemporaryDirectory()
            video_path = os.path.join(temp_dir.name, "video.mp4")

        # Download the video
        print("Downloading video...")
        if not download_video(args.input, video_path):
            print("Failed to download the video. Exiting.")
            if temp_dir:
                temp_dir.cleanup()
            return

        print(f"Video downloaded successfully to: {video_path}")

        # Set the file to transcribe
        file_to_transcribe = video_path
    else:
        # Neither a local file nor a URL
        print(f"Error: '{args.input}' is not a valid file path or URL.")
        return

    try:
        # Load the Whisper model
        print(f"Loading Whisper model: {args.model}")
        model = whisper.load_model(args.model)

        # Transcribe the file
        print("Transcribing audio...")
        result = model.transcribe(file_to_transcribe)

        # Save the transcription if requested
        if args.save_transcript:
            with open(args.save_transcript, "w", encoding="utf-8") as f:
                f.write(result["text"])
            print(f"Transcription saved to: {args.save_transcript}")

        # Print the transcription
        print("\nTranscription:\n")
        print(result["text"])

    finally:
        # Clean up the temporary directory if we created one
        if temp_dir:
            temp_dir.cleanup()


if __name__ == "__main__":
    main()
