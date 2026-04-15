# C2C SRE/DevOps Job Scraper - Implementation Summary

## ✅ What You're Getting

A **fully automated GitHub Actions workflow** that:

- **Scrapes** ZipRecruiter and Indeed daily for C2C SRE/DevOps contract roles
- **Filters** for relevant keywords (SRE, DevOps, Site Reliability Engineer, contract roles)
- **Emails** you a beautifully formatted HTML report each morning
- **Runs free** on GitHub's free tier (uses ~1 minute per day of your 2000 min/month allowance)
- **Requires zero maintenance** after initial 15-minute setup

### Files Included

| File | Purpose |
|------|---------|
| `scrape_jobs.py` | Python script that scrapes job boards, filters, and sends email |
| `.github/workflows/scraper.yml` | GitHub Actions workflow configuration (runs daily at 8 AM UTC) |
| `requirements.txt` | Python dependencies (requests, beautifulsoup4) |
| `README.md` | Comprehensive documentation and troubleshooting |
| `QUICK_SETUP.md` | Fast checklist for the impatient |
| `.gitignore` | Prevents committing sensitive data |

## 🚀 Quick Start (10 mins)

### 1. Create GitHub Repo
```bash
git clone https://github.com/YOUR-USERNAME/c2c-job-scraper.git
cd c2c-job-scraper
```

### 2. Copy Files
Place all provided files into the repo directory.

### 3. Gmail Setup
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Go to https://myaccount.google.com/apppasswords
4. Select "Mail" + "Windows Computer"
5. Copy the 16-character password

### 4. Add Secrets to GitHub
1. Go to repo → Settings → Secrets and variables → Actions
2. Create 3 secrets:
   - `SENDER_EMAIL` = your Gmail address
   - `SENDER_PASSWORD` = 16-char app password from step 3
   - `RECIPIENT_EMAIL` = your email (can be same as SENDER_EMAIL)

### 5. Push to GitHub
```bash
git add .
git commit -m "Initial C2C job scraper setup"
git push origin main
```

### 6. Test It
1. Go to repo → Actions tab
2. Click "C2C Job Scraper"
3. Click "Run workflow" → "Run workflow"
4. Wait 1-2 minutes
5. Check your email

**If you got an email with job listings, you're done! 🎉**

## 📅 What Happens Next

### Daily Automation
- ✅ Workflow runs automatically **every day at 8 AM UTC** (3 AM EST / 12 AM PST)
- ✅ You receive email with C2C job listings
- ✅ Click links to apply directly
- ✅ Respond to recruiters within 24 hours

### Change the Schedule (Optional)
Edit `.github/workflows/scraper.yml`:

```yaml
schedule:
  - cron: '0 8 * * *'  # Change the first 0 and 8
```

Examples:
- `0 9 * * *` = 9 AM UTC
- `0 15 * * *` = 3 PM UTC  
- `0 9 * * 1-5` = 9 AM UTC Monday-Friday only

## 🎯 Customization

### Filter for Different Keywords
Edit `scrape_jobs.py` in the `filter_jobs()` function:

```python
keywords = ['sre', 'devops', 'site reliability', 'platform engineer', 'kubernetes', 'terraform']
```

Add/remove keywords like `'aws'`, `'azure'`, `'gcp'`, `'golang'`, etc.

### Exclude Keywords
Add to `filter_jobs()`:

```python
exclude_keywords = ['junior', 'entry level', 'no sponsorship']
```

### Change Number of Results
In `scrape_jobs.py`, modify the slice:

```python
for listing in job_listings[:10]:  # Change 10 to 20, 50, etc.
```

### Add More Job Sources
Duplicate `scrape_ziprecruiter()` or `scrape_indeed()`, create new scrapers for Dice, LinkedIn, etc., and call them in `main()`.

## 🔧 Troubleshooting

### No email after running
1. Check spam folder
2. Verify secrets are set correctly
3. Check GitHub Actions logs: Actions tab → workflow run → Details

### "Authentication failed"
1. Regenerate App Password: https://myaccount.google.com/apppasswords
2. Update `SENDER_PASSWORD` secret with new 16-character password
3. Re-run workflow

### Workflow won't run on schedule
GitHub disables scheduled workflows after 60 days with no commits. Fix:
```bash
git commit --allow-empty -m "Reactivate workflow"
git push origin main
```

### Script runs but finds no jobs
1. Check job boards manually (ZipRecruiter, Indeed) to verify listings exist
2. Modify keywords in `filter_jobs()` to be broader
3. Check Gmail spam folder

## 📊 What the Email Looks Like

**Subject:** C2C SRE/DevOps Jobs - April 16, 2026

**Body:**
- Summary: "5 matching C2C position(s) found today"
- Job cards with:
  - Job title (clickable link)
  - Company name
  - Location badge
  - Salary range
  - Source and date
  - "View Full Listing" button

## 💡 Pro Tips

1. **Set email filter** to auto-label: Create filter in Gmail for emails from your sender address with subject containing "C2C SRE/DevOps" → auto-label "C2C Jobs"

2. **Quick apply system**: Have your rate range ready ($70-85/hr for Sr. SRE), your corporation EIN/LLC details saved, and a pitch template for quick recruiter responses

3. **Respond fast**: C2C roles fill within 24-48 hours. Check your email daily and reply immediately to good matches

4. **Track applications**: Maintain a spreadsheet (job, company, rate, applied date, recruiter, status) to manage the pipeline

5. **Refine filters**: After 1-2 weeks, adjust keywords based on what's actually useful vs. noise

## 🆓 Cost

- **GitHub Actions:** FREE (2000 minutes/month, your job uses ~1 min/day)
- **Gmail SMTP:** FREE (no additional cost for Python scripts)
- **Total:** $0/month ✓

## 📚 Files Reference

### Python Libraries Used
- `requests` - HTTP calls to job boards
- `beautifulsoup4` - HTML parsing
- `smtplib` (built-in) - Gmail SMTP
- `email` (built-in) - Email formatting

### GitHub Actions Runtime
- **OS:** Ubuntu 24
- **Python:** 3.11
- **Time per run:** ~1-2 minutes
- **Frequency:** Daily at 8 AM UTC (configurable)

## 🛡️ Security Notes

- **Secrets are encrypted** - Never visible in logs or workflow output
- **No PII storage** - Job data is not stored, only emailed
- **No third-party APIs** - Only uses public web scraping
- **No authentication required** - Scripts use simple HTTP requests

## 🚨 Important Limits

- ZipRecruiter/Indeed may rate-limit if you scrape too frequently - current setup (once daily) is safe
- Email deliverability depends on Gmail's SMTP service - rare but can happen if Gmail blocks unusual activity
- GitHub Actions are subject to GitHub's terms (free tier limits apply)

## 📞 Getting Help

1. **Check logs:** Actions → C2C Job Scraper → Click the failed/completed run → Details
2. **Review README.md** - Has detailed troubleshooting
3. **Run manually:** Actions → C2C Job Scraper → Run workflow to test
4. **Enable debug logging:** Add `print()` statements to `scrape_jobs.py`

## 🔄 Maintenance Checklist

### Weekly
- [ ] Check Actions tab for green checkmarks (workflow ran successfully)
- [ ] Verify emails arriving in inbox daily
- [ ] Apply to any relevant roles immediately

### Monthly
- [ ] Review and refine keyword filters if needed
- [ ] Update Python dependencies: `pip install --upgrade requests beautifulsoup4`
- [ ] Make a dummy commit to keep workflow active: `git commit --allow-empty -m "Monthly checkpoint"` → `git push`

### Quarterly
- [ ] Review job market trends in your keywords
- [ ] Add/remove job sources based on usefulness
- [ ] Optimize email report format if needed

---

## Next Steps

1. ✅ Download all files provided
2. ✅ Follow the Quick Start section above
3. ✅ Test the workflow manually
4. ✅ Verify first email arrives
5. ✅ Respond to good matches within 24 hours
6. ✅ Track your applications in a spreadsheet

**You now have a fully automated C2C job hunting system running 24/7 on GitHub's free tier. No servers, no maintenance, no cost.** 🚀

Good luck with your job search! C2C roles are hot right now — respond fast and you'll land something within 1-2 weeks. 📧
