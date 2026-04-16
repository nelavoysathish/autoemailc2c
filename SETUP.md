# 📊 C2C Jobs GitHub Dashboard - Setup Guide

Your requirement: **Fetch C2C jobs every day → Update GitHub README dashboard**

This setup does exactly that. ✅

---

## ⚡ Quick Setup (5 minutes)

### Step 1: Create GitHub Repo

```bash
cd ~
git clone https://github.com/YOUR-USERNAME/c2c-jobs.git
cd c2c-jobs
```

### Step 2: Copy Files

```bash
# Copy the scraper script
cp c2c_job_scraper.py .

# Create the workflows directory
mkdir -p .github/workflows

# Copy the workflow file
cp c2c-jobs.yml .github/workflows/
```

### Step 3: Create Initial Files

```bash
# Create empty jobs.json
echo '{}' > jobs.json

# Create empty README.md
touch README.md
```

### Step 4: Push to GitHub

```bash
git add .
git commit -m "Initial C2C job scraper setup"
git push origin main
```

### Step 5: Test It

```bash
# Go to GitHub → Actions tab
# Click "📊 C2C Jobs Dashboard"
# Click "Run workflow" → "Run workflow"
# Wait 30 seconds
# Check your repo - README.md should now have a job dashboard!
```

**Done!** 🎉 Your scraper now runs automatically every day at 8 AM UTC.

---

## 📋 What Happens Daily

1. **8 AM UTC** — Workflow automatically triggers
2. **Scraper runs** — Fetches C2C jobs from:
   - RemoteOK
   - Jooble  
   - We Work Remotely
3. **Deduplicates** — Removes duplicates
4. **Creates dashboard** — Generates README.md with job tables
5. **Saves data** — Stores jobs.json (raw data)
6. **Auto-commits** — Pushes changes back to GitHub
7. **You get notified** — Check your repo homepage for the latest jobs!

---

## 📊 Dashboard Preview

Your README.md will look like:

```
# 🔍 C2C DevOps/SRE Job Dashboard

**Auto-updated daily** | Last: 2024-04-17 08:15:32 UTC

## 📊 Today's Summary

| Role | Count |
|------|-------|
| Total C2C Jobs | 42 |
| DevOps Engineer | 18 |
| SRE | 16 |
| Release Engineer | 5 |
| Platform Engineer | 3 |

---

## 💼 DevOps Engineer (18)

| Company | Job Title | Location | Source | Link |
|---------|-----------|----------|--------|------|
| TechCorp | Senior DevOps... | Remote | RemoteOK | [Apply](...) |
| CloudCo | DevOps Engineer | USA | Jooble | [Apply](...) |
...
```

---

## 🔧 Customization

### Change Scheduled Time

Edit `.github/workflows/c2c-jobs.yml`:

```yaml
schedule:
  - cron: '0 8 * * *'  # Change 8 to your preferred hour (UTC)
```

Examples:
- `0 9 * * *` = 9 AM UTC
- `0 14 * * *` = 2 PM UTC
- `0 6 * * 1-5` = 6 AM UTC weekdays only

### Add More Job Sources

Edit `c2c_job_scraper.py` and add a new scraping function:

```python
def scrape_mynewsource():
    print("   🔍 MyNewSource...", end=" ")
    jobs = []
    try:
        # Your scraping code here
        return jobs
    except Exception as e:
        print(f"✗ Error: {e}")
        return []
```

Then call it in `main()`:

```python
all_jobs.extend(scrape_mynewsource())
```

### Filter by Location

In `c2c_job_scraper.py`, modify the scraping functions to add location check:

```python
if 'remote' in full_text or 'texas' in full_text or 'dallas' in full_text:
    # Add this job
```

---

## 📁 File Structure

```
your-repo/
├── .github/
│   └── workflows/
│       └── c2c-jobs.yml          ← Daily trigger
├── c2c_job_scraper.py             ← Main script
├── README.md                       ← Dashboard (auto-updated)
├── jobs.json                       ← Raw data (auto-updated)
└── .gitignore
```

---

## ✅ Verification Checklist

- [ ] Files pushed to GitHub
- [ ] Workflow file at `.github/workflows/c2c-jobs.yml`
- [ ] Scraper script at `c2c_job_scraper.py`
- [ ] Manual test: Run workflow → Dashboard appears ✓
- [ ] Check tomorrow at 8 AM UTC for automatic run

---

## 🚀 Monitor Your Dashboard

### View Latest Run
```bash
gh run list --workflow=c2c-jobs.yml
```

### View Run Details
```bash
gh run view <RUN_ID>
```

### View Logs
```bash
gh run view <RUN_ID> --log
```

---

## 💡 Pro Tips

1. **Star your repo** — Easy to find your C2C jobs dashboard
2. **Share the link** — Show recruiters your active job search
3. **Apply fast** — C2C roles fill quickly, respond within 24 hours
4. **Track results** — Keep a spreadsheet of jobs you applied to
5. **Monthly review** — Check if filters need adjustment

---

## 🆓 Cost

- **GitHub Actions:** FREE (2000 min/month, uses ~1 min/day)
- **APIs:** FREE (public job boards)
- **Hosting:** FREE (GitHub)

**Total: $0/month** ✓

---

## 🐛 Troubleshooting

### No dashboard showing up?

1. Check Actions tab for errors
2. Run manually: Actions → "Run workflow"
3. Check if `c2c_job_scraper.py` exists
4. Verify `git push` succeeded

### Jobs not fetching?

1. APIs might be rate-limited (uncommon)
2. Try manual run to test
3. Check scraper logs in Actions

### Need to update manually?

```bash
# Run locally
python c2c_job_scraper.py

# Commit changes
git add README.md jobs.json
git commit -m "Manual dashboard update"
git push origin main
```

---

## 📞 Need Help?

Check the Actions tab logs:
1. Go to GitHub repo
2. Click Actions
3. Click the latest run
4. See detailed logs with errors

---

## 🎯 You're Done!

You now have:
✅ Automated daily C2C job scraping  
✅ GitHub-hosted dashboard  
✅ Zero cost  
✅ No servers to manage  
✅ Public portfolio of your job search  

**Happy job hunting!** 🚀

Check back daily or set a reminder for 8:15 AM UTC to review new jobs!
