# Video Transcription Tool

A Python utility for transcribing audio from local video files or online videos using OpenAI's Whisper model.

## Features

- Download videos from URLs (YouTube, etc.) using yt-dlp
- Transcribe audio using OpenAI's Whisper speech recognition model
- Support for various Whisper model sizes (tiny, base, small, medium, large)
- Save transcriptions to text files
- Option to preserve downloaded videos

## Installation

### Prerequisites

- Python 3.7 or higher
- ffmpeg (required by Whisper for audio processing)

### Setup

1. Clone this repository:

```bash
git clone https://github.com/yourusername/video-transcription-tool.git
cd video-transcription-tool
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

Make sure the script is executable:

```bash
chmod +x transcribe.py
```

## Usage

### Transcribe a Local Video File

```bash
./transcribe.py video.mp4
```

### Transcribe from YouTube or Other Video URLs

```bash
./transcribe.py https://www.youtube.com/watch?v=example
```

### Using Different Whisper Model Sizes

```bash
./transcribe.py video.mp4 --model medium
```

Available models: tiny, base, small, medium, large (larger models are more accurate but require more resources)

### Save the Transcription to a File

```bash
./transcribe.py video.mp4 --save-transcript output.txt
```

### Download and Keep the Video

```bash
./transcribe.py https://www.youtube.com/watch?v=example --save-video downloaded_video.mp4
```

## Command-Line Options

- `input`: Path to a local video file or URL to download and transcribe
- `--model`: Whisper model to use (default: "base")
- `--save-video`: Path to save the downloaded video (URL mode only)
- `--save-transcript`: Path to save the transcription text

## Requirements

- openai-whisper
- yt-dlp
- ffmpeg-python

## License

MIT License

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for the speech recognition model
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video downloading capabilities
