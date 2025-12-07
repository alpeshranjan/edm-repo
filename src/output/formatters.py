"""Output formatters for different formats"""

from typing import List, Dict, Any
from ..recognizers.base import RecognitionResult


def format_time(seconds: float) -> str:
    """Format seconds as HH:MM:SS"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_json(tracks: List[Dict[str, Any]]) -> str:
    """Format tracks as JSON"""
    import json
    return json.dumps({"tracks": tracks}, indent=2)


def format_markdown(tracks: List[Dict[str, Any]]) -> str:
    """Format tracks as Markdown"""
    lines = ["## Tracklist", ""]
    
    for track in tracks:
        start = track.get("start_time", "00:00:00")
        end = track.get("end_time", "00:00:00")
        artist = track.get("artist", "Unknown Artist")
        title = track.get("title", "Unknown Title")
        confidence = track.get("confidence", 0.0)
        confidence_pct = int(confidence * 100)
        
        lines.append(f"{start} - {end} | {artist} - {title} (confidence: {confidence_pct}%)")
    
    return "\n".join(lines)


def format_csv(tracks: List[Dict[str, Any]]) -> str:
    """Format tracks as CSV"""
    import csv
    from io import StringIO
    
    if not tracks:
        return ""
    
    output = StringIO()
    fieldnames = ["start_time", "end_time", "artist", "title", "confidence", "source"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for track in tracks:
        writer.writerow({
            "start_time": track.get("start_time", "00:00:00"),
            "end_time": track.get("end_time", "00:00:00"),
            "artist": track.get("artist", "Unknown Artist"),
            "title": track.get("title", "Unknown Title"),
            "confidence": track.get("confidence", 0.0),
            "source": track.get("source", "unknown")
        })
    
    return output.getvalue()


def format_output(tracks: List[Dict[str, Any]], format_type: str) -> str:
    """Format tracks in the specified format"""
    format_type = format_type.lower()
    
    if format_type == "json":
        return format_json(tracks)
    elif format_type == "markdown" or format_type == "md":
        return format_markdown(tracks)
    elif format_type == "csv":
        return format_csv(tracks)
    else:
        raise ValueError(f"Unknown format: {format_type}")

