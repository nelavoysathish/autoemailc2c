#!/usr/bin/env python3
"""
C2C SRE/DevOps Job Scraper
Scrapes ZipRecruiter and Indeed for C2C contract roles
Sends daily email digest
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys

# Environment variables (set in GitHub Actions secrets)
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

def scrape_ziprecruiter():
    """Scrape DevOps C2C jobs from ZipRecruiter"""
    jobs = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        # ZipRecruiter DevOps C2C search URL
        url = "https://www.ziprecruiter.com/Jobs/Devops-C2C?search=devops%20c2c"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Parse job listings
        job_listings = soup.find_all('div', class_='job-result')
        
        for listing in job_listings[:10]:  # Get top 10
            try:
                title_elem = listing.find('a', class_='job-title')
                company_elem = listing.find('a', class_='company')
                location_elem = listing.find('div', class_='job-location')
                salary_elem = listing.find('span', class_='salary')
                
                if title_elem and company_elem:
                    job = {
                        'source': 'ZipRecruiter',
                        'title': title_elem.get_text(strip=True),
                        'company': company_elem.get_text(strip=True),
                        'location': location_elem.get_text(strip=True) if location_elem else 'Remote',
                        'salary': salary_elem.get_text(strip=True) if salary_elem else 'Not listed',
                        'url': title_elem.get('href', '#'),
                        'posted': datetime.now().strftime('%Y-%m-%d')
                    }
                    jobs.append(job)
            except Exception as e:
                print(f"Error parsing job listing: {e}")
                continue
    
    except Exception as e:
        print(f"Error scraping ZipRecruiter: {e}")
    
    return jobs


def scrape_indeed():
    """Scrape SRE/DevOps C2C jobs from Indeed"""
    jobs = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        # Indeed C2C DevOps search
        url = "https://www.indeed.com/jobs?q=c2c+devops&limit=10"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Parse job cards
        job_cards = soup.find_all('div', class_='job_seen_beacon')
        
        for card in job_cards[:10]:
            try:
                title_elem = card.find('h2', class_='jobTitle')
                company_elem = card.find('span', class_='companyName')
                location_elem = card.find('div', class_='companyLocation')
                link_elem = card.find('a')
                
                if title_elem and company_elem:
                    job = {
                        'source': 'Indeed',
                        'title': title_elem.get_text(strip=True),
                        'company': company_elem.get_text(strip=True),
                        'location': location_elem.get_text(strip=True) if location_elem else 'Remote',
                        'salary': 'Check listing',
                        'url': f"https://www.indeed.com{link_elem.get('href', '')}" if link_elem else '#',
                        'posted': datetime.now().strftime('%Y-%m-%d')
                    }
                    jobs.append(job)
            except Exception as e:
                print(f"Error parsing Indeed job: {e}")
                continue
    
    except Exception as e:
        print(f"Error scraping Indeed: {e}")
    
    return jobs


def filter_jobs(jobs):
    """Filter for relevant C2C roles"""
    keywords = ['sre', 'devops', 'site reliability', 'platform engineer', 'kubernetes', 'terraform']
    c2c_keywords = ['c2c', 'contract', 'contract-to-hire']
    
    filtered = []
    for job in jobs:
        title_lower = job['title'].lower()
        
        # Must contain SRE/DevOps keywords
        has_relevant_skill = any(kw in title_lower for kw in keywords)
        
        # Should mention contract/C2C
        is_contract = any(kw in title_lower for kw in c2c_keywords)
        
        if has_relevant_skill and is_contract:
            filtered.append(job)
    
    return filtered


def generate_html_report(jobs):
    """Generate HTML email report"""
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            .header {{ background: #0066cc; color: white; padding: 20px; text-align: center; border-radius: 5px; }}
            .job-card {{ border: 1px solid #ddd; margin: 15px 0; padding: 15px; border-radius: 5px; background: #f9f9f9; }}
            .job-title {{ font-size: 16px; font-weight: bold; color: #0066cc; }}
            .job-meta {{ font-size: 13px; color: #666; margin-top: 5px; }}
            .job-location {{ display: inline-block; background: #e8f4f8; padding: 3px 8px; border-radius: 3px; margin-right: 8px; }}
            .job-salary {{ display: inline-block; background: #f0e8f4; padding: 3px 8px; border-radius: 3px; }}
            .job-link {{ margin-top: 10px; }}
            .job-link a {{ background: #0066cc; color: white; padding: 8px 15px; text-decoration: none; border-radius: 3px; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #999; }}
            .summary {{ background: #f0f0f0; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 C2C SRE/DevOps Job Report</h1>
            <p>{datetime.now().strftime('%B %d, %Y')}</p>
        </div>
        
        <div class="summary">
            <strong>{len(jobs)} matching C2C position(s) found today</strong>
            <p>This is your daily automated job scrape from ZipRecruiter and Indeed</p>
        </div>
    """
    
    if jobs:
        for job in jobs:
            html += f"""
            <div class="job-card">
                <div class="job-title">{job['title']}</div>
                <div class="job-meta">
                    <strong>{job['company']}</strong>
                </div>
                <div class="job-meta">
                    <span class="job-location">📍 {job['location']}</span>
                    <span class="job-salary">💰 {job['salary']}</span>
                </div>
                <div class="job-meta">
                    <small>Source: {job['source']} | Posted: {job['posted']}</small>
                </div>
                <div class="job-link">
                    <a href="{job['url']}" target="_blank">View Full Listing →</a>
                </div>
            </div>
            """
    else:
        html += "<p style='text-align: center; color: #999;'>No new C2C positions found today. Check back tomorrow!</p>"
    
    html += """
        <div class="footer">
            <p>This is an automated email. You're receiving this because you set up a GitHub Actions job scraper.</p>
            <p><a href="https://github.com" style="color: #0066cc; text-decoration: none;">Manage your scraper settings</a></p>
        </div>
    </body>
    </html>
    """
    
    return html


def send_email(subject, html_content):
    """Send email via Gmail SMTP"""
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = SENDER_EMAIL
        message["To"] = RECIPIENT_EMAIL
        
        # Attach HTML
        part = MIMEText(html_content, "html")
        message.attach(part)
        
        # Send via Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, message.as_string())
        
        print(f"✓ Email sent successfully to {RECIPIENT_EMAIL}")
        return True
    
    except Exception as e:
        print(f"✗ Error sending email: {e}")
        return False


def main():
    """Main execution"""
    print("🔍 Starting C2C Job Scraper...")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Scrape both sources
    print("\n📍 Scraping ZipRecruiter...")
    ziprecruiter_jobs = scrape_ziprecruiter()
    print(f"   Found {len(ziprecruiter_jobs)} listings")
    
    print("📍 Scraping Indeed...")
    indeed_jobs = scrape_indeed()
    print(f"   Found {len(indeed_jobs)} listings")
    
    # Combine and filter
    all_jobs = ziprecruiter_jobs + indeed_jobs
    print(f"\n📊 Total listings: {len(all_jobs)}")
    
    filtered_jobs = filter_jobs(all_jobs)
    print(f"✓ After filtering: {len(filtered_jobs)} C2C roles")
    
    # Generate and send report
    if SENDER_EMAIL and SENDER_PASSWORD and RECIPIENT_EMAIL:
        print("\n📧 Generating email report...")
        html_report = generate_html_report(filtered_jobs)
        
        subject = f"C2C SRE/DevOps Jobs - {datetime.now().strftime('%B %d, %Y')}"
        success = send_email(subject, html_report)
        
        if success:
            print("\n✓ Job scraper completed successfully!")
            sys.exit(0)
        else:
            print("\n✗ Failed to send email")
            sys.exit(1)
    else:
        print("\n⚠ Missing email credentials. Set SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL")
        print("\nJobs found (would be emailed):")
        for job in filtered_jobs[:5]:
            print(f"  - {job['title']} @ {job['company']} ({job['location']})")
        sys.exit(1)


if __name__ == "__main__":
    main()
