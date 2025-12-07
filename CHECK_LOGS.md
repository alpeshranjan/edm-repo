# How to Check Render Logs for API Activity

## What You Just Saw

The logs show:
- ✅ Site is loading (GET / returns 200)
- ✅ Static files loading (main.js, style.css)
- ⚠️ Then shutdown - this is **normal** if Render is redeploying

## Next Steps

### 1. Wait for Redeploy to Finish
- Render is probably redeploying after the latest push
- Wait 2-3 minutes
- Check if site is back up: https://edm-repo.onrender.com

### 2. Test the API
Once site is back up:
1. Upload a file
2. **Watch the logs in real-time** (keep Render logs tab open)
3. Look for these log lines:

```
[MAIN] Processing X segments...
[MAIN] API Status - ACRCloud: True, Shazam: False...
[API] Calling ACRCloud for segment 0.0-45.0...
[ACRCloud] Trying region us-west-2...
[ACRCloud] Response status: 200
[ACRCloud] ✓ Found: Artist - Title
```

### 3. What to Look For

**Good signs:**
- `[ACRCloud] Response status: 200` - API is working
- `[ACRCloud] ✓ Found: Artist - Title` - Track found!
- `[ACRCloud] Status code: 0` - Success

**Bad signs:**
- `[ACRCloud] Response status: 401` or `403` - **API keys wrong**
- `[ACRCloud] Response status: 404` - Endpoint issue
- `[ACRCloud] ✗ Region ... exception` - Connection error
- `Status code: 3001` - No match (normal, just means track not in database)

### 4. If You See Errors

**401/403 Error:**
- API keys are incorrect
- Check Render → Environment → ACRCLOUD_ACCESS_KEY and ACRCLOUD_SECRET_KEY
- Make sure no extra spaces

**404 Error:**
- Endpoint issue (should try other regions automatically)
- Check if all regions fail

**No API calls at all:**
- Check if `[MAIN] API Status` shows `ACRCloud: True`
- If False, API keys not set

## Quick Test

1. Visit: https://edm-repo.onrender.com/api/status
2. Should return JSON with `"acrcloud_available": true`
3. If false, API keys aren't set correctly

## Share the Logs

After uploading a file, copy the logs that show:
- `[MAIN]` lines
- `[API]` lines  
- `[ACRCloud]` lines

This will show exactly what's happening!

