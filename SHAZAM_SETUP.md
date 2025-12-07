# Shazam API Setup Guide

## Getting Your Shazam API Key

The app uses **RapidAPI's Shazam API** (reliable third-party service).

### Step 1: Visit RapidAPI
Go to: **https://rapidapi.com/apidojo/api/shazam**

### Step 2: Sign Up / Get API Key
1. Click "Subscribe to Test" or "Subscribe" button
2. Create a RapidAPI account (free tier available)
3. Choose a plan (Free tier usually has limited requests)
4. After subscribing, you'll see your API key

### Step 3: Get Your API Key
1. On the RapidAPI Shazam page, look for **"X-RapidAPI-Key"** section
2. Copy the key (it's a long string starting with something like `abc123...`)
3. This is your `SHAZAM_API_KEY`

### Step 4: Add to Render

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Click on your service (edm-repo)

2. **Go to Environment Variables**
   - Click on "Environment" tab
   - Or go to Settings → Environment Variables

3. **Add New Variable**
   - Click "Add Environment Variable"
   - **Key**: `SHAZAM_API_KEY`
   - **Value**: Paste your API key from shazam-api.com
   - Click "Save Changes"

4. **Redeploy**
   - Render will automatically redeploy when you save
   - Wait 2-3 minutes for deployment

### Step 5: Verify It's Working

Check the status endpoint:
```
https://your-site.onrender.com/api/status
```

You should see:
```json
{
  "shazam_available": true,
  ...
}
```

## Alternative: If shazam-api.com doesn't work

If `shazam-api.com` is not available or requires payment, you can:

1. **Use RapidAPI Shazam**:
   - Go to: https://rapidapi.com/apidojo/api/shazam
   - Sign up and get API key
   - Update the code to use RapidAPI endpoint

2. **Skip Shazam** (optional):
   - The app works fine with just ACRCloud
   - Shazam is just an additional fallback for better coverage

## Current Status

After adding the key, Shazam will be used as a **fallback** when:
- ACRCloud doesn't find a match, OR
- ACRCloud finds a match but confidence is below threshold

This gives you better coverage for mainstream and popular tracks!

