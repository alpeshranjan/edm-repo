#!/bin/bash
# Script to push to GitHub repository "edm repo"

cd "/Users/alpesh/Downloads/untitled folder 2"

echo "=== Setting up GitHub remote ==="
echo ""
echo "Please make sure you've created the repository 'edm repo' on GitHub first!"
echo "Go to: https://github.com/new"
echo "Repository name: edm repo"
echo "Then press Enter to continue..."
read

echo ""
echo "What is your GitHub username?"
read GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "Error: GitHub username is required"
    exit 1
fi

echo ""
echo "Adding remote and pushing..."
git remote add origin "https://github.com/${GITHUB_USERNAME}/edm-repo.git" 2>/dev/null || git remote set-url origin "https://github.com/${GITHUB_USERNAME}/edm-repo.git"
git branch -M main
git push -u origin main

echo ""
echo "Done! Check your repository at: https://github.com/${GITHUB_USERNAME}/edm-repo"

