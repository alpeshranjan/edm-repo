"""Command-line interface"""

import os
import sys
import tempfile
from pathlib import Path
from typing import Optional

import click
from tqdm import tqdm

from .audio_processor import AudioProcessor
from .recognizers.acrcloud import ACRCloudRecognizer
from .recognizers.audd import AuddRecognizer
from .recognizers.base import RecognitionResult
from .output.formatters import format_output, format_time
from .utils.config import Config


def deduplicate_tracks(tracks: list[dict]) -> list[dict]:
    """Remove duplicate tracks based on artist and title"""
    seen = set()
    unique_tracks = []
    
    for track in tracks:
        key = (track.get("artist", ""), track.get("title", ""))
        if key not in seen and key != ("", ""):
            seen.add(key)
            unique_tracks.append(track)
    
    return unique_tracks


def merge_results(results: list[RecognitionResult], start_time: float, end_time: float, confidence_threshold: float) -> Optional[dict]:
    """Merge recognition results and return best match"""
    # Filter by confidence threshold
    valid_results = [r for r in results if r and r.confidence >= confidence_threshold]
    
    if not valid_results:
        return None
    
    # Get result with highest confidence
    best_result = max(valid_results, key=lambda r: r.confidence)
    
    return {
        "start_time": format_time(start_time),
        "end_time": format_time(end_time),
        "artist": best_result.artist or "Unknown Artist",
        "title": best_result.title or "Unknown Title",
        "confidence": best_result.confidence,
        "source": best_result.source
    }


@click.command()
@click.argument('audio_file', type=click.Path(exists=True, readable=True))
@click.option('--format', 'output_format', default='markdown', type=click.Choice(['json', 'markdown', 'csv'], case_sensitive=False),
              help='Output format (json, markdown, csv)')
@click.option('--output', '-o', type=click.Path(writable=True), help='Output file path (default: stdout)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--segment-length', type=int, default=None, help='Segment length in seconds')
@click.option('--segment-overlap', type=int, default=None, help='Segment overlap in seconds')
@click.option('--confidence-threshold', type=float, default=None, help='Minimum confidence threshold (0.0-1.0)')
def main(audio_file: str, output_format: str, output: Optional[str], verbose: bool,
         segment_length: Optional[int], segment_overlap: Optional[int], confidence_threshold: Optional[float]):
    """Identify tracks from continuous EDM/techno mixes"""
    
    # Validate configuration
    is_valid, errors = Config.validate()
    if not is_valid:
        click.echo("Error: Missing required API keys:", err=True)
        for error in errors:
            click.echo(f"  - {error}", err=True)
        click.echo("\nPlease set API keys in .env file or environment variables.", err=True)
        sys.exit(1)
    
    # Override config with CLI options
    if segment_length:
        Config.SEGMENT_LENGTH = segment_length
    if segment_overlap:
        Config.SEGMENT_OVERLAP = segment_overlap
    if confidence_threshold is not None:
        Config.CONFIDENCE_THRESHOLD = confidence_threshold
    
    # Initialize components
    processor = AudioProcessor(
        segment_length=Config.SEGMENT_LENGTH,
        segment_overlap=Config.SEGMENT_OVERLAP
    )
    
    acrcloud = ACRCloudRecognizer()
    audd = AuddRecognizer()
    
    # Check if at least one recognizer is available
    if not acrcloud.is_available() and not audd.is_available():
        click.echo("Error: No recognition APIs configured. Please set at least one API key.", err=True)
        sys.exit(1)
    
    # Validate audio file
    if not processor.is_supported_format(audio_file):
        click.echo(f"Error: Unsupported audio format. Supported formats: {', '.join(processor.SUPPORTED_FORMATS)}", err=True)
        sys.exit(1)
    
    if verbose:
        click.echo(f"Processing: {audio_file}")
        click.echo(f"Segment length: {Config.SEGMENT_LENGTH}s, Overlap: {Config.SEGMENT_OVERLAP}s")
        click.echo(f"Confidence threshold: {Config.CONFIDENCE_THRESHOLD}")
    
    try:
        # Get audio duration and segments
        duration = processor.get_duration(audio_file)
        segments = processor.segment_audio(audio_file)
        
        if verbose:
            click.echo(f"Audio duration: {format_time(duration)}")
            click.echo(f"Number of segments: {len(segments)}")
        
        # Process segments
        all_tracks = []
        temp_files = []
        
        with tqdm(total=len(segments), desc="Processing segments", disable=not verbose) as pbar:
            for start_time, end_time in segments:
                try:
                    # Extract segment
                    segment_path = processor.extract_segment(audio_file, start_time, end_time - start_time)
                    temp_files.append(segment_path)
                    
                    # Try recognition with primary (ACRCloud)
                    results = []
                    if acrcloud.is_available():
                        result = acrcloud.recognize(segment_path, start_time, end_time - start_time)
                        if result:
                            results.append(result)
                    
                    # Try fallback (Audd.io) if no result or low confidence
                    if (not results or results[0].confidence < Config.CONFIDENCE_THRESHOLD) and audd.is_available():
                        result = audd.recognize(segment_path, start_time, end_time - start_time)
                        if result:
                            results.append(result)
                    
                    # Merge results
                    track = merge_results(results, start_time, end_time, Config.CONFIDENCE_THRESHOLD)
                    if track:
                        all_tracks.append(track)
                    
                except Exception as e:
                    if verbose:
                        click.echo(f"Error processing segment {start_time}-{end_time}: {e}", err=True)
                
                pbar.update(1)
        
        # Clean up temp files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        
        # Deduplicate tracks
        unique_tracks = deduplicate_tracks(all_tracks)
        
        if verbose:
            click.echo(f"\nFound {len(unique_tracks)} unique tracks")
        
        # Format and output
        output_text = format_output(unique_tracks, output_format)
        
        if output:
            with open(output, 'w') as f:
                f.write(output_text)
            click.echo(f"Results saved to {output}")
        else:
            click.echo(output_text)
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

