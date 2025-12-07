"""AI-powered API orchestrator for intelligent track recognition"""

import json
import requests
from typing import List, Optional, Dict, Any
from ..recognizers.base import RecognitionResult
from ..utils.config import Config


class AIOrchestrator:
    """AI-powered orchestrator for intelligent API coordination"""
    
    # Free LLM API options
    HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
    
    def __init__(self):
        self.huggingface_key = getattr(Config, 'HUGGINGFACE_API_KEY', None)
        self.together_key = getattr(Config, 'TOGETHER_API_KEY', None)
        self.openai_key = getattr(Config, 'OPENAI_API_KEY', None)
    
    def is_available(self) -> bool:
        """Check if any AI service is available"""
        return bool(self.huggingface_key or self.together_key or self.openai_key)
    
    def validate_and_rank_results(self, results: List[RecognitionResult], audio_context: Optional[Dict] = None) -> List[RecognitionResult]:
        """
        Use AI to validate and rank results from multiple APIs
        
        Args:
            results: List of recognition results from different APIs
            audio_context: Optional context about the audio (genre, BPM, etc.)
            
        Returns:
            Ranked list of validated results
        """
        if not self.is_available() or not results:
            # Fallback to simple confidence-based ranking
            return sorted(results, key=lambda r: r.confidence, reverse=True)
        
        if len(results) == 1:
            return results
        
        # Use AI to validate and rank
        try:
            ranked = self._ai_validate_results(results, audio_context)
            return ranked if ranked else sorted(results, key=lambda r: r.confidence, reverse=True)
        except Exception as e:
            print(f"[AI] Validation failed: {e}, using fallback")
            return sorted(results, key=lambda r: r.confidence, reverse=True)
    
    def _ai_validate_results(self, results: List[RecognitionResult], audio_context: Optional[Dict]) -> Optional[List[RecognitionResult]]:
        """Use AI to validate results"""
        # Prepare results for AI analysis
        results_data = []
        for r in results:
            results_data.append({
                'artist': r.artist or 'Unknown',
                'title': r.title or 'Unknown',
                'confidence': r.confidence,
                'source': r.source
            })
        
        prompt = f"""You are a music recognition expert. Analyze these track recognition results from different APIs and rank them by accuracy and relevance.

Results:
{json.dumps(results_data, indent=2)}

Context: {json.dumps(audio_context or {}, indent=2)}

Task:
1. Identify which results are likely the same track (even if metadata differs slightly)
2. Rank results by confidence and accuracy
3. Flag any results that seem incorrect or mismatched
4. Return a JSON array with ranked results, each with: artist, title, confidence_score (0-1), is_valid (true/false), reason

Return ONLY valid JSON, no other text."""

        # Try different AI services
        response = None
        
        # Try Together AI first (good free tier)
        if self.together_key:
            response = self._call_together_ai(prompt)
        
        # Try Hugging Face
        if not response and self.huggingface_key:
            response = self._call_huggingface(prompt)
        
        # Try OpenAI
        if not response and self.openai_key:
            response = self._call_openai(prompt)
        
        if not response:
            return None
        
        # Parse AI response and reorder results
        try:
            ranked_data = json.loads(response)
            if isinstance(ranked_data, list):
                # Create mapping and reorder
                result_map = {f"{r.artist}-{r.title}": r for r in results}
                ranked_results = []
                for item in ranked_data:
                    key = f"{item.get('artist')}-{item.get('title')}"
                    if key in result_map and item.get('is_valid', True):
                        ranked_results.append(result_map[key])
                return ranked_results if ranked_results else None
        except:
            pass
        
        return None
    
    def _call_together_ai(self, prompt: str) -> Optional[str]:
        """Call Together AI API (fast, optimized)"""
        try:
            headers = {
                'Authorization': f'Bearer {self.together_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'model': 'mistralai/Mixtral-8x7B-Instruct-v0.1',
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.2,  # Lower = faster, more deterministic
                'max_tokens': 300,  # Reduced for speed
                'stop': ['\n\n']  # Stop early if possible
            }
            response = requests.post(self.TOGETHER_API_URL, json=data, headers=headers, timeout=5)  # Shorter timeout
            if response.status_code == 200:
                result = response.json()
                return result.get('choices', [{}])[0].get('message', {}).get('content')
        except Exception as e:
            print(f"[AI] Together AI error: {e}")
        return None
    
    def _call_huggingface(self, prompt: str) -> Optional[str]:
        """Call Hugging Face Inference API (fast)"""
        try:
            headers = {'Authorization': f'Bearer {self.huggingface_key}'}
            data = {'inputs': prompt, 'parameters': {'max_new_tokens': 200, 'temperature': 0.2}}
            response = requests.post(self.HUGGINGFACE_API_URL, json=data, headers=headers, timeout=8)  # Shorter timeout
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '')
        except Exception as e:
            print(f"[AI] Hugging Face error: {e}")
        return None
    
    def _call_openai(self, prompt: str) -> Optional[str]:
        """Call OpenAI API (fast, optimized)"""
        try:
            headers = {
                'Authorization': f'Bearer {self.openai_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.2,  # Lower = faster
                'max_tokens': 300  # Reduced for speed
            }
            response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers, timeout=5)
            if response.status_code == 200:
                result = response.json()
                return result.get('choices', [{}])[0].get('message', {}).get('content')
        except Exception as e:
            print(f"[AI] OpenAI error: {e}")
        return None
    
    def smart_deduplicate(self, tracks: List[Dict]) -> List[Dict]:
        """
        Use AI to intelligently deduplicate tracks
        Understands remixes, edits, and variations
        """
        if not self.is_available() or len(tracks) <= 1:
            # Fallback to simple deduplication
            from ..utils.track_utils import deduplicate_tracks
            return deduplicate_tracks(tracks)
        
        # Use AI for smart deduplication
        try:
            return self._ai_deduplicate(tracks)
        except Exception as e:
            print(f"[AI] Smart deduplication failed: {e}, using fallback")
            from ..utils.track_utils import deduplicate_tracks
            return deduplicate_tracks(tracks)
    
    def _ai_deduplicate(self, tracks: List[Dict]) -> List[Dict]:
        """Use AI to deduplicate tracks intelligently"""
        prompt = f"""Analyze these music tracks and identify which are duplicates or variations of the same track (remixes, edits, extended versions, etc.).

Tracks:
{json.dumps(tracks, indent=2)}

Return a JSON array with only unique tracks. Group variations together and keep the best/most complete version.

Return ONLY valid JSON array, no other text."""

        # Try AI services
        response = None
        if self.together_key:
            response = self._call_together_ai(prompt)
        elif self.huggingface_key:
            response = self._call_huggingface(prompt)
        elif self.openai_key:
            response = self._call_openai(prompt)
        
        if response:
            try:
                unique = json.loads(response)
                if isinstance(unique, list):
                    return unique
            except:
                pass
        
        # Fallback
        from ..utils.track_utils import deduplicate_tracks
        return deduplicate_tracks(tracks)

