#!/usr/bin/env python3
"""
C2C SRE/DevOps Job Scraper
Scrapes ZipRecruiter and Indeed for C2C contract roles:
- DevOps Engineer
- Site Reliability Engineer (SRE)
- Release Engineer
From all United States, posted in last 24 hours
Sends daily email digest
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys
import re

# Environment variables (set in GitHub Actions secrets)
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# Target roles
TARGET_ROLES = ['devops engineer', 'site reliability engineer', 'sre', 'release engineer']
C2C_KEYWORDS = ['c2c', 'contract', '1099', 'independent contractor', 'contract-to-hire']

def is_target_role(title):
    """Check if job title matches target roles"""
    title_lower = title.lower().strip()
    
    for role in TARGET_ROLES:
        if role in title_lower:
            return True
    return False

def is_c2c_role(title, company):
    """Check if job is C2C based"""
    title_lower = title.lower()
    company_lower = company.lower()
    
    for keyword in C2C_KEYWORDS:
        if keyword in title_lower or keyword in company_lower:
            return True
    return False

def parse_posting_time(time_str):
    """Parse posting time and check if within last 24 hours"""
    if not time_str:
        return True
    
    time_str = time_str.lower().strip()
    
    # Parse "X hours ago"
    if 'hour' in time_str:
        match = re.search(r'(\d+)\s*hour', time_str)
        if match:
            hours = int(match.group(1))
            if hours <= 24:
                return True
            else:
                return False
    
    # Parse "X days ago"
    if 'day' in time_str:
        match = re.search(r'(\d+)\s*day', time_str)
        if match:
            days = int(match.group(1))
            if days == 0:  # Posted today
                return True
            else:
                return False
    
    # "just now" or "recently"
    if 'just now' in time_str or 'recently' in time_str:
        return True
    
    # If no time info, include it
    return True

def scrape_ziprecruiter():
    """Scrape DevOps/SRE/Release Engineer C2C jobs from ZipRecruiter (USA, last 24 hours)"""
    jobs = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        # Search for each target role
        roles_to_search = [
            ("devops engineer", "devops%20engineer"),
            ("site reliability engineer", "site%20reliability%20engineer"),
            ("release engineer", "release%20engineer")
        ]
        
        for role_name, role_url in roles_to_search:
            print(f"   Searching for: {role_name}")
            
            # ZipRecruiter search: C2C + role + USA + last 24 hours
            url = f"https://www.ziprecruiter.com/Jobs/{role_url}-C2C?search=c2c%20{role_url}&days=1"
            
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                job_listings = soup.find_all('div', class_='job-result')
                
                print(f"      Found {len(job_listings)} listings")
                
                for listing in job_listings[:20]:
                    try:
                        title_elem = listing.find('a', class_='job-title')
                        company_elem = listing.find('a', class_='company')
                        location_elem = listing.find('div', class_='job-location')
                        salary_elem = listing.find('span', class_='salary')
                        time_elem = listing.find('span', class_='job-age')
                        
                        if title_elem and company_elem:
                            title = title_elem.text.strip()
                            company = company_elem.text.strip()
                            location = location_elem.text.strip() if location_elem else 'N/A'
                            
                            # Check if target role
                            if is_target_role(title):
                                # Check if USA location
                                if 'united states' in location.lower() or 'usa' in location.lower() or 'remote' in location.lower():
                                    # Check posting time
                                    time_str = time_elem.text if time_elem else ""
                                    if parse_posting_time(time_str):
                                        job = {
                                            'source': 'ZipRecruiter',
                                            'title': title,
                                            'company': company,
                                            'location': location,
                                            'salary': salary_elem.text.strip() if salary_elem else 'N/A',
                                            'posted': time_str,
                                            'url': title_elem.get('href', '#'),
                                            'is_c2c': is_c2c_role(title, company)
                                        }
                                        jobs.append(job)
                                        print(f"      ✓ {title[:45]}... | {location}")
                    except Exception as e:
                        continue
            except Exception as e:
                print(f"      Error: {e}")
                continue
        
        return jobs
    except Exception as e:
        print(f"Error scraping ZipRecruiter: {e}")
        return []

def scrape_indeed():
    """Scrape DevOps/SRE/Release Engineer C2C jobs from Indeed (USA, last 24 hours)"""
    jobs = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        # Search for each target role
        roles_to_search = [
            ("devops engineer", "devops%20engineer"),
            ("site reliability engineer", "site%20reliability%20engineer"),
            ("release engineer", "release%20engineer")
        ]
        
        for role_name, role_url in roles_to_search:
            print(f"   Searching for: {role_name}")
            
            # Indeed search: C2C + role + USA + last 24 hours
            url = f"https://www.indeed.com/jobs?q=c2c+{role_url}&l=United+States&date=1&limit=25"
            
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                job_listings = soup.find_all('div', class_='job_seen_beacon')
                
                print(f"      Found {len(job_listings)} listings")
                
                for listing in job_listings[:20]:
                    try:
                        title_elem = listing.find('h2', class_='jobTitle')
                        company_elem = listing.find('span', class_='companyName')
                        location_elem = listing.find('div', class_='companyLocation')
                        time_elem = listing.find('span', class_='date')
                        
                        if title_elem:
                            title = title_elem.text.strip()
                            company = company_elem.text.strip() if company_elem else 'N/A'
                            location = location_elem.text.strip() if location_elem else 'N/A'
                            
                            # Check if target role
                            if is_target_role(title):
                                # Check if USA location
                                if 'united states' in location.lower() or 'usa' in location.lower() or 'remote' in location.lower() or ',' in location:
                                    # Check posting time
                                    time_str = time_elem.text if time_elem else ""
                                    if parse_posting_time(time_str):
                                        job_url = '#'
                                        if title_elem.find('a'):
                                            job_url = title_elem.find('a').get('href', '#')
                                        
                                        job = {
                                            'source': 'Indeed',
                                            'title': title,
                                            'company': company,
                                            'location': location,
                                            'salary': 'N/A',
                                            'posted': time_str,
                                            'url': job_url,
                                            'is_c2c': is_c2c_role(title, company)
                                        }
                                        jobs.append(job)
                                        print(f"      ✓ {title[:45]}... | {location}")
                    except Exception as e:
                        continue
            except Exception as e:
                print(f"      Error: {e}")
                continue
        
        return jobs
    except Exception as e:
        print(f"Error scraping Indeed: {e}")
        return []

def send_email_gmail(jobs):
    """Send email using Gmail SMTP with app password"""
    try:
        if not SENDER_EMAIL or not SENDER_PASSWORD or not RECIPIENT_EMAIL:
            print("✗ Missing email credentials")
            return False
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"C2C DevOps/SRE/Release Engineer Jobs (Last 24h) - {datetime.now().strftime('%B %d, %Y')}"
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        
        # Create HTML content
        html = "<html><body style='font-family: Arial, sans-serif; color: #333;'>"
        html += f"<h2>🔍 C2C DevOps/SRE/Release Engineer Jobs</h2>"
        html += f"<p>📅 <strong>Report Date:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>"
        html += f"<p>🎯 <strong>Roles:</strong> DevOps Engineer | Site Reliability Engineer (SRE) | Release Engineer</p>"
        html += f"<p>📍 <strong>Location:</strong> United States (All)</p>"
        html += f"<p>⏰ <strong>Posted:</strong> Last 24 Hours</p>"
        html += f"<hr>"
        html += f"<p>Found <strong>{len(jobs)}</strong> matching positions:</p>"
        
        if jobs:
            html += "<hr>"
            for idx, job in enumerate(jobs, 1):
                html += f"<h3 style='color: #2c3e50;'>{idx}. {job['title']}</h3>"
                html += f"<p style='margin: 5px 0;'><strong>💼 Company:</strong> {job['company']}</p>"
                html += f"<p style='margin: 5px 0;'><strong>📍 Location:</strong> {job['location']}</p>"
                html += f"<p style='margin: 5px 0;'><strong>💰 Salary:</strong> {job['salary']}</p>"
                html += f"<p style='margin: 5px 0;'><strong>📅 Posted:</strong> {job['posted']}</p>"
                html += f"<p style='margin: 5px 0;'><strong>🔗 Source:</strong> {job['source']}"
                
                if job['is_c2c']:
                    html += " <span style='background-color: #27ae60; color: white; padding: 2px 8px; border-radius: 3px; font-size: 12px;'>✓ C2C</span>"
                html += "</p>"
                
                html += f"<p><a href='{job['url']}' style='display: inline-block; background-color: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;'>👉 Apply Now</a></p>"
                html += "<hr>"
        else:
            html += "<p style='color: #e74c3c;'><em>❌ No new C2C positions found in the last 24 hours matching your criteria.</em></p>"
        
        html += "<p style='color: #7f8c8d; font-size: 12px; margin-top: 30px;'>"
        html += "📊 This is an automated job scraper that runs daily at 8 AM UTC.<br>"
        html += "🔧 Target roles: DevOps Engineer, Site Reliability Engineer (SRE), Release Engineer<br>"
        html += "📍 Location: All United States<br>"
        html += "🔄 Refresh rate: Every 24 hours<br>"
        html += "Reply directly to this email or check the source site to apply."
        html += "</p>"
        html += "</body></html>"
        
        part = MIMEText(html, 'html')
        msg.attach(part)
        
        # Send using Gmail SMTP
        print("📧 Connecting to Gmail SMTP...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        
        print(f"✓ Email sent successfully to {RECIPIENT_EMAIL}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"✗ Gmail authentication failed: {e}")
        print("⚠️  Tip: Use an App Password (https://myaccount.google.com/apppasswords), not your regular password")
        return False
    except Exception as e:
        print(f"✗ Error sending email: {e}")
        return False

def main():
    print("🔍 Starting C2C Job Scraper")
    print("=" * 60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("🎯 Roles: DevOps Engineer, SRE, Release Engineer")
    print("📍 Location: United States (All)")
    print("⏱️  Time: Last 24 Hours")
    print("=" * 60)
    print()
    
    # Scrape jobs
    print("📍 Scraping ZipRecruiter...")
    zr_jobs = scrape_ziprecruiter()
    print(f"   ✓ Found {len(zr_jobs)} matching jobs\n")
    
    print("📍 Scraping Indeed...")
    indeed_jobs = scrape_indeed()
    print(f"   ✓ Found {len(indeed_jobs)} matching jobs\n")
    
    # Combine
    all_jobs = zr_jobs + indeed_jobs
    
    # Remove duplicates (same title + company)
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        key = (job['title'].lower(), job['company'].lower())
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)
    
    print(f"📊 Summary:")
    print(f"   ZipRecruiter: {len(zr_jobs)} jobs")
    print(f"   Indeed: {len(indeed_jobs)} jobs")
    print(f"   Total: {len(all_jobs)} jobs")
    print(f"   After deduplication: {len(unique_jobs)} unique jobs")
    print()
    
    # Send email
    print("📧 Sending email report...")
    if send_email_gmail(unique_jobs):
        print("✓ Report sent successfully!")
        sys.exit(0)
    else:
        print("✗ Failed to send email")
        sys.exit(1)

if __name__ == "__main__":
    main()
