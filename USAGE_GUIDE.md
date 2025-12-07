# How to Use EDM Track Recognizer (Standalone Guide)

This guide shows you how to use the tool on your own, without Cursor.

## Quick Start

### 1. Open Terminal

On macOS:
- Press `Cmd + Space` to open Spotlight
- Type "Terminal" and press Enter
- Or go to Applications → Utilities → Terminal

### 2. Navigate to the Project Directory

```bash
cd "/Users/alpesh/Downloads/untitled folder 2"
```

### 3. Activate the Virtual Environment

```bash
source venv/bin/activate
```

You should see `(venv)` appear at the beginning of your terminal prompt, like:
```
(venv) alpesh@MacBook ~/Downloads/untitled folder 2 %
```

### 4. Run the Tool

```bash
python -m src.cli "/path/to/your/audio/file.mp3"
```

## Basic Usage Examples

### Identify tracks from a mix (Markdown output)
```bash
python -m src.cli ~/Downloads/your_mix.mp3
```

### Save results to a file
```bash
python -m src.cli ~/Downloads/your_mix.mp3 --output tracklist.md
```

### Get JSON output
```bash
python -m src.cli ~/Downloads/your_mix.mp3 --format json --output tracklist.json
```

### Get CSV output (for spreadsheets)
```bash
python -m src.cli ~/Downloads/your_mix.mp3 --format csv --output tracklist.csv
```

### Verbose mode (see progress)
```bash
python -m src.cli ~/Downloads/your_mix.mp3 --verbose
```

## All Available Options

```bash
python -m src.cli [OPTIONS] AUDIO_FILE

Options:
  --format [json|markdown|csv]  Output format (default: markdown)
  -o, --output PATH              Save to file instead of printing
  -v, --verbose                  Show detailed progress
  --segment-length INTEGER       Length of each segment in seconds (default: 45)
  --segment-overlap INTEGER      Overlap between segments in seconds (default: 15)
  --confidence-threshold FLOAT  Minimum confidence score 0.0-1.0 (default: 0.5)
  --help                        Show help message
```

## Common Workflows

### Process a mix and save to file
```bash
cd "/Users/alpesh/Downloads/untitled folder 2"
source venv/bin/activate
python -m src.cli ~/Downloads/my_mix.mp3 --output tracklist.md --verbose
```

### Process multiple files (one at a time)
```bash
cd "/Users/alpesh/Downloads/untitled folder 2"
source venv/bin/activate

python -m src.cli ~/Downloads/mix1.mp3 --output mix1_tracks.md
python -m src.cli ~/Downloads/mix2.mp3 --output mix2_tracks.md
python -m src.cli ~/Downloads/mix3.mp3 --output mix3_tracks.md
```

### Custom settings for better accuracy
```bash
python -m src.cli ~/Downloads/my_mix.mp3 \
  --segment-length 60 \
  --segment-overlap 20 \
  --confidence-threshold 0.7 \
  --output tracklist.json \
  --format json
```

## File Paths

### Using files in Downloads folder
```bash
python -m src.cli ~/Downloads/filename.mp3
```

### Using files with spaces in name
```bash
python -m src.cli "/Users/alpesh/Downloads/file with spaces.mp3"
```

### Using files in current directory
```bash
python -m src.cli ./myfile.mp3
```

### Using absolute paths
```bash
python -m src.cli "/full/path/to/your/file.mp3"
```

## Supported Audio Formats

- MP3 (`.mp3`)
- WAV (`.wav`)
- FLAC (`.flac`)
- M4A (`.m4a`)
- OGG (`.ogg`)
- AAC (`.aac`)

## Output Formats

### Markdown (default)
Human-readable format with timestamps:
```markdown
## Tracklist

00:00:00 - 00:05:23 | Artist Name - Track Title (confidence: 95%)
00:05:23 - 00:10:45 | Another Artist - Another Track (confidence: 87%)
```

### JSON
Structured data for programming:
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

### CSV
Spreadsheet-friendly format:
```csv
start_time,end_time,artist,title,confidence,source
00:00:00,00:05:23,Artist Name,Track Title,0.95,acrcloud
```

## Troubleshooting

### "No module named 'src'"
**Solution:** Make sure you're in the project directory and virtual environment is activated:
```bash
cd "/Users/alpesh/Downloads/untitled folder 2"
source venv/bin/activate
```

### "Missing required API keys"
**Solution:** Edit the `.env` file and add your API keys:
```bash
nano .env
# or
open -e .env
```

### "FFmpeg not found"
**Solution:** Install FFmpeg:
```bash
brew install ffmpeg
```

### "File not found"
**Solution:** Check the file path. Use quotes if path has spaces:
```bash
python -m src.cli "/path/with spaces/file.mp3"
```

### Process takes too long
**Solution:** Adjust segment settings:
```bash
python -m src.cli file.mp3 --segment-length 60 --segment-overlap 20
```

## Monitoring Progress

### Check if process is running
```bash
ps aux | grep "python -m src.cli"
```

### Check output file
```bash
ls -lh tracklist.md
cat tracklist.md
```

### Use the progress checker script
```bash
./check_progress.sh
```

## Tips

1. **Always activate the virtual environment first** - You need to run `source venv/bin/activate` each time you open a new terminal

2. **Use verbose mode for long files** - See progress with `--verbose` flag

3. **Save output to files** - Use `--output filename.md` to save results

4. **For better accuracy** - Use longer segments (60s) and higher confidence threshold (0.7)

5. **For faster processing** - Use shorter segments (30s) but may miss some tracks

## Quick Reference Card

```bash
# Setup (do this once per terminal session)
cd "/Users/alpesh/Downloads/untitled folder 2"
source venv/bin/activate

# Basic usage
python -m src.cli ~/Downloads/mix.mp3

# With options
python -m src.cli ~/Downloads/mix.mp3 --format json --output results.json --verbose

# Check help
python -m src.cli --help
```

## Need Help?

- Check the README.md file for more details
- Check API_KEYS_SETUP.md for API key setup
- Run `python -m src.cli --help` for command options

