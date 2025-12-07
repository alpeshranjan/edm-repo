# Render Deployment Fix

If you're getting "The string did not match the expected pattern" error:

## Solution 1: Check Render Settings

In Render dashboard, make sure:

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn app:app --bind 0.0.0.0:$PORT
```

**Important:** Make sure there are NO extra spaces or characters.

## Solution 2: Use render.yaml (Alternative)

If Procfile isn't working, you can use the `render.yaml` file I created. Render will auto-detect it.

## Solution 3: Manual Settings

1. Go to your Render service
2. Click "Settings"
3. Scroll to "Build & Deploy"
4. Make sure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Save and redeploy

## Common Issues

- **Extra spaces** in commands
- **Wrong Python version** (should be 3.11+)
- **Missing gunicorn** in requirements.txt (it's there, but check)
- **Port variable** - must use `$PORT` not a number

## Test Locally First

```bash
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:5000
```

If this works locally, the issue is in Render settings.

