# Push to GitHub - Quick Instructions

## Step 1: Create Repository on GitHub

1. Go to: **https://github.com/new**
2. Repository name: **edm repo** (or **edm-repo** if spaces cause issues)
3. Description: "CLI tool to identify tracks from continuous EDM/techno mixes"
4. Choose **Public** or **Private**
5. **DO NOT** check "Add a README file" (we already have one)
6. **DO NOT** check "Add .gitignore" (we already have one)
7. Click **"Create repository"**

## Step 2: Push Your Code

After creating the repository, run these commands:

```bash
cd "/Users/alpesh/Downloads/untitled folder 2"

# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/edm-repo.git
git branch -M main
git push -u origin main
```

### Or use the automated script:
```bash
cd "/Users/alpesh/Downloads/untitled folder 2"
./push_to_github.sh
```

## Note about repository name

GitHub doesn't allow spaces in repository names, so:
- If you named it **"edm repo"** on GitHub, it becomes **"edm-repo"** in the URL
- Use **"edm-repo"** in the git commands above

## Example

If your GitHub username is `alpesh`:
```bash
git remote add origin https://github.com/alpesh/edm-repo.git
git branch -M main
git push -u origin main
```

## Troubleshooting

### "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/edm-repo.git
```

### Authentication required
- GitHub may ask for your username and password
- For password, use a **Personal Access Token** (not your GitHub password)
- Create token at: https://github.com/settings/tokens
- Select scope: `repo`

### "repository not found"
- Make sure you created the repository on GitHub first
- Check the repository name matches (use `edm-repo` not `edm repo` in URL)

