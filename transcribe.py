#!/usr/bin/env python3

import argparse
import os
import shutil
import sys
import tempfile
import subprocess
from faster_whisper import WhisperModel
import glob
import math


def format_timestamp(seconds):
    """Convert seconds to a formatted timestamp string (HH:MM:SS)."""
    hours = math.floor(seconds / 3600)
    minutes = math.floor((seconds % 3600) / 60)
    seconds = math.floor(seconds % 60)
    return f"[{hours:02d}:{minutes:02d}:{seconds:02d}]"


def download_audio(url, output_path):
    """Download audio from a URL using yt-dlp."""
    command = [
        "yt-dlp",
        "-f", "bestaudio",       # Best quality audio-only stream
        "-x",                     # Extract audio
        "--audio-format", "m4a",  # Consistent output format
        "-o", output_path,
        url,
    ]

    try:
        subprocess.run(command, check=True)
        return True, output_path
    except subprocess.CalledProcessError as e:
        print(f"Error downloading audio: {e}")
        return False, None


def download_raw(url, output_dir, filename_stem="media"):
    """Download from a URL using default yt-dlp settings."""
    output_template = os.path.join(output_dir, filename_stem + ".%(ext)s")
    command = ["yt-dlp", "-o", output_template, url]
    try:
        subprocess.run(command, check=True)
        files = glob.glob(os.path.join(output_dir, filename_stem + ".*"))
        if not files:
            return False, None
        return True, files[0]
    except subprocess.CalledProcessError as e:
        print(f"Error downloading: {e}")
        return False, None


def is_likely_url(text):
    """Simple check to determine if the input is likely a URL."""
    return text.startswith(("http://", "https://", "www.", "youtube.com", "youtu.be"))


def update_ytdlp():
    """Update yt-dlp to the latest version using uv."""
    if shutil.which("uv"):
        # Update the lock file to pick up the latest yt-dlp version
        lock_result = subprocess.run(
            ["uv", "lock", "--upgrade-package", "yt-dlp"],
            capture_output=True,
            text=True
        )
        if lock_result.returncode == 0 and "Updated" in lock_result.stderr:
            # Sync the venv with the updated lock file
            subprocess.run(["uv", "sync"], capture_output=True, text=True)
            print("yt-dlp updated to latest version")


def main_with_update():
    """Entry point that updates yt-dlp before running (unless --no-update)."""
    try:
        if "--no-update" not in sys.argv:
            update_ytdlp()
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)


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

    # Update options
    parser.add_argument(
        "--no-update",
        action="store_true",
        help="Skip automatic yt-dlp update check (faster startup)",
    )

    # Output options
    parser.add_argument(
        "--save-audio", type=str, help="Path to save the downloaded audio (URL mode only)"
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Download with default yt-dlp settings instead of audio-only (use for sites that don't offer separate audio streams)",
    )
    parser.add_argument("--save-transcript", type=str, help="Path to save the transcription text")

    # Timestamp options - now as a mutually exclusive group
    timestamp_group = parser.add_argument_group("timestamp options")
    timestamp_group.add_argument(
        "--timestamps",
        action="store_true",
        help="Enable timestamps at regular intervals",
    )
    timestamp_group.add_argument(
        "--all-segments",
        action="store_true",
        help="Show timestamps for all segments detected by Whisper",
    )
    timestamp_group.add_argument(
        "--interval",
        type=float,
        default=30.0,
        help="Interval in seconds between timestamps (only used with --timestamps, default: 30.0)",
    )

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

        if args.save_audio:
            save_dir = os.path.dirname(os.path.abspath(args.save_audio))
            save_stem = os.path.splitext(os.path.basename(args.save_audio))[0]
            temp_dir = None
        else:
            temp_dir = tempfile.TemporaryDirectory()
            save_dir = temp_dir.name
            save_stem = "media"

        if args.raw:
            # Raw mode: download with default yt-dlp settings
            print("Downloading (raw mode)...")
            success, actual_path = download_raw(args.input, save_dir, save_stem)
            if not success:
                print("Failed to download. Exiting.")
                if temp_dir:
                    temp_dir.cleanup()
                return
        else:
            # Standard mode: try audio-only first
            audio_path = os.path.join(save_dir, save_stem + ".m4a") if args.save_audio else os.path.join(save_dir, "audio.m4a")
            print("Downloading audio...")
            success, actual_path = download_audio(args.input, audio_path)

            if not success:
                print("\nAudio-only download failed. This can happen with sites that don't offer separate audio streams.")
                try:
                    response = input("Would you like to fall back to downloading the full video? (Y/n) ")
                except EOFError:
                    response = "n"

                if response.strip().lower() not in ("n", "no"):
                    print("Downloading with default settings...")
                    success, actual_path = download_raw(args.input, save_dir, save_stem)
                    if not success:
                        print("Failed to download. Exiting.")
                        if temp_dir:
                            temp_dir.cleanup()
                        return
                else:
                    print("Exiting.")
                    if temp_dir:
                        temp_dir.cleanup()
                    return

        print(f"Downloaded successfully to: {actual_path}")
        file_to_transcribe = actual_path
    else:
        # Neither a local file nor a URL
        print(f"Error: '{args.input}' is not a valid file path or URL.")
        return

    try:
        # Load the Whisper model
        print(f"Loading Whisper model: {args.model}")
        model = WhisperModel(args.model, device="cpu", compute_type="int8")

        # Transcribe the file
        print("Transcribing audio...")
        segments, info = model.transcribe(file_to_transcribe)

        # Print header before streaming starts
        print("\nTranscription:\n")

        # Open file for streaming writes if requested
        output_file = None
        if args.save_transcript:
            output_file = open(args.save_transcript, "w", encoding="utf-8")

        # Process segments as they're generated (real-time streaming)
        formatted_transcription = ""
        last_timestamp = -args.interval  # Ensure first segment always gets a timestamp if enabled
        use_timestamps = args.timestamps or args.all_segments

        for segment in segments:
            start_time = segment.start
            text = segment.text

            # Determine formatted output for this segment
            segment_output = ""

            # No timestamps (default behavior)
            if not use_timestamps:
                if not formatted_transcription:
                    segment_output = text.lstrip()
                else:
                    segment_output = " " + text.lstrip()
            # Add timestamp for all segments
            elif args.all_segments:
                if formatted_transcription:  # Add newline except for the first timestamp
                    segment_output = "\n"
                timestamp = format_timestamp(start_time)
                segment_output += f"{timestamp} {text.lstrip()}"
            # Add timestamp at specified intervals
            elif args.timestamps and start_time - last_timestamp >= args.interval:
                if formatted_transcription:  # Add newline except for the first timestamp
                    segment_output = "\n"
                timestamp = format_timestamp(start_time)
                segment_output += f"{timestamp} {text.lstrip()}"
                last_timestamp = start_time
            # Just append text without timestamp (within the interval)
            else:
                segment_output = " " + text.lstrip()

            # Stream to terminal
            print(segment_output, end="", flush=True)

            # Stream to file if open
            if output_file:
                output_file.write(segment_output)
                output_file.flush()

            # Build complete transcription
            formatted_transcription += segment_output

        # Add final newline to terminal
        print()

        # Close file if it was opened
        if output_file:
            output_file.close()
            print(f"\nTranscription saved to: {args.save_transcript}")

    finally:
        # Clean up the temporary directory if we created one
        if temp_dir:
            temp_dir.cleanup()


if __name__ == "__main__":
    main_with_update()
