"""Base recognizer interface"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class RecognitionResult:
    """Result from track recognition"""
    artist: Optional[str] = None
    title: Optional[str] = None
    confidence: float = 0.0
    source: str = "unknown"
    metadata: Optional[Dict[str, Any]] = None


class BaseRecognizer(ABC):
    """Base class for all recognition backends"""
    
    @abstractmethod
    def recognize(self, audio_file_path: str, start_time: float = 0.0, duration: float = 30.0) -> Optional[RecognitionResult]:
        """
        Recognize a track from an audio file segment
        
        Args:
            audio_file_path: Path to the audio file
            start_time: Start time in seconds
            duration: Duration of segment in seconds
            
        Returns:
            RecognitionResult if track found, None otherwise
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the recognizer is available (API keys configured)"""
        pass

