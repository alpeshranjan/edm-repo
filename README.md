# EDM Set Track Recognition Tool

A command-line tool to identify individual tracks from continuous EDM/techno mixes that may have overlays, BPM changes, and effects. Uses third-party API recognition services (ACRCloud and Audd.io) to identify tracks from your mixes.

## Features

- Identify tracks from continuous mixes (up to 100MB)
- Handles tempo changes, overlays, and effects
- Supports multiple audio formats (MP3, WAV, FLAC, M4A, OGG)
- Multiple output formats (JSON, Markdown, CSV)
- Progress indicators for large files
- Dual API support (ACRCloud primary, Audd.io fallback)

## Installation

1. Install Python 3.11+ and FFmpeg:
   ```bash
   # macOS
   brew install ffmpeg
   
   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Get API keys:
   - **ACRCloud**: Sign up at [acrcloud.com](https://www.acrcloud.com) and get your access key and secret key
   - **Audd.io**: Sign up at [audd.io](https://audd.io) and get your API token

4. Create `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

## Usage

```bash
# Basic usage
python -m src.cli path/to/your/mix.mp3

# Specify output format
python -m src.cli path/to/your/mix.mp3 --format json
python -m src.cli path/to/your/mix.mp3 --format markdown
python -m src.cli path/to/your/mix.mp3 --format csv

# Specify output file
python -m src.cli path/to/your/mix.mp3 --output tracklist.json

# Verbose mode
python -m src.cli path/to/your/mix.mp3 --verbose
```

## Output Formats

### JSON
```json
{
  "tracks": [
    {
      "start_time": "00:00:00",
      "end_time": "00:05:23",
      "artist": "Artist Name",
      "title": "Track Title",
      "confidence": 0.95,
      "source": "acrcloud"
    }
  ]
}
```

### Markdown
```markdown
## Tracklist

00:00:00 - 00:05:23 | Artist Name - Track Title (confidence: 95%)
```

### CSV
```csv
start_time,end_time,artist,title,confidence,source
00:00:00,00:05:23,Artist Name,Track Title,0.95,acrcloud
```

## Configuration

You can configure the tool via environment variables in `.env`:

- `SEGMENT_LENGTH`: Length of audio segments in seconds (default: 45)
- `SEGMENT_OVERLAP`: Overlap between segments in seconds (default: 15)
- `CONFIDENCE_THRESHOLD`: Minimum confidence score to include track (default: 0.5)

## API Limits

- **ACRCloud Free Tier**: ~100 requests/day
- **Audd.io Free Tier**: Limited requests/month

For higher usage, consider upgrading to paid plans.

## Troubleshooting

- **FFmpeg not found**: Make sure FFmpeg is installed and in your PATH
- **API errors**: Check your API keys in `.env` file
- **Rate limit errors**: You've exceeded your API quota, wait or upgrade plan
- **No matches found**: The tracks might not be in the API databases (especially very obscure underground tracks)

## License

MIT

