# Debugging Web App - Not Recognizing Tracks

## Most Common Issue: API Keys Not Set

**Check in Render:**
1. Go to your Render service
2. Click "Environment" tab
3. Verify these are set:
   - `ACRCLOUD_ACCESS_KEY` = `1428547f09cdd87cf22d847390b6666c`
   - `ACRCLOUD_SECRET_KEY` = `yppcnQ75noT6fFGcNwWwkx7MmxT0P3kR8S0Xjz6N`
4. If missing, add them and **redeploy**

## Check API Status

Visit: `https://your-site.onrender.com/api/status`

Should return:
```json
{
  "acrcloud_available": true,
  "audd_available": false,
  "status": "ready"
}
```

If `acrcloud_available` is `false`, your API keys aren't set correctly.

## Check Render Logs

1. Go to Render dashboard
2. Click "Logs" tab
3. Look for errors like:
   - "ACRCloud error: 404"
   - "No recognition APIs available"
   - "API keys not configured"

## Test Steps

1. **Check status endpoint first**: `/api/status`
2. **Try a small file** (5-10 minutes, not 52 minutes)
3. **Check browser console** (F12) for JavaScript errors
4. **Check Render logs** for Python errors

## Quick Fix

If API keys aren't set:
1. Render dashboard → Your service → Environment
2. Add the two variables above
3. Save (auto-redeploys)
4. Wait 2-3 minutes
5. Try again

## If Still Not Working

Check the error message in the web interface - it should now show what's wrong.

