"""Audio processing and segmentation"""

import os
import tempfile
import librosa
import soundfile as sf
from typing import List, Tuple, Optional
from pathlib import Path


class AudioProcessor:
    """Handle audio file loading, segmentation, and processing"""
    
    SUPPORTED_FORMATS = {'.mp3', '.wav', '.flac', '.m4a', '.ogg', '.aac'}
    
    def __init__(self, segment_length: int = 45, segment_overlap: int = 15):
        """
        Initialize audio processor
        
        Args:
            segment_length: Length of each segment in seconds
            segment_overlap: Overlap between segments in seconds
        """
        self.segment_length = segment_length
        self.segment_overlap = segment_overlap
    
    def is_supported_format(self, file_path: str) -> bool:
        """Check if file format is supported"""
        ext = Path(file_path).suffix.lower()
        return ext in self.SUPPORTED_FORMATS
    
    def get_duration(self, file_path: str) -> float:
        """Get duration of audio file in seconds"""
        try:
            y, sr = librosa.load(file_path, sr=None, duration=0.1)
            duration = librosa.get_duration(path=file_path)
            return duration
        except Exception as e:
            raise ValueError(f"Could not read audio file: {e}")
    
    def segment_audio(self, file_path: str) -> List[Tuple[float, float]]:
        """
        Segment audio file into overlapping windows
        
        Returns:
            List of (start_time, end_time) tuples in seconds
        """
        duration = self.get_duration(file_path)
        segments = []
        
        start = 0.0
        while start < duration:
            end = min(start + self.segment_length, duration)
            segments.append((start, end))
            start += (self.segment_length - self.segment_overlap)
        
        return segments
    
    def extract_segment(self, file_path: str, start_time: float, duration: float, output_path: Optional[str] = None) -> str:
        """
        Extract a segment from audio file using FFmpeg (memory efficient)
        
        Args:
            file_path: Path to source audio file
            start_time: Start time in seconds
            duration: Duration of segment in seconds
            output_path: Optional output path (creates temp file if not provided)
            
        Returns:
            Path to extracted segment file
        """
        try:
            # Use FFmpeg for memory-efficient extraction (doesn't load full file)
            import subprocess
            
            # Create output file if not provided
            if output_path is None:
                fd, output_path = tempfile.mkstemp(suffix='.wav', prefix='segment_')
                os.close(fd)
            
            # Use FFmpeg to extract segment directly (much more memory efficient)
            cmd = [
                'ffmpeg',
                '-i', file_path,
                '-ss', str(start_time),
                '-t', str(duration),
                '-ar', '22050',  # Sample rate
                '-ac', '1',  # Mono
                '-y',  # Overwrite output
                output_path
            ]
            
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30
            )
            
            if result.returncode != 0:
                # Fallback to librosa if FFmpeg fails
                y, sr = librosa.load(
                    file_path,
                    offset=start_time,
                    duration=duration,
                    sr=22050
                )
                sf.write(output_path, y, sr)
            else:
                # Verify file was created
                if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                    # Fallback to librosa
                    y, sr = librosa.load(
                        file_path,
                        offset=start_time,
                        duration=duration,
                        sr=22050
                    )
                    sf.write(output_path, y, sr)
            
            return output_path
            
        except Exception as e:
            # Final fallback to librosa
            try:
                y, sr = librosa.load(
                    file_path,
                    offset=start_time,
                    duration=duration,
                    sr=22050
                )
                if output_path is None:
                    fd, output_path = tempfile.mkstemp(suffix='.wav', prefix='segment_')
                    os.close(fd)
                sf.write(output_path, y, sr)
                return output_path
            except Exception as e2:
                raise ValueError(f"Could not extract segment: {e2}")
    
    def convert_to_wav(self, file_path: str, output_path: Optional[str] = None) -> str:
        """
        Convert audio file to WAV format (for API compatibility)
        
        Args:
            file_path: Path to source audio file
            output_path: Optional output path (creates temp file if not provided)
            
        Returns:
            Path to converted WAV file
        """
        try:
            # Load audio
            y, sr = librosa.load(file_path, sr=22050)
            
            # Create output file if not provided
            if output_path is None:
                fd, output_path = tempfile.mkstemp(suffix='.wav', prefix='converted_')
                os.close(fd)
            
            # Save as WAV
            sf.write(output_path, y, sr)
            
            return output_path
            
        except Exception as e:
            raise ValueError(f"Could not convert audio file: {e}")

