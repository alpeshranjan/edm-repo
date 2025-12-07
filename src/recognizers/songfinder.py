"""SongFinder API integration"""

import requests
from typing import Optional
from .base import BaseRecognizer, RecognitionResult
from ..utils.config import Config


class SongFinderRecognizer(BaseRecognizer):
    """SongFinder API recognizer"""
    
    API_URL = "https://api.songfinder.gg/v1/recognize"
    
    def __init__(self):
        self.api_key = getattr(Config, 'SONGFINDER_API_KEY', None)
    
    def is_available(self) -> bool:
        """Check if SongFinder API is configured"""
        return bool(self.api_key)
    
    def recognize(self, audio_file_path: str, start_time: float = 0.0, duration: float = 30.0) -> Optional[RecognitionResult]:
        """
        Recognize a track using SongFinder API
        
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
                    'audio': (audio_file_path, f, 'audio/mpeg')
                }
                headers = {
                    'Authorization': f'Bearer {self.api_key}'
                }
                
                # Make API request
                response = requests.post(self.API_URL, files=files, headers=headers, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                
                # Parse response (adjust based on actual API response format)
                if result.get('success') and result.get('track'):
                    track = result['track']
                    return RecognitionResult(
                        artist=track.get('artist'),
                        title=track.get('title'),
                        confidence=float(track.get('confidence', 0)) / 100.0 if track.get('confidence') else 0.7,
                        source="songfinder",
                        metadata=track
                    )
            
            return None
            
        except Exception as e:
            print(f"SongFinder error: {e}")
            return None

