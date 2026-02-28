# Video Transcription Tool

A Python utility for transcribing audio from local video files or online videos using OpenAI's Whisper model.

## Features

- Download audio from URLs (YouTube, etc.) using yt-dlp
- Transcribe audio using OpenAI's Whisper speech recognition model
- Real-time streaming output - text appears progressively during transcription
- 4x faster transcription with lower memory usage (via faster-whisper and int8 quantization)
- Support for various Whisper model sizes (tiny, base, small, medium, large)
- Optional timestamps at configurable intervals or for all detected segments
- Save transcriptions to text files with incremental writing
- Option to preserve downloaded audio

## Installation

### Prerequisites

- Python 3.7 or higher
- ffmpeg (required by Whisper for audio processing)
- uv (Python package installer)

### Setup

1. Install uv if you haven't already:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or on Windows:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. Clone this repository:

```bash
git clone https://github.com/askjohngeorge/video-transcription-tool.git
cd video-transcription-tool
```

3. Install required packages:

```bash
uv sync
```

## Usage

**Note:** The tool automatically updates yt-dlp to the latest version on each run. Use `--no-update` to skip this for faster startup.

### Transcribe a Local Video File

```bash
uv run transcribe video.mp4
```

### Transcribe from YouTube or Other Video URLs

```bash
uv run transcribe https://www.youtube.com/watch?v=example
```

### Using Different Whisper Model Sizes

```bash
uv run transcribe video.mp4 --model medium
```

Available models: tiny, base, small, medium, large (larger models are more accurate but require more resources)

### Adding Timestamps

By default, no timestamps are added to the transcription. To enable timestamps at regular intervals:

```bash
uv run transcribe video.mp4 --timestamps
```

To customize the timestamp interval (default is 30 seconds):

```bash
uv run transcribe video.mp4 --timestamps --interval 60
```

To include timestamps for all segments detected by Whisper:

```bash
uv run transcribe video.mp4 --all-segments
```

### Save the Transcription to a File

```bash
uv run transcribe video.mp4 --save-transcript output.txt
```

### Download and Keep the Audio

```bash
uv run transcribe https://www.youtube.com/watch?v=example --save-audio downloaded_audio.m4a
```

## Common Usage Examples

### Transcribe a Local File to a Custom Directory

```bash
uv run transcribe video.mp4 --save-transcript ./output/transcript.txt
```

### Transcribe with Model Selection and Save Output

```bash
uv run transcribe video.mp4 --model medium --save-transcript ./transcripts/output.txt
```

### Transcribe with Timestamps and Save to File

```bash
uv run transcribe video.mp4 --timestamps --interval 60 --save-transcript ./output/transcript_with_timestamps.txt
```

### Full Example: URL Download with All Options

```bash
uv run transcribe https://www.youtube.com/watch?v=example --model large --all-segments --save-audio ./audio/downloaded.m4a --save-transcript ./transcripts/full_transcript.txt
```

## Command-Line Options

- `input`: Path to a local video file or URL to download and transcribe
- `--model`: Whisper model to use (default: "base")
- `--no-update`: Skip automatic yt-dlp update check (faster startup)
- `--save-audio`: Path to save the downloaded audio (URL mode only)
- `--save-transcript`: Path to save the transcription text

Timestamp options:

- `--timestamps`: Enable timestamps at regular intervals
- `--interval`: Interval in seconds between timestamps (only used with --timestamps, default: 30.0)
- `--all-segments`: Show timestamps for all segments detected by Whisper

## Requirements

- faster-whisper
- yt-dlp
- ffmpeg-python

## License

MIT License

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for the speech recognition model
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video downloading capabilities
