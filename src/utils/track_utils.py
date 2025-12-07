"""Track processing utilities"""

from typing import Optional
from ..recognizers.base import RecognitionResult
from ..output.formatters import format_time


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

