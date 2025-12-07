# How to Get API Keys

This guide will walk you through getting API keys for both ACRCloud (primary) and Audd.io (optional fallback).

## ACRCloud (Primary - Recommended)

ACRCloud has the best coverage for underground techno tracks with 150M+ tracks in their database.

### Steps:

1. **Visit ACRCloud Website**
   - Go to: https://www.acrcloud.com
   - Click on "Sign Up" or "Get Started"

2. **Create an Account**
   - Provide your email address
   - Set a password
   - Complete the registration form

3. **Verify Your Email**
   - Check your email inbox
   - Click the verification link to activate your account

4. **Access the Dashboard**
   - Log in to: https://console.acrcloud.com (or the dashboard URL provided)
   - Navigate to "API Keys" or "Access Keys" section

5. **Get Your Credentials**
   - You'll need two values:
     - **Access Key** (also called Host or Access Key ID)
     - **Secret Key** (also called Access Secret)
   - Copy both values

6. **Free Tier Limits**
   - Free tier typically includes ~100 requests per day
   - For more usage, you may need to upgrade to a paid plan

### Add to .env file:
```bash
ACRCLOUD_ACCESS_KEY=your_access_key_here
ACRCLOUD_SECRET_KEY=your_secret_key_here
```

---

## Audd.io (Optional Fallback)

Audd.io can be used as a fallback when ACRCloud doesn't find a track.

### Steps:

1. **Visit Audd.io Website**
   - Go to: https://audd.io/
   - Click on "Sign Up for an API Token" or "Get Started"

2. **Create an Account**
   - Visit the dashboard: https://dashboard.audd.io/
   - Sign up with your email address and password

3. **Verify Your Email**
   - Check your email for a verification message
   - Click the verification link

4. **Get Your API Token**
   - Log in to the dashboard: https://dashboard.audd.io/
   - Your API token will be displayed on the main dashboard
   - Copy the token

5. **Free Tier Limits**
   - Free tier has limited requests per month
   - Check the dashboard for your current quota

### Add to .env file:
```bash
AUDD_API_TOKEN=your_api_token_here
```

---

## Setting Up Your .env File

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file** with your favorite text editor:
   ```bash
   nano .env
   # or
   vim .env
   # or open in any text editor
   ```

3. **Add your API keys:**
   ```bash
   # ACRCloud API Credentials (Required)
   ACRCLOUD_ACCESS_KEY=your_actual_access_key_here
   ACRCLOUD_SECRET_KEY=your_actual_secret_key_here

   # Audd.io API Credentials (Optional - for fallback)
   AUDD_API_TOKEN=your_actual_api_token_here

   # Optional: Configuration
   SEGMENT_LENGTH=45
   SEGMENT_OVERLAP=15
   CONFIDENCE_THRESHOLD=0.5
   ```

4. **Save the file** (make sure it's named exactly `.env`)

5. **Verify it's working:**
   ```bash
   source venv/bin/activate
   python -m src.cli --help
   ```

---

## Important Notes

- **Keep your API keys secret!** Never commit your `.env` file to version control
- The `.env` file is already in `.gitignore` to prevent accidental commits
- **ACRCloud is required** - the tool needs at least one API to work
- **Audd.io is optional** - it's only used as a fallback if ACRCloud doesn't find a match
- Free tiers have usage limits - check each service's dashboard for your quota

---

## Troubleshooting

### "Missing required API keys" error
- Make sure your `.env` file exists in the project root
- Verify the variable names match exactly (case-sensitive)
- Check that there are no extra spaces or quotes around the values

### "API error" messages
- Verify your API keys are correct
- Check if you've exceeded your free tier limits
- Make sure you have an internet connection

### Can't find API keys in dashboard
- Look for sections named: "API Keys", "Access Keys", "Credentials", or "Settings"
- Some dashboards require you to create/generate the keys first
- Check the service's documentation for the exact location

---

## Quick Links

- **ACRCloud**: https://www.acrcloud.com
- **ACRCloud Console**: https://console.acrcloud.com
- **Audd.io**: https://audd.io
- **Audd.io Dashboard**: https://dashboard.audd.io
- **Audd.io Documentation**: https://docs.audd.io

