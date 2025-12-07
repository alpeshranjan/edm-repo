"""Shazam API integration"""

import os
import requests
from typing import Optional
from .base import BaseRecognizer, RecognitionResult
from ..utils.config import Config


class ShazamRecognizer(BaseRecognizer):
    """Shazam API recognizer (via RapidAPI)"""
    
    # RapidAPI Shazam endpoint
    API_URL = "https://shazam.p.rapidapi.com/songs/detect"
    
    def __init__(self):
        self.api_key = getattr(Config, 'SHAZAM_API_KEY', None)
        self.api_host = "shazam.p.rapidapi.com"
    
    def is_available(self) -> bool:
        """Check if Shazam API is configured"""
        return bool(self.api_key)
    
    def recognize(self, audio_file_path: str, start_time: float = 0.0, duration: float = 30.0) -> Optional[RecognitionResult]:
        """
        Recognize a track using Shazam API
        
        Args:
            audio_file_path: Path to the audio file
            start_time: Start time in seconds
            duration: Duration of segment in seconds
            
        Returns:
            RecognitionResult if track found, None otherwise
        """
        if not self.is_available():
            return None
        
        try:
            # Read audio file
            with open(audio_file_path, 'rb') as f:
                files = {
                    'upload_file': (os.path.basename(audio_file_path), f, 'audio/mpeg')
                }
                headers = {
                    'X-RapidAPI-Key': self.api_key,
                    'X-RapidAPI-Host': self.api_host
                }
                
                # Make API request to RapidAPI Shazam
                response = requests.post(self.API_URL, files=files, headers=headers, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                
                # Parse RapidAPI Shazam response format
                if result.get('status') == 'success' and result.get('track'):
                    track = result['track']
                    return RecognitionResult(
                        artist=track.get('subtitle') or track.get('artists', [{}])[0].get('name', 'Unknown'),
                        title=track.get('title', 'Unknown'),
                        confidence=0.85,  # Shazam results are typically high confidence
                        source="shazam",
                        metadata=track
                    )
                elif result.get('matches') and len(result['matches']) > 0:
                    # Alternative response format
                    match = result['matches'][0]
                    track_info = match.get('metadata', {})
                    return RecognitionResult(
                        artist=track_info.get('artist', {}).get('name') or track_info.get('artists', [{}])[0].get('name', 'Unknown'),
                        title=track_info.get('title', 'Unknown'),
                        confidence=0.85,
                        source="shazam",
                        metadata=result
                    )
            
            return None
            
        except Exception as e:
            print(f"Shazam error: {e}")
            return None

