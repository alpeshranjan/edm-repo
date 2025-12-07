# Performance Tips

## Why Processing Takes Time

**For a 52-minute mix:**
- ~106 segments (with 45s segments)
- Each segment = 3-5 seconds (API call + processing)
- Total time: **6-8 minutes**

## Ways to Speed It Up

### 1. Use Longer Segments
- Default: 45 seconds
- Faster: 60 seconds = fewer segments = faster processing
- Trade-off: Might miss some tracks

### 2. Increase Confidence Threshold
- Lower threshold = more API calls (tries fallback more)
- Higher threshold = fewer calls = faster

### 3. Process Smaller Files
- 10-minute mix = ~1-2 minutes
- 30-minute mix = ~3-4 minutes
- 52-minute mix = ~6-8 minutes

### 4. For Render Build
- First build: 5-10 minutes (normal)
- Free tier: Can be slower
- Subsequent deploys: Faster (2-3 minutes)

## Expected Times

| File Length | Processing Time |
|-------------|----------------|
| 10 minutes  | 1-2 minutes    |
| 30 minutes  | 3-4 minutes    |
| 52 minutes  | 6-8 minutes    |

## If It's Really Slow

1. **Check Render logs** - See if there are errors
2. **Check API rate limits** - Free tier has limits
3. **Try smaller file first** - Test with 5-10 minute mix
4. **Check internet connection** - API calls need good connection

