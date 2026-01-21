# GitHub Setup Guide

This guide will help you upload the Jira Auto Reply Agent to GitHub.

## Prerequisites

- Git installed (✅ Already installed: git version 2.49.0)
- GitHub account
- GitHub repository created (public or private)

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Fill in repository details:
   - **Repository name**: `jira-auto-reply-agent` (or your preferred name)
   - **Description**: "Automated Jira ticket reply agent with AI-powered responses"
   - **Visibility**: Choose **Private** (recommended for internal tools with credentials)
   - **Initialize**: Do NOT check "Add a README" (we already have one)
4. Click **"Create repository"**

## Step 2: Initialize Git Repository (Local)

Run these commands in PowerShell from the project directory:

```powershell
# Navigate to project directory
cd C:\Users\anura\Downloads\Devlpoment\ai_agent

# Initialize git repository
git init

# Add all files (respecting .gitignore)
git add .

# Create initial commit
git commit -m "Initial commit: Jira Auto Reply Agent"
```

## Step 3: Connect to GitHub and Push

After creating the repository on GitHub, you'll see setup instructions. Use these commands:

```powershell
# Add remote repository (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/jira-auto-reply-agent.git

# Rename default branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**If you're using SSH instead of HTTPS:**

```powershell
git remote add origin git@github.com:YOUR_USERNAME/jira-auto-reply-agent.git
git push -u origin main
```

## Step 4: Verify Upload

1. Go to your GitHub repository page
2. Verify all files are present:
   - ✅ `jira_auto_reply.py`
   - ✅ `jira_auto_reply.ipynb`
   - ✅ `requirements.txt`
   - ✅ `README.md`
   - ✅ `IMPLEMENTATION_PATH.md`
   - ✅ `tests/` directory
   - ✅ `.gitignore`
3. Verify sensitive files are NOT present:
   - ❌ `.env` (should be ignored)
   - ❌ `last_run.json` (should be ignored)
   - ❌ `.venv/` (should be ignored)
   - ❌ `__pycache__/` (should be ignored)

## Step 5: Add Environment Variables Template

Since `.env` files are ignored, create a template file for others:

**Create `env.example` file** (manually or via GitHub web interface):

```env
# Copy this file to .env and fill in your actual values
# DO NOT commit .env file with real credentials!

JIRA_BASE_URL=https://certifyos.atlassian.net
JIRA_EMAIL=your_email@certifyos.com
JIRA_API_TOKEN=your_jira_api_token_here
JIRA_ASSIGNEE_ACCOUNT_ID=your_account_id_here
PROJECT_KEY=TS
STATUS_TRANSITION_TODO_TO_IN_PROGRESS=To-Do
STATUS_TRANSITION_IN_PROGRESS_TO_WAITING=Iprogress
STATUS_TRANSITION_WAITING_TO_IN_PROGRESS=Wating for clinet
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
TIMEZONE=Asia/Kolkata
WINDOW_START=05:30
WINDOW_END=17:30
```

## Security Checklist

Before pushing, verify:

- [x] `.gitignore` includes `.env`
- [x] `.gitignore` includes `last_run.json`
- [x] `.gitignore` includes `.venv/`
- [x] No API keys or tokens in code files
- [x] No hardcoded credentials
- [x] README mentions environment variables
- [ ] Repository is set to **Private** (if contains internal tools)

## Future Updates

To push future changes:

```powershell
# Check status
git status

# Add changed files
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push
```

## Troubleshooting

### Authentication Issues

If you get authentication errors:

**Option 1: Use Personal Access Token**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` scope
3. Use token as password when pushing

**Option 2: Use GitHub CLI**
```powershell
# Install GitHub CLI
winget install GitHub.cli

# Authenticate
gh auth login

# Then push normally
git push
```

### Large Files

If you get errors about large files:
- Ensure `.venv/` is in `.gitignore`
- Ensure `__pycache__/` is in `.gitignore`
- Remove cached files: `git rm -r --cached .venv` (if accidentally added)

## Repository Settings (Recommended)

After creating the repository:

1. **Settings → Secrets and variables → Actions** (if using GitHub Actions)
   - Add repository secrets for CI/CD (if needed)

2. **Settings → Collaborators**
   - Add team members who need access

3. **Settings → Branches**
   - Add branch protection rules for `main` branch (optional)

4. **Add Topics/Tags**
   - `jira`
   - `automation`
   - `python`
   - `openai`
   - `atlassian`

## Next Steps

After uploading:

1. ✅ Share repository link with team
2. ✅ Update README with any additional setup steps
3. ✅ Set up branch protection (if team project)
4. ✅ Configure GitHub Actions for CI/CD (optional)
5. ✅ Add license file (if open source)

---

**Need Help?** Contact: anurag.rai@certifyos.com
