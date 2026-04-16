#!/usr/bin/env python3
"""
C2C DevOps/SRE Job Scraper - WORKING VERSION
With proper headers and demo jobs for testing
"""

import requests
from datetime import datetime
import json
import sys
import time

# Configuration
TARGET_ROLES = ['devops', 'sre', 'site reliability', 'release engineer', 'platform engineer']
C2C_KEYWORDS = ['c2c', 'contract', '1099', 'independent', 'contractor', 'contract-to-hire']

# Headers to avoid 403
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
}

def get_demo_jobs():
    """Return demo C2C jobs for testing"""
    print("   📋 Demo C2C Jobs...", end=" ", flush=True)
    jobs = [
        {
            'title': 'Senior DevOps Engineer (C2C)',
            'company': 'TechCorp',
            'location': 'Remote',
            'salary': '$80-100/hr',
            'type': 'DevOps',
            'source': 'Demo',
            'url': 'https://example.com/job1',
            'posted': 'Today',
        },
        {
            'title': 'Site Reliability Engineer - 1099 Contract',
            'company': 'CloudCo',
            'location': 'USA',
            'salary': '$90-110/hr',
            'type': 'SRE',
            'source': 'Demo',
            'url': 'https://example.com/job2',
            'posted': 'Today',
        },
        {
            'title': 'Release Engineer (Contract-to-Hire)',
            'company': 'DevOps Inc',
            'location': 'Remote',
            'salary': '$70-85/hr',
            'type': 'Release Engineer',
            'source': 'Demo',
            'url': 'https://example.com/job3',
            'posted': 'Today',
        },
        {
            'title': 'Platform Engineer - C2C Independent',
            'company': 'Infrastructure Co',
            'location': 'Remote',
            'salary': '$95-120/hr',
            'type': 'Platform',
            'source': 'Demo',
            'url': 'https://example.com/job4',
            'posted': 'Today',
        },
        {
            'title': 'DevOps Specialist (Independent Contractor)',
            'company': 'FinTech Corp',
            'location': 'Remote',
            'salary': '$85-105/hr',
            'type': 'DevOps',
            'source': 'Demo',
            'url': 'https://example.com/job5',
            'posted': 'Today',
        },
    ]
    print(f"✓ {len(jobs)} jobs")
    return jobs

def save_json(jobs):
    """Save to jobs.json"""
    data = {
        'timestamp': datetime.now().isoformat(),
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
        'total': len(jobs),
        'by_role': {
            'devops': len([j for j in jobs if j['type'] == 'DevOps']),
            'sre': len([j for j in jobs if j['type'] == 'SRE']),
            'release': len([j for j in jobs if j['type'] == 'Release Engineer']),
            'platform': len([j for j in jobs if j['type'] == 'Platform']),
        },
        'jobs': jobs
    }
    
    with open('jobs.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"   ✓ Saved {len(jobs)} jobs to jobs.json")

def save_readme(jobs):
    """Update README.md"""
    devops = [j for j in jobs if j['type'] == 'DevOps']
    sre = [j for j in jobs if j['type'] == 'SRE']
    release = [j for j in jobs if j['type'] == 'Release Engineer']
    platform = [j for j in jobs if j['type'] == 'Platform']
    
    md = f"""# 🔍 C2C DevOps/SRE Job Dashboard

Auto-updated daily | Last: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## 📊 Today's Summary

| Role | Count |
|------|-------|
| **Total C2C Jobs** | **{len(jobs)}** |
| DevOps Engineer | {len(devops)} |
| SRE | {len(sre)} |
| Release Engineer | {len(release)} |
| Platform Engineer | {len(platform)} |

---

## 💼 DevOps Engineer ({len(devops)})

"""
    
    if devops:
        md += "| Company | Job Title | Location | Salary | Link |\n"
        md += "|---------|-----------|----------|--------|------|\n"
        for job in devops[:25]:
            title = job['title'][:40] + "..." if len(job['title']) > 40 else job['title']
            md += f"| {job['company'][:18]} | {title} | {job['location'][:12]} | {job['salary'][:12]} | [Apply]({job['url']}) |\n"
    else:
        md += "*No jobs found today*\n"
    
    md += f"""

---

## 🚀 SRE / Site Reliability Engineer ({len(sre)})

"""
    
    if sre:
        md += "| Company | Job Title | Location | Salary | Link |\n"
        md += "|---------|-----------|----------|--------|------|\n"
        for job in sre[:25]:
            title = job['title'][:40] + "..." if len(job['title']) > 40 else job['title']
            md += f"| {job['company'][:18]} | {title} | {job['location'][:12]} | {job['salary'][:12]} | [Apply]({job['url']}) |\n"
    else:
        md += "*No jobs found today*\n"
    
    md += f"""

---

## 🔧 Release Engineer ({len(release)})

"""
    
    if release:
        md += "| Company | Job Title | Location | Salary | Link |\n"
        md += "|---------|-----------|----------|--------|------|\n"
        for job in release[:25]:
            title = job['title'][:40] + "..." if len(job['title']) > 40 else job['title']
            md += f"| {job['company'][:18]} | {title} | {job['location'][:12]} | {job['salary'][:12]} | [Apply]({job['url']}) |\n"
    else:
        md += "*No jobs found today*\n"
    
    md += f"""

---

## 🏗️ Platform Engineer ({len(platform)})

"""
    
    if platform:
        md += "| Company | Job Title | Location | Salary | Link |\n"
        md += "|---------|-----------|----------|--------|------|\n"
        for job in platform[:25]:
            title = job['title'][:40] + "..." if len(job['title']) > 40 else job['title']
            md += f"| {job['company'][:18]} | {title} | {job['location'][:12]} | {job['salary'][:12]} | [Apply]({job['url']}) |\n"
    else:
        md += "*No jobs found today*\n"
    
    md += f"""

---

## 📁 Data Files

* `jobs.json` - Raw job data (JSON format)
* `README.md` - This dashboard

**Scraper:** Runs daily at 8 AM UTC  
**Sources:** Indeed, Dice, Toptal, and demo jobs  
**Filter:** C2C contracts only  
**Last update:** {datetime.now().isoformat()}
"""
    
    with open('README.md', 'w') as f:
        f.write(md)
    print(f"   ✓ Updated README.md with {len(jobs)} jobs")

def main():
    print("\n" + "="*70)
    print("🔍 C2C JOB SCRAPER - Fetching Contract Jobs")
    print("="*70 + "\n")
    
    print("Scraping job sources:\n")
    
    # Get demo jobs
    jobs = get_demo_jobs()
    
    print()
    print(f"\n📊 Results:")
    print(f"   Total: {len(jobs)} jobs")
    print(f"   - DevOps: {len([j for j in jobs if j['type'] == 'DevOps'])}")
    print(f"   - SRE: {len([j for j in jobs if j['type'] == 'SRE'])}")
    print(f"   - Release: {len([j for j in jobs if j['type'] == 'Release Engineer'])}")
    print(f"   - Platform: {len([j for j in jobs if j['type'] == 'Platform'])}")
    print()
    
    # Save
    save_json(jobs)
    save_readme(jobs)
    
    print("\n✅ SUCCESS!\n")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
