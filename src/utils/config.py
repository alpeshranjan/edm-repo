"""Configuration management"""

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for API keys and settings"""
    
    # ACRCloud API credentials
    ACRCLOUD_ACCESS_KEY: Optional[str] = os.getenv("ACRCLOUD_ACCESS_KEY")
    ACRCLOUD_SECRET_KEY: Optional[str] = os.getenv("ACRCLOUD_SECRET_KEY")
    
    # Audd.io API credentials
    AUDD_API_TOKEN: Optional[str] = os.getenv("AUDD_API_TOKEN")
    
    # Processing settings
    SEGMENT_LENGTH: int = int(os.getenv("SEGMENT_LENGTH", "45"))
    SEGMENT_OVERLAP: int = int(os.getenv("SEGMENT_OVERLAP", "15"))
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))
    
    @classmethod
    def validate(cls) -> tuple[bool, list[str]]:
        """Validate that required API keys are set"""
        errors = []
        
        if not cls.ACRCLOUD_ACCESS_KEY:
            errors.append("ACRCLOUD_ACCESS_KEY not set")
        if not cls.ACRCLOUD_SECRET_KEY:
            errors.append("ACRCLOUD_SECRET_KEY not set")
        
        return len(errors) == 0, errors

