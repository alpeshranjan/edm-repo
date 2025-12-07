# Additional API Integration Guide

I've added support for **Shazam** and **SongFinder** APIs to improve underground track recognition.

## New APIs Added

### 1. Shazam API
- **Coverage**: Excellent for mainstream and popular tracks
- **Underground**: Good coverage, better than Audd.io
- **Get API Key**: https://shazam-api.com
- **Cost**: Check their pricing

### 2. SongFinder API  
- **Coverage**: Specialized for underground/electronic music
- **Underground**: Best option for techno/EDM underground tracks
- **Get API Key**: https://songfinder.gg/api
- **Cost**: Check their pricing

## How to Add API Keys

### For Local Use (.env file):
```bash
SHAZAM_API_KEY=your_shazam_key_here
SONGFINDER_API_KEY=your_songfinder_key_here
```

### For Render Deployment:
Add as Environment Variables:
- `SHAZAM_API_KEY` = your key
- `SONGFINDER_API_KEY` = your key

## How It Works

The tool now tries APIs in this order:
1. **ACRCloud** (primary - best underground coverage you have)
2. **Shazam** (if ACRCloud fails or low confidence)
3. **SongFinder** (if still no good match - specialized for underground)
4. **Audd.io** (last fallback)

This gives you **4 chances** to find each track!

## Current Status

- ✅ ACRCloud: Configured and working
- ❌ Shazam: Not configured (optional)
- ❌ SongFinder: Not configured (optional)
- ❌ Audd.io: Not configured (optional)

**You only need ACRCloud to work**, but adding Shazam and SongFinder will significantly improve results for underground tracks.

## Getting API Keys

### Shazam:
1. Go to: https://shazam-api.com
2. Sign up and get API key
3. Add to `.env` or Render environment variables

### SongFinder:
1. Go to: https://songfinder.gg/api
2. Sign up and get API key  
3. Add to `.env` or Render environment variables

## Testing

After adding keys, check status:
```
https://your-site.onrender.com/api/status
```

Should show all APIs as available.

