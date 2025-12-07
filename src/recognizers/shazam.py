"""Shazam API integration"""

import requests
from typing import Optional
from .base import BaseRecognizer, RecognitionResult
from ..utils.config import Config


class ShazamRecognizer(BaseRecognizer):
    """Shazam API recognizer"""
    
    API_URL = "https://shazam-api.com/v1/search"
    
    def __init__(self):
        self.api_key = getattr(Config, 'SHAZAM_API_KEY', None)
    
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
                    'file': (audio_file_path, f, 'audio/mpeg')
                }
                data = {
                    'api_key': self.api_key
                }
                
                # Make API request
                response = requests.post(self.API_URL, files=files, data=data, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                
                # Parse response (adjust based on actual Shazam API response format)
                if result.get('status') == 'success' and result.get('track'):
                    track = result['track']
                    return RecognitionResult(
                        artist=track.get('artist', {}).get('name') or track.get('subtitle'),
                        title=track.get('title'),
                        confidence=float(track.get('match', 0)) / 100.0 if track.get('match') else 0.8,  # Default high confidence
                        source="shazam",
                        metadata=track
                    )
            
            return None
            
        except Exception as e:
            print(f"Shazam error: {e}")
            return None

