"""Track processing utilities"""

from typing import Optional, List
from ..recognizers.base import RecognitionResult
from ..output.formatters import format_time


def deduplicate_tracks(tracks: list[dict], use_ai: bool = True) -> list[dict]:
    """Remove duplicate tracks (with optional AI-powered smart deduplication)"""
    if not tracks:
        return []
    
    # Use AI for smart deduplication if available
    if use_ai and len(tracks) > 1:
        try:
            from ..ai.orchestrator import AIOrchestrator
            orchestrator = AIOrchestrator()
            if orchestrator.is_available():
                unique = orchestrator.smart_deduplicate(tracks)
                print(f"[AI] Smart deduplication: {len(tracks)} -> {len(unique)} tracks")
                return unique
        except Exception as e:
            print(f"[AI] Smart deduplication unavailable: {e}, using fallback")
    
    # Fallback to simple deduplication
    seen = set()
    unique_tracks = []
    
    for track in tracks:
        key = (track.get("artist", "").lower().strip(), track.get("title", "").lower().strip())
        if key not in seen and key != ("", ""):
            seen.add(key)
            unique_tracks.append(track)
    
    return unique_tracks


def merge_results(results: list[RecognitionResult], start_time: float, end_time: float, confidence_threshold: float, use_ai: bool = True) -> Optional[dict]:
    """Merge recognition results and return best match (with optional AI validation)"""
    # Filter by confidence threshold
    valid_results = [r for r in results if r and r.confidence >= confidence_threshold]
    
    if not valid_results:
        return None
    
    # Use AI to validate and rank if available
    if use_ai and len(valid_results) > 1:
        try:
            from ..ai.orchestrator import AIOrchestrator
            orchestrator = AIOrchestrator()
            if orchestrator.is_available():
                valid_results = orchestrator.validate_and_rank_results(valid_results)
                print(f"[AI] Validated and ranked {len(valid_results)} results")
        except Exception as e:
            print(f"[AI] Orchestrator unavailable: {e}, using fallback")
    
    # Get best result (now AI-validated if available)
    best_result = valid_results[0] if valid_results else max(valid_results, key=lambda r: r.confidence)
    
    return {
        "start_time": format_time(start_time),
        "end_time": format_time(end_time),
        "artist": best_result.artist or "Unknown Artist",
        "title": best_result.title or "Unknown Title",
        "confidence": best_result.confidence,
        "source": best_result.source
    }

