# GitHub Actions Schedule Configuration Guide

## Understanding the Schedule

GitHub Actions uses **UTC time** for cron schedules, but your script uses **IST (UTC+5:30)**.

### Time Conversion
- **IST = UTC + 5:30**
- 5:30 AM IST = 00:00 UTC
- 5:30 PM IST = 12:00 UTC

## Current Schedule

The workflow is configured to run **every hour at :30 minutes past the hour** from **00:30 UTC to 12:30 UTC**.

This translates to:
- **00:30 UTC** = 6:00 AM IST (first run)
- **01:30 UTC** = 7:00 AM IST
- **02:30 UTC** = 8:00 AM IST
- ...
- **11:30 UTC** = 5:00 PM IST
- **12:30 UTC** = 6:00 PM IST (last run)

**Total: 13 runs per day**

## Option 1: Current Setup (Recommended)

**Cron:** `'30 0-12 * * *'`

**Runs:** Every hour from 6:00 AM to 6:00 PM IST

**Why this works:** The script itself checks the time window (`WINDOW_START=05:30` and `WINDOW_END=17:30`), so even if GitHub Actions runs at 6:00 AM IST, the script will check if it's within 5:30 AM - 5:30 PM and exit if outside the window.

## Option 2: Exact Times (5:30 AM and 5:30 PM)

If you want the workflow to run at **exactly** 5:30 AM and 5:30 PM IST, use:

```yaml
schedule:
  - cron: '0 0 * * *'      # 5:30 AM IST (00:00 UTC)
  - cron: '30 0-11 * * *' # Every hour 6:00 AM - 4:30 PM IST (00:30-11:30 UTC)  
  - cron: '0 12 * * *'    # 5:30 PM IST (12:00 UTC)
```

This gives you:
- **00:00 UTC** = 5:30 AM IST ✅
- **00:30-11:30 UTC** = 6:00 AM - 5:00 PM IST (hourly)
- **12:00 UTC** = 5:30 PM IST ✅

## Option 3: More Frequent Checks (Every 30 Minutes)

If you want to check more frequently:

```yaml
schedule:
  - cron: '0,30 0-12 * * *'  # Every 30 minutes from 00:00-12:30 UTC
```

This runs:
- Every 30 minutes from 5:30 AM to 6:00 PM IST
- **Total: 25 runs per day**

## Option 4: Every 15 Minutes

For even more frequent checks:

```yaml
schedule:
  - cron: '0,15,30,45 0-12 * * *'  # Every 15 minutes
```

## Option 5: Weekdays Only

To run only on weekdays (Monday-Friday):

```yaml
schedule:
  - cron: '30 0-12 * * 1-5'  # Monday-Friday only
```

## Cron Syntax Reference

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
* * * * *
```

### Examples

| Cron | Description | IST Times |
|------|-------------|-----------|
| `'30 0-12 * * *'` | Every hour at :30, UTC 00:30-12:30 | 6:00 AM - 6:00 PM |
| `'0 0 * * *'` | Daily at 00:00 UTC | 5:30 AM |
| `'0 12 * * *'` | Daily at 12:00 UTC | 5:30 PM |
| `'*/30 0-12 * * *'` | Every 30 minutes, UTC 00:00-12:30 | 5:30 AM - 6:00 PM |
| `'30 0-12 * * 1-5'` | Weekdays only, hourly | Mon-Fri 6:00 AM - 6:00 PM |

## Important Notes

1. **GitHub Actions Limitations:**
   - Scheduled workflows may be delayed by up to 15 minutes
   - Free accounts: 2000 minutes/month for private repos
   - Cron runs in UTC timezone

2. **Script Time Window:**
   - The script checks `WINDOW_START` and `WINDOW_END` environment variables
   - Even if GitHub Actions runs outside your desired window, the script will exit gracefully
   - This provides a safety net

3. **Recommended Approach:**
   - Use Option 1 (current setup) - runs every hour
   - The script's internal time check ensures it only processes during 5:30 AM - 5:30 PM IST
   - More reliable than trying to match exact times in cron

## Testing Your Schedule

1. Go to your repository → **Actions** tab
2. Click **"Run workflow"** → **"Run workflow"**
3. This manually triggers the workflow (useful for testing)
4. Check the logs to verify the time window check works

## Verifying Schedule

After updating the schedule:

1. Commit and push the workflow file
2. Wait for the next scheduled run
3. Check the Actions tab to see when it actually ran
4. Verify the script's time window check in the logs

---

**Current Configuration:** Option 1 (hourly runs with script-level time window check)
