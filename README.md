# Video Transcription Tool

A Python utility for transcribing audio from local video files or online videos using OpenAI's Whisper model.

## Features

- Download videos from URLs (YouTube, etc.) using yt-dlp
- Transcribe audio using OpenAI's Whisper speech recognition model
- Support for various Whisper model sizes (tiny, base, small, medium, large)
- Optional timestamps at configurable intervals or for all detected segments
- Save transcriptions to text files
- Option to preserve downloaded videos

## Installation

### Prerequisites

- Python 3.7 or higher
- ffmpeg (required by Whisper for audio processing)

### Setup

1. Clone this repository:

```bash
git clone https://github.com/askjohngeorge/video-transcription-tool.git
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

### Adding Timestamps

By default, no timestamps are added to the transcription. To enable timestamps at regular intervals:

```bash
./transcribe.py video.mp4 --timestamps
```

To customize the timestamp interval (default is 30 seconds):

```bash
./transcribe.py video.mp4 --timestamps --interval 60
```

To include timestamps for all segments detected by Whisper:

```bash
./transcribe.py video.mp4 --all-segments
```

### Save the Transcription to a File

```bash
./transcribe.py video.mp4 --save-transcript output.txt
```

### Download and Keep the Video

```bash
./transcribe.py https://www.youtube.com/watch?v=example --save-video downloaded_video.mp4
```

## Common Usage Examples

### Transcribe a Local File to a Custom Directory

```bash
./transcribe.py video.mp4 --save-transcript ./output/transcript.txt
```

### Transcribe with Model Selection and Save Output

```bash
./transcribe.py video.mp4 --model medium --save-transcript ./transcripts/output.txt
```

### Transcribe with Timestamps and Save to File

```bash
./transcribe.py video.mp4 --timestamps --interval 60 --save-transcript ./output/transcript_with_timestamps.txt
```

### Full Example: URL Download with All Options

```bash
./transcribe.py https://www.youtube.com/watch?v=example --model large --all-segments --save-video ./videos/downloaded.mp4 --save-transcript ./transcripts/full_transcript.txt
```

## Command-Line Options

- `input`: Path to a local video file or URL to download and transcribe
- `--model`: Whisper model to use (default: "base")
- `--save-video`: Path to save the downloaded video (URL mode only)
- `--save-transcript`: Path to save the transcription text

Timestamp options:

- `--timestamps`: Enable timestamps at regular intervals
- `--interval`: Interval in seconds between timestamps (only used with --timestamps, default: 30.0)
- `--all-segments`: Show timestamps for all segments detected by Whisper

## Requirements

- openai-whisper
- yt-dlp
- ffmpeg-python

## License

MIT License

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for the speech recognition model
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video downloading capabilities
