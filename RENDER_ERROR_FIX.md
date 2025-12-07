# Fix "The string did not match the expected pattern" Error

This error in Render is usually from the **Start Command** format.

## Solution

1. Go to Render dashboard → Your service → **Settings**
2. Scroll to **"Build & Deploy"** section
3. Check **"Start Command"** - it should be EXACTLY:

```
gunicorn app:app --bind 0.0.0.0:$PORT
```

**Common mistakes:**
- ❌ Extra spaces: `gunicorn  app:app` (two spaces)
- ❌ Missing `$PORT`: `gunicorn app:app --bind 0.0.0.0:5000`
- ❌ Wrong format: `python app.py`
- ❌ Trailing spaces

**Correct format:**
- ✅ `gunicorn app:app --bind 0.0.0.0:$PORT` (no extra spaces, use $PORT)

4. **Build Command** should be:
```
pip install -r requirements.txt
```

5. Click **"Save Changes"**
6. It will auto-redeploy

## Alternative: Delete and Recreate

If it still doesn't work:
1. Delete the current service
2. Create new one
3. Use the exact commands above
4. Make sure no extra characters/spaces

The Procfile in the repo is correct, so if Render auto-detects it, that should work too.

