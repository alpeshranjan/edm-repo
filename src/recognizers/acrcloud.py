"""ACRCloud API integration"""

import os
import time
import hmac
import hashlib
import base64
import requests
from typing import Optional
from .base import BaseRecognizer, RecognitionResult
from ..utils.config import Config


class ACRCloudRecognizer(BaseRecognizer):
    """ACRCloud API recognizer"""
    
    # ACRCloud uses region-specific endpoints
    # Common regions: us-west-2, eu-west-1, ap-southeast-1
    # Try multiple regions if one fails
    API_REGIONS = [
        "us-west-2",
        "eu-west-1", 
        "ap-southeast-1",
        "us-east-1"
    ]
    API_URL = f"https://identify-{API_REGIONS[0]}.acrcloud.com/v1/identify"
    
    def __init__(self):
        self.access_key = Config.ACRCLOUD_ACCESS_KEY
        self.secret_key = Config.ACRCLOUD_SECRET_KEY
    
    def is_available(self) -> bool:
        """Check if ACRCloud API is configured"""
        return bool(self.access_key and self.secret_key)
    
    def _generate_signature(self, http_method: str, uri: str, access_key: str, secret_key: str, data_type: str, signature_version: str) -> str:
        """Generate ACRCloud API signature"""
        timestamp = str(int(time.time()))
        string_to_sign = f"{http_method}\n{uri}\n{access_key}\n{data_type}\n{signature_version}\n{timestamp}"
        sign = base64.b64encode(
            hmac.new(secret_key.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha1).digest()
        ).decode('utf-8')
        return sign
    
    def recognize(self, audio_file_path: str, start_time: float = 0.0, duration: float = 30.0) -> Optional[RecognitionResult]:
        """
        Recognize a track using ACRCloud API
        
        Args:
            audio_file_path: Path to the audio file
            start_time: Start time in seconds (not used for ACRCloud, processes full file)
            duration: Duration of segment in seconds (not used for ACRCloud)
            
        Returns:
            RecognitionResult if track found, None otherwise
        """
        if not self.is_available():
            return None
        
        try:
            # Read audio file
            with open(audio_file_path, 'rb') as f:
                audio_data = f.read()
            
            # Generate signature
            http_method = "POST"
            uri = "/v1/identify"
            data_type = "audio"
            signature_version = "1"
            timestamp = str(int(time.time()))
            signature = self._generate_signature(
                http_method, uri, self.access_key, self.secret_key, data_type, signature_version
            )
            
            # Prepare request
            files = {
                'sample': (os.path.basename(audio_file_path), audio_data, 'audio/mpeg')
            }
            data = {
                'access_key': self.access_key,
                'data_type': data_type,
                'signature_version': signature_version,
                'signature': signature,
                'sample_bytes': str(len(audio_data)),
                'timestamp': timestamp
            }
            
            # Make API request - try multiple regions if needed
            last_error = None
            response = None
            for region in self.API_REGIONS:
                api_url = f"https://identify-{region}.acrcloud.com/v1/identify"
                try:
                    response = requests.post(api_url, files=files, data=data, timeout=30)
                    response.raise_for_status()
                    break  # Success, exit loop
                except requests.exceptions.HTTPError as e:
                    last_error = e
                    if response and response.status_code == 404:
                        # Try next region
                        continue
                    else:
                        # Other error, raise it
                        raise
                except Exception as e:
                    last_error = e
                    continue
            
            # If all regions failed, raise the last error
            if not response or response.status_code != 200:
                raise last_error or Exception("All API regions failed")
            
            result = response.json()
            
            # Parse response
            if result.get('status', {}).get('code') == 0:
                metadata = result.get('metadata', {})
                music = metadata.get('music', [])
                
                if music and len(music) > 0:
                    track = music[0]
                    return RecognitionResult(
                        artist=track.get('artists', [{}])[0].get('name') if track.get('artists') else None,
                        title=track.get('title'),
                        confidence=float(track.get('score', 0)) / 100.0 if track.get('score') else 0.0,
                        source="acrcloud",
                        metadata=track
                    )
            
            return None
            
        except Exception as e:
            # Log error but don't raise (allow fallback to other recognizers)
            import traceback
            error_msg = str(e)
            if "404" in error_msg:
                print(f"ACRCloud error: {error_msg} (endpoint not found)")
            elif "401" in error_msg or "403" in error_msg:
                print(f"ACRCloud error: {error_msg} (authentication failed - check API keys)")
            else:
                print(f"ACRCloud error: {error_msg}")
            return None

