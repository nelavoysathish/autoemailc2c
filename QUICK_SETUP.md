# GitHub Actions C2C Job Scraper - Quick Setup Checklist

## ⏱️ Time Required: 10-15 minutes

## 📋 Step-by-Step Setup

### 1. Create/Prepare GitHub Repository (2 min)

- [ ] Create new GitHub repo named `c2c-job-scraper` (or similar)
- [ ] Clone to your computer: `git clone https://github.com/YOUR-USERNAME/c2c-job-scraper.git`
- [ ] Navigate to folder: `cd c2c-job-scraper`

### 2. Add Project Files (1 min)

Copy these files into your repo:
- [ ] `.github/workflows/scraper.yml` (GitHub Actions workflow)
- [ ] `scrape_jobs.py` (main scraper script)
- [ ] `requirements.txt` (Python dependencies)
- [ ] `README.md` (documentation)
- [ ] `.gitignore` (prevent committing secrets)

### 3. Set Up Gmail (5 min)

**Option A: Gmail App Password (Recommended)**

- [ ] Visit https://myaccount.google.com/security
- [ ] Enable "2-Step Verification" (if not already done)
- [ ] Go to https://myaccount.google.com/apppasswords
- [ ] Select Mail → Windows Computer
- [ ] Copy the 16-character app password

**Option B: Gmail Password (Less Secure)**

- [ ] Visit https://myaccount.google.com/security
- [ ] Enable "Less secure app access"
- [ ] Use your Gmail password directly

### 4. Add GitHub Secrets (3 min)

- [ ] Go to GitHub repo → Settings → Secrets and variables → Actions
- [ ] Click "New repository secret"

**Add 3 secrets:**

| # | Name | Value |
|---|------|-------|
| 1 | `SENDER_EMAIL` | your-email@gmail.com |
| 2 | `SENDER_PASSWORD` | 16-char app password (or Gmail password) |
| 3 | `RECIPIENT_EMAIL` | your-email@gmail.com (or another email) |

- [ ] Verify all 3 secrets are created

### 5. Commit and Push (2 min)

```bash
git add .
git commit -m "Initial setup: C2C job scraper with GitHub Actions"
git push origin main
```

- [ ] Verify files appear on GitHub.com

### 6. Test the Workflow (2 min)

- [ ] Go to GitHub repo → Actions tab
- [ ] Click "C2C Job Scraper" workflow
- [ ] Click "Run workflow" → "Run workflow" button
- [ ] Wait 1-2 minutes
- [ ] Check your email for the job report

**✓ If you got an email with job listings, you're done!**

### 7. (Optional) Adjust Schedule

Edit `.github/workflows/scraper.yml` to change run time:

```yaml
schedule:
  - cron: '0 8 * * *'  # Current: 8 AM UTC daily
```

Common schedules:
- `0 9 * * *` = 9 AM UTC
- `0 15 * * *` = 3 PM UTC
- `0 9 * * 1-5` = 9 AM UTC Mon-Fri only

---

## 🎯 What Happens Next

- ✅ Workflow runs automatically daily (8 AM UTC by default)
- ✅ You receive email with C2C job listings
- ✅ Click links to apply directly
- ✅ Respond to recruiters within 24 hours

## 🔧 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| No email after manual run | Check spam folder, verify secrets are correct |
| "Authentication failed" in logs | Regenerate Gmail App Password, use that instead |
| Workflow won't run on schedule | Make a commit to re-enable: `git commit --allow-empty -m "Reactivate workflow" && git push` |
| Want different job keywords | Edit `filter_jobs()` function in `scrape_jobs.py` |

## 📊 Monitor Workflow

Every week, check:
1. GitHub Actions tab
2. Verify last run has green ✓ checkmark
3. Check your email for that day's report

## 💡 Pro Tips

- Set email filter to auto-label: `from:(Gmail address) subject:("C2C SRE/DevOps")` → Create label "C2C Jobs"
- Reply to recruiters within 24 hours (C2C roles fill fast!)
- Have your rate range ready: $70-85/hr for Sr. SRE/DevOps
- Save your corporation info (EIN, LLC details) for quick client submissions

---

**You're all set!** 🚀 You now have a fully automated job scraper running on GitHub's free tier.
