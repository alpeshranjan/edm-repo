# How to Add FFmpeg Buildpack on Render

## Step-by-Step Instructions

### Method 1: Using Render Dashboard (Recommended)

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Log in to your account

2. **Select Your Service**
   - Click on your service: **"edm-repo"** (or whatever you named it)

3. **Go to Settings**
   - Click on **"Settings"** tab (in the left sidebar or top menu)

4. **Find Buildpacks Section**
   - Scroll down to find **"Buildpacks"** section
   - It might be under "Build & Deploy" or "Build Settings"

5. **Add Buildpack**
   - Click **"Add Buildpack"** or **"Add buildpack"** button
   - In the input field, paste this URL:
     ```
     https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest
     ```
   - Click **"Save"** or **"Add"**

6. **Redeploy**
   - Render will automatically start a new deployment
   - Or click **"Manual Deploy"** → **"Deploy latest commit"**
   - Wait 3-5 minutes for deployment to complete

### Method 2: Using render.yaml (Alternative)

If you prefer to configure it in code:

1. **Edit render.yaml** (if you have one)
   - Add this to your service configuration:
   ```yaml
   services:
     - type: web
       name: edm-repo
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
       buildpacks:
         - https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest
   ```

2. **Push to GitHub**
   - Render will auto-detect and use it

## Verify FFmpeg is Installed

After deployment, check the build logs:

1. Go to your service → **"Logs"** tab
2. Look for build logs
3. You should see something like:
   ```
   -----> FFmpeg app detected
   -----> Installing FFmpeg
   ```

Or test in the app:
- The app will now use FFmpeg instead of librosa fallback
- No more memory crashes!

## Troubleshooting

### Can't Find Buildpacks Section?
- Some Render plans don't show buildpacks in UI
- Try Method 2 (render.yaml) instead
- Or contact Render support

### Buildpack Not Working?
- Make sure the URL is exactly: `https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest`
- Check build logs for errors
- Try redeploying

### Still Getting Memory Errors?
- Check if FFmpeg is actually installed (check build logs)
- Make sure file is under 50MB
- Check Render logs for FFmpeg errors

## What This Does

- **Installs FFmpeg** during the build process
- **Enables memory-efficient** audio processing
- **Prevents crashes** from loading entire files
- **Required** for the app to work properly

After adding the buildpack and redeploying, your app should work without memory issues!

