# C2C SRE/DevOps Job Scraper

Automated GitHub Actions workflow that scrapes C2C SRE/DevOps job listings from ZipRecruiter and Indeed, then emails you a daily report.

## Features

✅ **Automated daily scraping** - Runs on schedule (8 AM UTC by default)  
✅ **Multi-source** - Scrapes ZipRecruiter and Indeed  
✅ **Smart filtering** - Only shows C2C contract roles matching your skills  
✅ **Email delivery** - Beautiful HTML email with direct job links  
✅ **Free tier** - Uses GitHub Actions free tier (2000 minutes/month)  
✅ **Manual trigger** - Run anytime from GitHub Actions UI  

## Setup Instructions

### Step 1: Create GitHub Repository

```bash
# Create a new repo (or use existing one)
git clone https://github.com/YOUR-USERNAME/c2c-job-scraper.git
cd c2c-job-scraper

# Copy the files from this project into your repo
```

Or simply fork this repository.

### Step 2: Set Up Email Credentials

The script sends emails via Gmail SMTP. You have two options:

#### Option A: Use Gmail App Password (Recommended)

1. **Enable 2-Step Verification** on your Gmail account:
   - Go to https://myaccount.google.com/security
   - Click "2-Step Verification" and follow prompts

2. **Generate App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Google will generate a 16-character password
   - Copy this password (you'll use it as SENDER_PASSWORD)

#### Option B: Use Regular Gmail Password (Less Secure)

1. Enable "Less secure app access":
   - Go to https://myaccount.google.com/security
   - Scroll to "Less secure app access"
   - Toggle "Allow less secure apps" ON

2. Use your Gmail password directly

### Step 3: Add GitHub Secrets

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Create three secrets:

| Secret Name | Value | Example |
|-----------|-------|---------|
| `SENDER_EMAIL` | Your Gmail address | `your-email@gmail.com` |
| `SENDER_PASSWORD` | App password (16 chars) OR Gmail password | `abcd efgh ijkl mnop` |
| `RECIPIENT_EMAIL` | Email to receive reports | `your-email@gmail.com` (can be same or different) |

**Screenshot example:**
```
Settings > Secrets and variables > Actions > New repository secret

Name: SENDER_EMAIL
Value: your-email@gmail.com
[Add secret]

Name: SENDER_PASSWORD  
Value: xxxx xxxx xxxx xxxx
[Add secret]

Name: RECIPIENT_EMAIL
Value: your-email@gmail.com
[Add secret]
```

### Step 4: File Structure

Ensure your repository has this structure:

```
c2c-job-scraper/
├── .github/
│   └── workflows/
│       └── scraper.yml          # GitHub Actions workflow
├── scrape_jobs.py               # Main scraper script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

### Step 5: Test the Workflow

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Click **C2C Job Scraper** on the left
4. Click **Run workflow** → **Run workflow**
5. Wait 1-2 minutes, then check your email

You should receive an email with today's C2C job listings!

### Step 6: Verify Automatic Scheduling

The workflow is set to run automatically:
- **Daily at 8 AM UTC** (3 AM EST / 12 AM PST)

To change the schedule time, edit `.github/workflows/scraper.yml`:

```yaml
schedule:
  - cron: '0 8 * * *'  # Change this line
```

**Cron timing examples:**
- `0 8 * * *` = 8 AM UTC daily
- `0 9 * * *` = 9 AM UTC daily
- `0 15 * * *` = 3 PM UTC daily
- `0 9 * * 1-5` = 9 AM UTC Monday-Friday only

## Customization

### Change Job Search Keywords

Edit `scrape_jobs.py` and modify the `filter_jobs()` function:

```python
def filter_jobs(jobs):
    keywords = ['sre', 'devops', 'site reliability', 'platform engineer', 'kubernetes', 'terraform']
    c2c_keywords = ['c2c', 'contract', 'contract-to-hire']
    # ... rest of function
```

Add or remove keywords as needed.

### Change Number of Results

In `scrape_jobs.py`, modify these lines:

```python
job_listings = soup.find_all('div', class_='job-result')

for listing in job_listings[:10]:  # Change 10 to any number
```

### Add More Job Sources

Duplicate `scrape_ziprecruiter()` and `scrape_indeed()` functions, add new scraper for other sites (LinkedIn, Dice, etc.), then call it in `main()`.

### Exclude Certain Keywords

Add a blacklist to `filter_jobs()`:

```python
def filter_jobs(jobs):
    exclude_keywords = ['junior', 'entry level', 'no sponsorship']
    
    filtered = []
    for job in jobs:
        title_lower = job['title'].lower()
        
        if any(kw in title_lower for kw in exclude_keywords):
            continue  # Skip this job
        
        # ... rest of filtering logic
```

## Troubleshooting

### "Authentication failed" error

**Problem:** Workflow shows SMTP authentication error  
**Solution:**
- Verify `SENDER_PASSWORD` is correct (use App Password, not Gmail password)
- Make sure 2-Step Verification is enabled on Gmail
- Regenerate App Password at https://myaccount.google.com/apppasswords

### No email received

**Problem:** Workflow runs but no email arrives  
**Solution:**
- Check GitHub Actions logs (Actions tab → workflow run → logs)
- Verify secrets are set correctly
- Check spam/junk folder
- Try manual trigger to test: Actions → Run workflow

### Workflow not running on schedule

**Problem:** Daily scheduled run doesn't execute  
**Solution:**
- GitHub Actions disables scheduled workflows if no commits in 60 days
- Make a small commit to re-enable: `git commit --allow-empty -m "Keep workflow active"` then `git push`
- Alternatively, manually trigger weekly to keep it active

### HTML email looks broken

**Problem:** Email client doesn't display HTML correctly  
**Solution:**
- The script sends both HTML and plain text
- Try opening in different email client
- Edit `scrape_jobs.py` email generation if needed

## Cost

- **GitHub Actions free tier:** 2000 minutes/month
- **This job:** ~1 minute per run
- **Daily runs:** 30 runs/month = ~30 minutes/month
- **Cost:** FREE ✓

## Privacy & Security

- Secrets are encrypted and never exposed in logs
- Job data is not stored or shared
- Only you have access to results (your email)
- No third-party APIs required (pure web scraping)

## Maintenance

### Weekly check-in

Every week, verify the workflow is running:
1. Go to Actions tab
2. Check the last run status (should show ✓ green checkmark)
3. If showing ✗, read the logs to debug

### Keep dependencies updated

Every month, update Python packages:

```bash
pip install --upgrade requests beautifulsoup4 lxml
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

## Future Enhancements

- Add database to track new vs. seen jobs
- Filter by rate range (e.g., only $70+/hr)
- Add Slack notifications
- Track which recruiters are most active
- Export to CSV for analysis

## Support

If you run into issues:

1. Check GitHub Actions logs (Actions → workflow → Details)
2. Verify secrets are set
3. Test manually: Actions → Run workflow
4. Check spam folder for emails
5. Read the Troubleshooting section above

---

**Last updated:** April 2026  
**Status:** Working ✓

Happy job hunting! 🚀
