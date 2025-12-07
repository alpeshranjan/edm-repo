# AI Orchestrator Setup Guide

## What It Does

The AI orchestrator intelligently:
- ✅ **Validates results** from multiple APIs
- ✅ **Ranks results** by accuracy (not just confidence)
- ✅ **Smart deduplication** - understands remixes, edits, versions
- ✅ **Detects false positives** - filters out incorrect matches
- ✅ **Works automatically** - no manual configuration needed

## Free AI API Options

### Option 1: Together AI (Recommended - Best Free Tier)
1. Go to: https://together.ai
2. Sign up (free account)
3. Go to API Keys: https://api.together.xyz/settings/api-keys
4. Create new API key
5. Copy the key

**Free tier**: Generous free credits per month

### Option 2: Hugging Face (Free)
1. Go to: https://huggingface.co
2. Sign up (free)
3. Go to Settings → Access Tokens: https://huggingface.co/settings/tokens
4. Create new token (read permission)
5. Copy the token

**Free tier**: Free but may be slower

### Option 3: OpenAI (Paid - Best Quality)
1. Go to: https://platform.openai.com
2. Sign up
3. Go to API Keys: https://platform.openai.com/api-keys
4. Create new key
5. Copy the key

**Cost**: Pay per use (~$0.002 per request)

## Setup

### For Local Use (.env file):
```bash
# Add to your .env file
TOGETHER_API_KEY=your_together_key_here
# OR
HUGGINGFACE_API_KEY=your_huggingface_token_here
# OR
OPENAI_API_KEY=your_openai_key_here
```

### For Render Deployment:
1. Go to Render dashboard → Your service → Environment
2. Add environment variable:
   - Key: `TOGETHER_API_KEY` (or `HUGGINGFACE_API_KEY` or `OPENAI_API_KEY`)
   - Value: Your API key
3. Save (auto-redeploys)

## How It Works

1. **Multiple APIs return results** → ACRCloud, Shazam, SongFinder, Audd
2. **AI analyzes all results** → Validates, ranks, filters
3. **Best result selected** → Most accurate, not just highest confidence
4. **Smart deduplication** → Groups remixes/edits together

## Benefits

- **Higher accuracy**: AI validates results, reduces false positives
- **Better for underground**: AI understands context better
- **Smarter deduplication**: Knows when tracks are variations
- **Automatic**: Works seamlessly, falls back if AI unavailable

## Testing

After adding API key:
1. Process a file
2. Check logs for `[AI]` messages
3. Should see: `[AI] Validated and ranked X results`
4. Results should be more accurate!

## Optional

AI is **completely optional** - the app works fine without it. But with AI, you get:
- Better accuracy
- Smarter deduplication
- Fewer false positives

Try it and see the difference! 🚀

