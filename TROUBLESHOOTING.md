# Troubleshooting "Unknown error" and Other Issues

## What I Just Fixed

The app now shows **actual error messages** instead of "Unknown error". After Render redeploys, you'll see the real problem.

## Common Errors and Fixes

### 1. "No recognition APIs available"
**Problem**: API keys not set in Render

**Fix**:
1. Go to Render dashboard → Your service → Environment
2. Make sure these are set:
   - `ACRCLOUD_ACCESS_KEY`
   - `ACRCLOUD_SECRET_KEY`
3. Save and wait for redeploy (2-3 minutes)

**Check**: Visit `https://your-site.onrender.com/api/status`
- Should show `"acrcloud_available": true`

---

### 2. "Failed to process audio file" or "File may be corrupted"
**Problem**: Audio file format issue

**Fix**:
- Try a different file format (MP3, WAV, FLAC)
- Make sure file is not corrupted
- Try a smaller file first (under 50MB)

---

### 3. "Out of memory" or "SIGKILL"
**Problem**: File too large for Render free tier

**Fix**:
- Use smaller files (under 50MB recommended)
- Or upgrade Render plan for more RAM
- The app now limits to 200 segments max

---

### 4. "FFmpeg not found"
**Problem**: FFmpeg not installed on Render

**Fix**: 
- This should be auto-installed, but if not:
- Add buildpack: `https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest`
- Or contact Render support

---

### 5. "Failed to initialize API recognizers"
**Problem**: Missing Python dependencies

**Fix**:
- Check Render logs for missing module
- Make sure `requirements.txt` has all dependencies
- Redeploy to reinstall packages

---

### 6. "HTTP 500" or "Server error"
**Problem**: General server error

**Fix**:
1. **Check Render Logs**:
   - Go to Render dashboard → Your service → Logs
   - Look for Python error messages
   - Copy the error and check what it says

2. **Check Browser Console**:
   - Press F12 in browser
   - Go to "Console" tab
   - Look for JavaScript errors

3. **Check API Status**:
   - Visit: `https://your-site.onrender.com/api/status`
   - Verify APIs are configured

---

## How to Debug

### Step 1: Check Status Endpoint
```
https://your-site.onrender.com/api/status
```

Should return:
```json
{
  "acrcloud_available": true,
  "status": "ready"
}
```

### Step 2: Check Render Logs
1. Render dashboard → Your service
2. Click "Logs" tab
3. Look for error messages (red text)
4. Copy the full error message

### Step 3: Check Browser Console
1. Open your site
2. Press F12
3. Go to "Console" tab
4. Try uploading a file
5. Look for errors (red text)

### Step 4: Try a Small Test File
- Use a small MP3 file (5-10 minutes)
- Make sure it's a valid audio file
- Try different formats if one doesn't work

---

## Still Not Working?

1. **Check the actual error message** (should show now, not "Unknown error")
2. **Copy the full error** from browser or Render logs
3. **Check**:
   - API keys are set correctly
   - File format is supported (MP3, WAV, FLAC, M4A, OGG, AAC)
   - File size is reasonable (under 100MB)
   - Render service is running (not sleeping)

---

## Quick Test

1. Visit: `https://your-site.onrender.com/api/status`
2. Should return JSON with API status
3. If it works, APIs are configured
4. If it doesn't, check Render logs

---

## Most Common Issue

**90% of "Unknown error" cases are:**
- API keys not set in Render environment variables
- Or API keys are incorrect

**Fix**: Double-check your ACRCloud keys in Render → Environment tab

