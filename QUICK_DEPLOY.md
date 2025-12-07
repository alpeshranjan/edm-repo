# Quick Deploy to Render

## Steps:

1. **Go to**: https://render.com
2. **Sign up** (free with GitHub)
3. **Click "New +" → "Web Service"**
4. **Connect GitHub** and select `edm-repo`
5. **Settings**:
   - Name: `edm-track-recognizer`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
6. **Environment Variables** (click "Advanced"):
   - `ACRCLOUD_ACCESS_KEY` = your key
   - `ACRCLOUD_SECRET_KEY` = your secret
   - `AUDD_API_TOKEN` = your token (optional)
7. **Click "Create Web Service"**
8. **Wait 5-10 minutes** for deployment
9. **Done!** Your site will be live at: `https://edm-track-recognizer.onrender.com`

That's it!

