# Deployment Guide

## ⚠️ IMPORTANT: Install FFmpeg Buildpack First!

**Before deploying, you MUST add the FFmpeg buildpack in Render settings:**

1. Go to Render Dashboard → Your service → Settings
2. Find "Buildpacks" section
3. Add: `https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest`
4. Save and redeploy

**See `FFMPEG_SETUP.md` for detailed instructions.**

Without FFmpeg, the app will crash with memory errors!

## Quick Deploy to Render (Recommended)

1. **Push your code to GitHub** (already done: https://github.com/alpeshranjan/edm-repo)

2. **Go to Render**: https://render.com

3. **Create New Web Service**:
   - Connect your GitHub repository
   - Select `edm-repo`
   - Name: `edm-track-recognizer`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - Plan: Free tier is fine to start

4. **Add Environment Variables**:
   - Go to Environment tab
   - Add:
     - `ACRCLOUD_ACCESS_KEY` = your access key
     - `ACRCLOUD_SECRET_KEY` = your secret key
     - `AUDD_API_TOKEN` = your token (optional)

5. **Deploy!**

## Alternative: Deploy to Heroku

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

2. Login:
   ```bash
   heroku login
   ```

3. Create app:
   ```bash
   heroku create edm-track-recognizer
   ```

4. Set environment variables:
   ```bash
   heroku config:set ACRCLOUD_ACCESS_KEY=your_key
   heroku config:set ACRCLOUD_SECRET_KEY=your_secret
   heroku config:set AUDD_API_TOKEN=your_token
   ```

5. Deploy:
   ```bash
   git push heroku main
   ```

## Local Testing

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then visit: http://localhost:5000

## Notes

- Free tiers have limitations (file size, processing time)
- For production, consider upgrading to paid plans
- The app handles files up to 200MB
- Processing time depends on file length (1-2 minutes per 10 minutes of audio)

