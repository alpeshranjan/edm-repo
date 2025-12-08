
from fastmcp import FastMCP
from typing import Optional, List
import sys
import os
import concurrent.futures

# Add src to path to import local modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.utils.config import Config
    from src.audio_processor import AudioProcessor
    from src.recognizers.acrcloud import ACRCloudRecognizer
    from src.recognizers.audd import AuddRecognizer
    from src.recognizers.shazam import ShazamRecognizer
    from src.recognizers.songfinder import SongFinderRecognizer
    from src.utils.track_utils import merge_results, deduplicate_tracks
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

# Initialize FastMCP server
mcp = FastMCP("EDM Track Identifier")

@mcp.tool()
def identify_tracks(
    audio_file_path: str,
    confidence_threshold: float = 0.5,
    segment_length: int = 60,
    segment_overlap: int = 20
) -> str:
    """
    Identify tracks in an EDM mix using available recognition APIs (ACRCloud, Shazam, etc.).
    
    Args:
        audio_file_path: Absolute path to the audio file.
        confidence_threshold: Minimum confidence score (0.0-1.0) to include a track.
        segment_length: Length of audio segments in seconds.
        segment_overlap: Overlap between segments in seconds.
        
    Returns:
        A markdown formatted string containing the list of identified tracks.
    """
    
    # Validate file
    if not os.path.exists(audio_file_path):
        return f"Error: File not found at {audio_file_path}"
        
    # Validate config
    is_valid, errors = Config.validate()
    if not is_valid:
        error_msg = "Error: Missing API keys:\n" + "\n".join([f"- {e}" for e in errors])
        return error_msg

    # Configure
    Config.CONFIDENCE_THRESHOLD = confidence_threshold
    Config.SEGMENT_LENGTH = segment_length
    Config.SEGMENT_OVERLAP = segment_overlap
    
    # Initialize components
    try:
        processor = AudioProcessor(
            segment_length=segment_length,
            segment_overlap=segment_overlap
        )
    except Exception as e:
        return f"Error initializing audio processor: {str(e)}"

    acrcloud = ACRCloudRecognizer()
    audd = AuddRecognizer()
    shazam = ShazamRecognizer()
    songfinder = SongFinderRecognizer()
    
    if not any([acrcloud.is_available(), audd.is_available(), shazam.is_available(), songfinder.is_available()]):
        return "Error: No recognition APIs configured. Please set at least one API key in .env."

    try:
        # Process
        # duration = processor.get_duration(audio_file_path) # Not strictly needed for result
        segments = processor.segment_audio(audio_file_path)
        
        all_tracks = []
        
        # Limit segments to avoid timeouts in MCP context if file is huge
        # But let's try to process as much as possible or maybe add a limit param
        max_segments = 20 # Conservative limit for tool usage
        
        if len(segments) > max_segments:
             print(f"Warning: File too large, processing first {max_segments} segments only.")
             segments = segments[:max_segments]

        # Use a simplified processing loop for MCP (similar to cli.py but cleaner return)
        for start_time, end_time in segments:
            segment_path = None
            try:
                segment_path = processor.extract_segment(audio_file_path, start_time, end_time - start_time)
                
                results = []
                
                # Try ACRCloud
                if acrcloud.is_available():
                    res = acrcloud.recognize(segment_path, start_time, end_time - start_time)
                    if res: results.append(res)
                
                # Try Shazam if needed
                if (not results or results[0].confidence < confidence_threshold) and shazam.is_available():
                    res = shazam.recognize(segment_path, start_time, end_time - start_time)
                    if res: results.append(res)
                    
                # Try SongFinder if needed
                if (not results or (results and results[0].confidence < confidence_threshold)) and songfinder.is_available():
                    res = songfinder.recognize(segment_path, start_time, end_time - start_time)
                    if res: results.append(res)

                # Try Audd if needed
                if (not results or results[0].confidence < confidence_threshold) and audd.is_available():
                    res = audd.recognize(segment_path, start_time, end_time - start_time)
                    if res: results.append(res)
                
                use_ai = len(results) > 1 
                track = merge_results(results, start_time, end_time, confidence_threshold, use_ai=use_ai)
                if track:
                    all_tracks.append(track)
                    
            except Exception as e:
                print(f"Error processing segment {start_time}-{end_time}: {e}")
            finally:
                if segment_path and os.path.exists(segment_path):
                    try:
                        os.unlink(segment_path)
                    except:
                        pass
                        
        unique_tracks = deduplicate_tracks(all_tracks)
        
        if not unique_tracks:
            return "No tracks identified."
            
        # Format output
        output_lines = ["## Identified Tracks"]
        for t in unique_tracks:
            output_lines.append(f"- **{t['artist']}** - {t['title']} ({t['start_time']} - {t['end_time']}) [Confidence: {t['confidence']:.2f}]")

        return "\n".join(output_lines)
        
    except Exception as e:
        return f"Error during processing: {str(e)}"

if __name__ == "__main__":
    mcp.run()
