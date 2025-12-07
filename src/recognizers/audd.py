"""Audd.io API integration"""

import os
import requests
from typing import Optional
from .base import BaseRecognizer, RecognitionResult
from ..utils.config import Config


class AuddRecognizer(BaseRecognizer):
    """Audd.io API recognizer"""
    
    API_URL = "https://api.audd.io/"
    
    def __init__(self):
        self.api_token = Config.AUDD_API_TOKEN
    
    def is_available(self) -> bool:
        """Check if Audd.io API is configured"""
        return bool(self.api_token)
    
    def recognize(self, audio_file_path: str, start_time: float = 0.0, duration: float = 30.0) -> Optional[RecognitionResult]:
        """
        Recognize a track using Audd.io API
        
        Args:
            audio_file_path: Path to the audio file
            start_time: Start time in seconds (not used for Audd.io)
            duration: Duration of segment in seconds (not used for Audd.io)
            
        Returns:
            RecognitionResult if track found, None otherwise
        """
        if not self.is_available():
            return None
        
        try:
            # Read audio file and prepare for upload
            with open(audio_file_path, 'rb') as f:
                audio_data = f.read()
            
            files = {
                'file': (os.path.basename(audio_file_path), audio_data, 'audio/mpeg')
            }
            data = {
                'api_token': self.api_token,
                'return': 'spotify,apple_music,deezer'
            }
            
            # Make API request
            response = requests.post(self.API_URL, files=files, data=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # Parse response
            if result.get('status') == 'success' and result.get('result'):
                track = result['result']
                return RecognitionResult(
                    artist=track.get('artist'),
                    title=track.get('title'),
                    confidence=float(track.get('score', 0)) / 100.0 if track.get('score') else 0.0,
                    source="audd",
                    metadata=track
                )
            
            return None
            
        except Exception as e:
            # Log error but don't raise (allow graceful failure)
            print(f"Audd.io error: {e}")
            return None

