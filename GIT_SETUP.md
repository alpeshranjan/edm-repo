# Git Setup Instructions

Your repository is initialized and ready to push! Follow these steps:

## Option 1: Push to GitHub (Recommended)

### 1. Create a new repository on GitHub
- Go to https://github.com/new
- Repository name: `edm-track-recognizer` (or any name you prefer)
- Description: "CLI tool to identify tracks from continuous EDM/techno mixes"
- Choose Public or Private
- **DO NOT** initialize with README, .gitignore, or license (we already have these)
- Click "Create repository"

### 2. Add the remote and push
```bash
cd "/Users/alpesh/Downloads/untitled folder 2"

# Add your GitHub repository as remote (replace USERNAME and REPO_NAME)
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Example:
```bash
git remote add origin https://github.com/alpesh/edm-track-recognizer.git
git branch -M main
git push -u origin main
```

## Option 2: Push to existing repository

If you already have a repository:
```bash
cd "/Users/alpesh/Downloads/untitled folder 2"
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

## Future Updates

After making changes:
```bash
git add .
git commit -m "Description of changes"
git push
```

## Important Notes

- ✅ `.env` file is already in `.gitignore` (your API keys are safe)
- ✅ `venv/` is ignored (virtual environment)
- ✅ Generated output files (tracklist.md, etc.) are ignored
- ✅ All source code and documentation is included

## Quick Commands Reference

```bash
# Check status
git status

# See what files changed
git diff

# Add all changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push

# Pull latest changes
git pull
```

