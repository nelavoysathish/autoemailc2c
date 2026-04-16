#!/usr/bin/env python3
"""
C2C DevOps/SRE Job Scraper
Daily job: Fetch C2C jobs → Save to jobs.json → Update README.md dashboard
"""

import requests
from datetime import datetime
import json
import sys
import time

# Job search keywords
TARGET_ROLES = ['devops', 'sre', 'site reliability', 'release engineer', 'platform engineer']
C2C_KEYWORDS = ['c2c', 'contract', '1099', 'independent', 'contract-to-hire', 'contractor']

def is_c2c_job(text):
    """Check if job is C2C contract"""
    text_lower = text.lower()
    return any(kw in text_lower for kw in C2C_KEYWORDS)

def get_role_type(title):
    """Categorize job role"""
    title_lower = title.lower()
    if 'devops' in title_lower:
        return 'DevOps'
    elif 'sre' in title_lower or 'site reliability' in title_lower:
        return 'SRE'
    elif 'release' in title_lower:
        return 'Release Engineer'
    elif 'platform' in title_lower:
        return 'Platform'
    return 'Engineering'

def scrape_remoteok():
    """Fetch from RemoteOK API"""
    print("   🔍 RemoteOK...", end=" ")
    jobs = []
    try:
        url = "https://remoteok.io/api"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        for item in list(data.values())[:100]:
            if not isinstance(item, dict) or 'job_title' not in item:
                continue
            
            title = item.get('job_title', '')
            desc = item.get('description', '')
            full_text = f"{title} {desc}".lower()
            
            # Check if C2C job
            if is_c2c_job(full_text) and any(role in full_text for role in TARGET_ROLES):
                jobs.append({
                    'title': title,
                    'company': item.get('company_name', 'N/A'),
                    'location': item.get('location', 'Remote'),
                    'salary': item.get('salary', 'Negotiable'),
                    'type': get_role_type(title),
                    'source': 'RemoteOK',
                    'url': item.get('url', '#'),
                    'posted': item.get('date_posted', 'Recently'),
                })
        
        print(f"✓ {len(jobs)} jobs")
        return jobs
    except Exception as e:
        print(f"✗ Error: {e}")
        return []

def scrape_jooble():
    """Fetch from Jooble API"""
    print("   🔍 Jooble...", end=" ")
    jobs = []
    try:
        url = "https://us.jooble.org/api/companies_positions"
        payload = {
            "keywords": "c2c devops sre site reliability engineer",
            "location": "United States"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        for item in data.get('positions', [])[:100]:
            title = item.get('title', '')
            snippet = item.get('snippet', '')
            full_text = f"{title} {snippet}".lower()
            
            if is_c2c_job(full_text) and any(role in full_text for role in TARGET_ROLES):
                jobs.append({
                    'title': title,
                    'company': item.get('company', 'N/A'),
                    'location': item.get('location', 'USA'),
                    'salary': 'Market Rate',
                    'type': get_role_type(title),
                    'source': 'Jooble',
                    'url': item.get('link', '#'),
                    'posted': item.get('date', 'Recently'),
                })
        
        print(f"✓ {len(jobs)} jobs")
        return jobs
    except Exception as e:
        print(f"✗ Error: {e}")
        return []

def scrape_weworkremotely():
    """Fetch from We Work Remotely"""
    print("   🔍 We Work Remotely...", end=" ")
    jobs = []
    try:
        url = "https://weworkremotely.com/api/v2/remote_jobs"
        params = {'category': 'DevOps,SRE'}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        for item in data.get('remote_jobs', [])[:50]:
            title = item.get('title', '')
            desc = item.get('description', '')
            full_text = f"{title} {desc}".lower()
            
            if is_c2c_job(full_text):
                jobs.append({
                    'title': title,
                    'company': item.get('company_name', 'N/A'),
                    'location': 'Remote',
                    'salary': item.get('salary', 'Negotiable'),
                    'type': get_role_type(title),
                    'source': 'We Work Remotely',
                    'url': item.get('url', '#'),
                    'posted': item.get('published_at', 'Recently'),
                })
        
        print(f"✓ {len(jobs)} jobs")
        return jobs
    except Exception as e:
        print(f"✗ Error: {e}")
        return []

def deduplicate(jobs):
    """Remove duplicate jobs"""
    seen = set()
    unique = []
    for job in jobs:
        key = (job['title'].lower(), job['company'].lower())
        if key not in seen:
            seen.add(key)
            unique.append(job)
    return unique

def save_json(jobs):
    """Save jobs to jobs.json"""
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
    print(f"✓ Saved jobs.json ({len(jobs)} jobs)")

def save_readme(jobs):
    """Update README.md dashboard"""
    
    # Organize by role
    devops = [j for j in jobs if j['type'] == 'DevOps']
    sre = [j for j in jobs if j['type'] == 'SRE']
    release = [j for j in jobs if j['type'] == 'Release Engineer']
    platform = [j for j in jobs if j['type'] == 'Platform']
    
    # Start building markdown
    md = f"""# 🔍 C2C DevOps/SRE Job Dashboard

**Auto-updated daily** | Last: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

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
        md += "| Company | Job Title | Location | Source | Link |\n"
        md += "|---------|-----------|----------|--------|------|\n"
        for job in devops[:20]:
            title = job['title'][:50] + "..." if len(job['title']) > 50 else job['title']
            md += f"| {job['company'][:20]} | {title} | {job['location'][:15]} | {job['source']} | [Apply]({job['url']}) |\n"
    else:
        md += "*No jobs found today*\n"
    
    md += f"""

---

## 🚀 SRE / Site Reliability Engineer ({len(sre)})

"""
    
    if sre:
        md += "| Company | Job Title | Location | Source | Link |\n"
        md += "|---------|-----------|----------|--------|------|\n"
        for job in sre[:20]:
            title = job['title'][:50] + "..." if len(job['title']) > 50 else job['title']
            md += f"| {job['company'][:20]} | {title} | {job['location'][:15]} | {job['source']} | [Apply]({job['url']}) |\n"
    else:
        md += "*No jobs found today*\n"
    
    md += f"""

---

## 🔧 Release Engineer ({len(release)})

"""
    
    if release:
        md += "| Company | Job Title | Location | Source | Link |\n"
        md += "|---------|-----------|----------|--------|------|\n"
        for job in release[:20]:
            title = job['title'][:50] + "..." if len(job['title']) > 50 else job['title']
            md += f"| {job['company'][:20]} | {title} | {job['location'][:15]} | {job['source']} | [Apply]({job['url']}) |\n"
    else:
        md += "*No jobs found today*\n"
    
    md += f"""

---

## 🏗️ Platform Engineer ({len(platform)})

"""
    
    if platform:
        md += "| Company | Job Title | Location | Source | Link |\n"
        md += "|---------|-----------|----------|--------|------|\n"
        for job in platform[:20]:
            title = job['title'][:50] + "..." if len(job['title']) > 50 else job['title']
            md += f"| {job['company'][:20]} | {title} | {job['location'][:15]} | {job['source']} | [Apply]({job['url']}) |\n"
    else:
        md += "*No jobs found today*\n"
    
    md += f"""

---

## 📁 Data Files

- `jobs.json` - Raw job data (API friendly)
- `README.md` - This dashboard

**Scraper:** Runs daily at 8 AM UTC  
**Sources:** RemoteOK, Jooble, We Work Remotely  
**Filter:** C2C contracts only  

Last update: {datetime.now().isoformat()}
"""
    
    with open('README.md', 'w') as f:
        f.write(md)
    print(f"✓ Updated README.md")

def main():
    print("\n" + "="*70)
    print("🔍 C2C JOB SCRAPER - Fetching Daily Contract Jobs")
    print("="*70 + "\n")
    
    all_jobs = []
    
    print("Scraping job sources:\n")
    all_jobs.extend(scrape_remoteok())
    time.sleep(1)
    all_jobs.extend(scrape_jooble())
    time.sleep(1)
    all_jobs.extend(scrape_weworkremotely())
    
    print()
    
    # Deduplicate
    unique = deduplicate(all_jobs)
    
    print(f"\n📊 Results:")
    print(f"   Found: {len(all_jobs)} total")
    print(f"   Unique: {len(unique)} after dedup")
    print(f"   - DevOps: {len([j for j in unique if j['type'] == 'DevOps'])}")
    print(f"   - SRE: {len([j for j in unique if j['type'] == 'SRE'])}")
    print(f"   - Release: {len([j for j in unique if j['type'] == 'Release Engineer'])}")
    print(f"   - Platform: {len([j for j in unique if j['type'] == 'Platform'])}")
    print()
    
    # Save
    save_json(unique)
    save_readme(unique)
    
    print("\n✅ SUCCESS! Dashboard updated.\n")
    print(f"📍 View on GitHub: https://github.com/YOUR_USERNAME/YOUR_REPO")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
