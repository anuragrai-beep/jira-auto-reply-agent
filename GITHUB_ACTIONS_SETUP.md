# GitHub Actions Setup Guide

This guide explains how to set up GitHub Actions to run the Jira Auto Reply Agent continuously.

## Overview

The GitHub Actions workflow will:
- Run automatically on a schedule (every hour from 5:30 AM to 5:30 PM IST)
- Execute the Jupyter notebook (`jira_auto_reply.ipynb`)
- Process Jira tickets automatically
- Allow manual triggering for testing

## Step 1: Add Required Secrets to GitHub

GitHub Actions uses **Secrets** to store sensitive information like API keys. You need to add these secrets to your repository.

### Access Repository Secrets

1. Go to your GitHub repository: `https://github.com/anuragrai-beep/jira-auto-reply-agent`
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

### Required Secrets

Add each of these secrets (click "New repository secret" for each):

#### Required Secrets (Must Have)

| Secret Name | Value | Description |
|------------|-------|-------------|
| `JIRA_BASE_URL` | `https://certifyos.atlassian.net` | Your Jira instance URL |
| `JIRA_EMAIL` | `anurag.rai@certifyos.com` | Your Jira email |
| `JIRA_API_TOKEN` | `your_jira_api_token` | Your Jira API token |
| `JIRA_ASSIGNEE_ACCOUNT_ID` | `712020:c0bede50-504a-4050-9cfb-663b18068ef0` | Account ID for assignment |
| `PROJECT_KEY` | `TS` | Jira project key |

#### Optional Secrets (Have Defaults)

| Secret Name | Default Value | Description |
|------------|---------------|-------------|
| `OPENAI_API_KEY` | (empty) | OpenAI API key (optional) |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI model to use |
| `TIMEZONE` | `Asia/Kolkata` | Timezone for time window |
| `WINDOW_START` | `05:30` | Start time for processing |
| `WINDOW_END` | `17:30` | End time for processing |
| `STATUS_TRANSITION_TODO_TO_IN_PROGRESS` | `To-Do` | Transition name |
| `STATUS_TRANSITION_IN_PROGRESS_TO_WAITING` | `Iprogress` | Transition name |
| `STATUS_TRANSITION_WAITING_TO_IN_PROGRESS` | `Wating for clinet` | Transition name |

### Quick Setup Script

You can add secrets via GitHub CLI (if installed):

```powershell
# Install GitHub CLI if not installed
winget install GitHub.cli

# Authenticate
gh auth login

# Add secrets (replace values)
gh secret set JIRA_BASE_URL --body "https://certifyos.atlassian.net"
gh secret set JIRA_EMAIL --body "anurag.rai@certifyos.com"
gh secret set JIRA_API_TOKEN --body "your_token_here"
gh secret set JIRA_ASSIGNEE_ACCOUNT_ID --body "712020:c0bede50-504a-4050-9cfb-663b18068ef0"
gh secret set PROJECT_KEY --body "TS"
gh secret set OPENAI_API_KEY --body "your_openai_key_here"
```

## Step 2: Verify Workflow File

The workflow file is already created at `.github/workflows/jira-auto-reply.yml`. It's configured to:

- **Schedule**: Run every hour at :30 minutes past the hour, from UTC 00:00 to 11:30
  - This translates to IST: 5:30 AM to 5:00 PM (approximately)
- **Manual Trigger**: Can be triggered manually from GitHub Actions tab
- **Timeout**: 15 minutes per run

### Adjust Schedule (Optional)

To change the schedule, edit `.github/workflows/jira-auto-reply.yml`:

```yaml
schedule:
  # Cron format: minute hour day month day-of-week
  # Example: Run every 30 minutes during business hours
  - cron: '*/30 0-11 * * *'  # Every 30 minutes, UTC 00:00-11:59
```

**Cron Schedule Reference:**
- `*/30 0-11 * * *` = Every 30 minutes, UTC 00:00-11:59
- `30 0-11 * * *` = Every hour at :30, UTC 00:00-11:30
- `0 0-11 * * *` = Every hour at :00, UTC 00:00-11:00

**IST Time Conversion:**
- IST = UTC + 5:30
- UTC 00:00 = IST 5:30 AM
- UTC 11:30 = IST 5:00 PM

## Step 3: Commit and Push Workflow

```powershell
# Add workflow file
git add .github/workflows/jira-auto-reply.yml

# Commit
git commit -m "Add GitHub Actions workflow for automated Jira replies"

# Push
git push origin main
```

## Step 4: Test the Workflow

### Manual Trigger Test

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **Jira Auto Reply Agent** workflow
4. Click **Run workflow** → **Run workflow**
5. Watch it execute

### Check Workflow Status

1. Go to **Actions** tab
2. Click on a workflow run to see:
   - Execution logs
   - Success/failure status
   - Notebook output (if uploaded as artifact)

## Step 5: Monitor Execution

### View Logs

1. Go to **Actions** tab
2. Click on a workflow run
3. Click on **run-jira-agent** job
4. Expand steps to see detailed logs

### Check for Errors

Common issues:
- **Missing secrets**: Check that all required secrets are set
- **Authentication failures**: Verify API tokens are correct
- **Timeout**: Increase timeout in workflow file if needed
- **Notebook execution errors**: Check notebook output artifact

## Step 6: Update Requirements (if needed)

If you need additional Python packages, update `requirements.txt`:

```txt
requests>=2.31.0
pytest>=7.4.0
pytest-mock>=3.11.0
papermill>=2.5.0
jupyter>=1.0.0
```

Then commit and push:

```powershell
git add requirements.txt
git commit -m "Add papermill and jupyter for notebook execution"
git push origin main
```

## Workflow Features

### ✅ Automatic Scheduling
- Runs every hour during business hours
- Respects time window configuration
- Skips execution outside configured hours

### ✅ Manual Trigger
- Can be triggered manually for testing
- Useful for debugging and immediate runs

### ✅ Artifact Storage
- Notebook output saved for 7 days
- Can download and inspect execution results

### ✅ Error Handling
- Fails gracefully on errors
- Logs detailed error messages
- Timeout protection (15 minutes)

## Troubleshooting

### Workflow Not Running

**Check:**
1. Secrets are configured correctly
2. Workflow file is in `.github/workflows/` directory
3. Workflow syntax is valid (check Actions tab for errors)
4. Schedule is correct (GitHub Actions uses UTC)

### Authentication Errors

**Check:**
1. Jira API token is valid and not expired
2. Account has necessary permissions
3. Email matches the token owner

### Notebook Execution Fails

**Check:**
1. All environment variables are set
2. Dependencies are installed correctly
3. Notebook code is valid
4. Check notebook output artifact for details

### Time Window Issues

**Check:**
1. TIMEZONE secret is set correctly
2. WINDOW_START and WINDOW_END are in correct format (HH:MM)
3. GitHub Actions runs in UTC, but script converts to configured timezone

## Advanced Configuration

### Run More Frequently

Edit `.github/workflows/jira-auto-reply.yml`:

```yaml
schedule:
  - cron: '*/15 0-11 * * *'  # Every 15 minutes
```

### Run Only on Weekdays

```yaml
schedule:
  - cron: '30 0-11 * * 1-5'  # Monday-Friday only
```

### Multiple Time Windows

```yaml
schedule:
  - cron: '30 0-5 * * *'   # Early morning
  - cron: '30 6-11 * * *'  # Business hours
```

### Use Self-Hosted Runner (Optional)

If you want to use your own server instead of GitHub's runners:

```yaml
jobs:
  run-jira-agent:
    runs-on: self-hosted  # Instead of ubuntu-latest
```

## Cost Considerations

- **GitHub Actions**: Free for public repos, 2000 minutes/month for private repos
- **OpenAI API**: Pay per use (if using OpenAI)
- **Jira API**: No additional cost (uses existing Jira license)

## Security Best Practices

1. ✅ **Never commit secrets** - Use GitHub Secrets
2. ✅ **Use private repository** - For internal tools
3. ✅ **Rotate tokens regularly** - Update secrets periodically
4. ✅ **Limit permissions** - Use least privilege for API tokens
5. ✅ **Monitor usage** - Check Actions tab regularly

## Next Steps

1. ✅ Add all required secrets
2. ✅ Push workflow file to repository
3. ✅ Test manual trigger
4. ✅ Monitor first scheduled run
5. ✅ Adjust schedule if needed
6. ✅ Set up notifications (optional)

## Notification Setup (Optional)

To get notified of workflow runs:

1. Go to repository **Settings** → **Notifications**
2. Enable notifications for:
   - Workflow runs
   - Workflow failures
   - Workflow successes (optional)

---

**Need Help?** Check the workflow logs in the Actions tab or contact: anurag.rai@certifyos.com
