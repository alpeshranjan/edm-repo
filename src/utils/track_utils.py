"""Track processing utilities"""

from typing import Optional, List
from ..recognizers.base import RecognitionResult
from ..output.formatters import format_time


def deduplicate_tracks(tracks: list[dict], use_ai: bool = False) -> list[dict]:
    """Remove duplicate tracks (AI only used for final batch, not per-track)"""
    if not tracks:
        return []
    
    # Fast simple deduplication first
    seen = set()
    unique_tracks = []
    
    for track in tracks:
        key = (track.get("artist", "").lower().strip(), track.get("title", "").lower().strip())
        if key not in seen and key != ("", ""):
            seen.add(key)
            unique_tracks.append(track)
    
    # Only use AI for final smart deduplication if many tracks remain
    # This is fast - AI called once at the end, not per-track
    if use_ai and len(unique_tracks) > 5:  # Only for larger tracklists
        try:
            from ..ai.orchestrator import AIOrchestrator
            orchestrator = AIOrchestrator()
            if orchestrator.is_available():
                # Batch process all tracks at once (much faster)
                smart_unique = orchestrator.smart_deduplicate(unique_tracks)
                if len(smart_unique) < len(unique_tracks):
                    print(f"[AI] Smart deduplication: {len(unique_tracks)} -> {len(smart_unique)} tracks")
                    return smart_unique
        except Exception as e:
            print(f"[AI] Unavailable: {e}, using simple deduplication")
    
    return unique_tracks


def merge_results(results: list[RecognitionResult], start_time: float, end_time: float, confidence_threshold: float, use_ai: bool = False) -> Optional[dict]:
    """Merge recognition results and return best match (AI only used when results conflict)"""
    # Filter by confidence threshold
    valid_results = [r for r in results if r and r.confidence >= confidence_threshold]
    
    if not valid_results:
        return None
    
    # Only use AI if results conflict (different tracks from different APIs)
    # This is much faster - AI only called when needed
    if use_ai and len(valid_results) > 1:
        # Check if results conflict (different artist/title)
        artists = set(r.artist.lower().strip() if r.artist else "" for r in valid_results)
        titles = set(r.title.lower().strip() if r.title else "" for r in valid_results)
        
        # Only use AI if there's actual conflict
        if len(artists) > 1 or len(titles) > 1:
            try:
                from ..ai.orchestrator import AIOrchestrator
                orchestrator = AIOrchestrator()
                if orchestrator.is_available():
                    valid_results = orchestrator.validate_and_rank_results(valid_results)
                    print(f"[AI] Resolved conflict: {len(valid_results)} results")
            except Exception as e:
                print(f"[AI] Unavailable: {e}, using confidence-based selection")
    
    # Get best result (AI-validated if conflict, otherwise highest confidence)
    best_result = valid_results[0] if valid_results else max(valid_results, key=lambda r: r.confidence)
    
    return {
        "start_time": format_time(start_time),
        "end_time": format_time(end_time),
        "artist": best_result.artist or "Unknown Artist",
        "title": best_result.title or "Unknown Title",
        "confidence": best_result.confidence,
        "source": best_result.source
    }

