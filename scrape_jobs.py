#!/usr/bin/env python3
"""
C2C DevOps/SRE/Release Engineer Job Scraper
Saves jobs to JSON file for dashboard display
No email required
"""

import requests
from datetime import datetime
import json
import os
import sys

# Target roles
TARGET_ROLES = ['devops', 'sre', 'site reliability engineer', 'release engineer']
C2C_KEYWORDS = ['c2c', 'contract', '1099', 'independent', 'contract-to-hire']

def is_target_role(title, description=""):
    """Check if job matches target roles"""
    combined = (title + " " + description).lower()
    return any(role in combined for role in TARGET_ROLES)

def is_c2c_job(title, description):
    """Check if job is C2C contract"""
    combined = (title + " " + description).lower()
    return any(kw in combined for kw in C2C_KEYWORDS)

def get_role_type(title):
    """Determine role type"""
    title_lower = title.lower()
    if 'devops' in title_lower:
        return 'devops'
    elif 'sre' in title_lower or 'site reliability' in title_lower:
        return 'sre'
    elif 'release' in title_lower:
        return 'release'
    return 'other'

def scrape_github_jobs():
    """Scrape from GitHub Jobs API"""
    jobs = []
    
    try:
        print("   Searching GitHub Jobs...")
        
        base_url = "https://jobs.github.com/positions.json"
        
        params = {
            "description": "devops sre release engineer",
            "location": "United States",
            "full_time": False,
            "page": 1
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        for job in data[:20]:
            try:
                if is_target_role(job.get('title', ''), job.get('description', '')):
                    job_obj = {
                        'title': job.get('title', 'N/A'),
                        'company': job.get('company', 'N/A'),
                        'location': job.get('location', 'USA'),
                        'salary': 'N/A',
                        'type': get_role_type(job.get('title', '')),
                        'source': 'GitHub Jobs',
                        'posted': job.get('created_at', ''),
                        'url': job.get('url', '#'),
                        'is_c2c': is_c2c_job(job.get('title', ''), job.get('description', ''))
                    }
                    jobs.append(job_obj)
            except:
                continue
        
        return jobs
    except Exception as e:
        print(f"      Error: {e}")
        return []

def scrape_jooble():
    """Scrape from Jooble API"""
    jobs = []
    
    try:
        print("   Searching Jooble...")
        
        url = "https://us.jooble.org/api/companies_positions"
        
        payload = {
            "keywords": "devops engineer sre release engineer c2c",
            "location": "United States",
            "radius": 0
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'positions' in data:
            for job in data['positions'][:20]:
                try:
                    if is_target_role(job.get('title', ''), job.get('snippet', '')):
                        job_obj = {
                            'title': job.get('title', 'N/A'),
                            'company': job.get('company', 'N/A'),
                            'location': job.get('location', 'USA'),
                            'salary': 'N/A',
                            'type': get_role_type(job.get('title', '')),
                            'source': 'Jooble',
                            'posted': job.get('date', ''),
                            'url': job.get('link', '#'),
                            'is_c2c': is_c2c_job(job.get('title', ''), job.get('snippet', ''))
                        }
                        jobs.append(job_obj)
                except:
                    continue
        
        return jobs
    except Exception as e:
        print(f"      Error: {e}")
        return []

def scrape_adzuna():
    """Scrape from Adzuna API"""
    jobs = []
    
    try:
        print("   Searching Adzuna...")
        
        base_url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
        
        params = {
            "app_id": "demo",
            "app_key": "demo",
            "what": "devops engineer sre",
            "where": "United States",
            "days_ago": 1,
            "results_per_page": 20
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'results' in data:
            for job in data['results'][:20]:
                try:
                    if is_target_role(job.get('title', ''), job.get('description', '')):
                        job_obj = {
                            'title': job.get('title', 'N/A'),
                            'company': job.get('company', {}).get('display_name', 'N/A'),
                            'location': job.get('location', {}).get('area', ['USA'])[0] if job.get('location') else 'USA',
                            'salary': str(job.get('salary_max', 'N/A')),
                            'type': get_role_type(job.get('title', '')),
                            'source': 'Adzuna',
                            'posted': job.get('created', ''),
                            'url': job.get('redirect_url', '#'),
                            'is_c2c': is_c2c_job(job.get('title', ''), job.get('description', ''))
                        }
                        jobs.append(job_obj)
                except:
                    continue
        
        return jobs
    except Exception as e:
        print(f"      Error: {e}")
        return []

def save_to_json(jobs):
    """Save jobs to JSON file"""
    try:
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_jobs': len(jobs),
            'roles': {
                'devops': len([j for j in jobs if j['type'] == 'devops']),
                'sre': len([j for j in jobs if j['type'] == 'sre']),
                'release': len([j for j in jobs if j['type'] == 'release'])
            },
            'jobs': jobs
        }
        
        with open('jobs.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n✓ Saved {len(jobs)} jobs to jobs.json")
        return True
    except Exception as e:
        print(f"✗ Error saving jobs: {e}")
        return False

def main():
    print("🔍 C2C Job Scraper (Saving to JSON)")
    print("=" * 60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("🎯 Roles: DevOps, SRE, Release Engineer")
    print("📍 Location: United States")
    print("=" * 60)
    print()
    
    all_jobs = []
    
    # Scrape from multiple sources
    print("📍 Scraping job boards...")
    print()
    
    try:
        gh_jobs = scrape_github_jobs()
        all_jobs.extend(gh_jobs)
        print(f"   ✓ GitHub Jobs: {len(gh_jobs)} jobs")
    except:
        print(f"   ⚠️  GitHub Jobs: Failed")
    
    try:
        jooble_jobs = scrape_jooble()
        all_jobs.extend(jooble_jobs)
        print(f"   ✓ Jooble: {len(jooble_jobs)} jobs")
    except:
        print(f"   ⚠️  Jooble: Failed")
    
    try:
        adzuna_jobs = scrape_adzuna()
        all_jobs.extend(adzuna_jobs)
        print(f"   ✓ Adzuna: {len(adzuna_jobs)} jobs")
    except:
        print(f"   ⚠️  Adzuna: Failed")
    
    print()
    
    # Deduplicate
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        key = (job['title'].lower(), job['company'].lower())
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)
    
    print(f"📊 Summary:")
    print(f"   Total jobs found: {len(all_jobs)}")
    print(f"   Unique jobs: {len(unique_jobs)}")
    
    devops_count = len([j for j in unique_jobs if j['type'] == 'devops'])
    sre_count = len([j for j in unique_jobs if j['type'] == 'sre'])
    release_count = len([j for j in unique_jobs if j['type'] == 'release'])
    
    print(f"   - DevOps: {devops_count}")
    print(f"   - SRE: {sre_count}")
    print(f"   - Release Engineer: {release_count}")
    print()
    
    # Save to JSON
    if save_to_json(unique_jobs):
        print("✓ Success!")
        sys.exit(0)
    else:
        print("✗ Failed to save jobs")
        sys.exit(1)

if __name__ == "__main__":
    main()
