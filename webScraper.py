"""
OnlineJobs.ph Data Analyst Job Scraper
=======================================
Scrapes job postings from onlinejobs.ph using the keyword "data analyst".
Extracts job details and matches skills, responsibilities, and qualifications
from each posting's description using keyword comparison.

Input:  onlinejobs.ph (live web scraping)
Output: jobs.csv

Dependencies: selenium, pandas, chromedriver
Run order:    01 - this is the first script
Author:       Your Name
Date:         2026-04-15
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# ── Configuration ─────────────────────────────────────────────────────────────

PATH = "C:\\Program Files (x86)\\chromedriver.exe"  # Update path if chromedriver moves
service = Service(PATH)
driver = webdriver.Chrome(service=service)

# ── Keyword Lists ─────────────────────────────────────────────────────────────
# Used to match against job description text (case-insensitive)
job_titles = ["Design", "book","graphic", "email", "SaaS", "E-commerce", "Amazon", "Airbnb", "Short-Term Rental", "STR", "Real Estate", "Healthcare", "Finance", "Marketing", "Advertising", "Social Media", "Instagram", "TikTok", "Google Ads", "Google Sheets", "Google Tag Manager", "GA4", "GoHighLevel", "HighLevel", "Airtable", "Salesforce", "SAP", "Amplitude", "Betfair", "Amazon FBA", "Amazon PPC", "Power BI", "Looker Studio", "AgencyAnalytics", "SEO", "PPC", "ERP", "API", "CRM", "ERD", "Skip Tracing", "Lead Gen", "Affiliate Marketing", "Media Buyer", "Call Center", "Construction", "Dental", "Property Management", "Stock", "Sports Betting", "Procurement", "Bookkeeping", "Accounting", "Auditing", "Field Service", "Digital Marketing", "Content Planning", "User Acquisition", "Revenue Share", "Virtual Assistant", "Data Analyst", "Senior", "Junior", "Data Scientist", "Business", "Analyst", "Data Engineer", "Financial", "Market", "Ecommerce", "Real Estate", "Medical", "Insurance", "Workforce", "Pricing", "Revenue", "Reporting", "Retention", "Research", "Operations", "Performance", "Data Specialist", "Data Solutions", "Data Systems", "Specialist", "Visual", "BI", "Power BI", "Annotation", "Labeling ", "Entry", "Inventory", "SEO", "PPC", "Social Media", "Creative", "Technical", "Quantitative", "Coordinator", "Associate", "Operations", "Automation", "Manager", "Strategy", "Intelligence", "KPI", "Insights", "FP&A", "M&A", "Sports", "Fractional", "CFO"]

# ── State ─────────────────────────────────────────────────────────────────────

df = []
countOfPost = 200  # Total number of job posts to scrape
currentCount = 0   # Tracks how many posts have been scraped so far

# ── Helper Functions ──────────────────────────────────────────────────────────

def comparison(description, keywords):
    """
    Checks which keywords from a list appear in the job description.

    Args:
        description (str): Full text of the job posting.
        keywords (list):   List of keywords to search for.

    Returns:
        list: Keywords found in the description (case-insensitive match).
    """
    found = []
    for word in keywords:
        if word.lower() in description.lower():
            found.append(word)
    return found


def pageScrape():
    """
    Scrapes job details from the current page of search results.
    Visits each job post link, extracts structured fields, and appends
    a row to the global df list.

    Modifies globals: df, currentCount
    Stops collecting links once countOfPost is reached.
    """
    global currentCount, countOfPost

    # Collect links first to avoid stale element issues after navigation
    listOfLinks = []
    for post in posts:
        if currentCount < countOfPost:
            link = post.find_element(By.TAG_NAME, 'a')
            listOfLinks.append(link.get_attribute("href"))
            print(currentCount)
            currentCount += 1

    for link in listOfLinks:
        driver.get(link)

        # CSS selector targets the detail fields in order: type, salary, hours, date
        details = driver.find_elements(By.CSS_SELECTOR, "p.fs-18")

        job_title = driver.find_element(By.CSS_SELECTOR, "h1.job__title").text
        job_type  = details[0].text
        salary    = details[1].text
        hours     = details[2].text
        date      = details[3].text
        description = driver.find_element(By.ID, "job-description").text

        df.append({
            "Date":            date,
            "Job_title":       comparison(job_title, job_titles),
            "Job_type":        job_type,
            "Salary":          salary,
            "Hours":           hours,
            "Description":     description,
            #"Skills":          comparison(description, skills),
            #"Responsibilities": comparison(description, responsibility),
            #"Qualifications":  comparison(description, qualifications),
            "Link": link
        })

        #print(job_type, salary, hours, date)
        print(job_title)
        driver.back()

# ── Main Scraping Loop ────────────────────────────────────────────────────────

driver.get("https://www.onlinejobs.ph/")

# Search for data analyst postings
keywords = driver.find_element(By.NAME, "jobkeyword")
keywords.send_keys("data analyst")
keywords.send_keys(Keys.RETURN)

while currentCount < countOfPost:
    try:
        # Wait up to 10s for job results container to load
        divResults = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "results"))
        )
    except Exception as e:
        print(f"Page failed to load: {e}")
        driver.quit()
        break

    posts = divResults.find_elements(By.CLASS_NAME, "jobpost-cat-box")
    pageScrape()

    # Move to next page of results
    next_button = driver.find_element(By.CSS_SELECTOR, "a[rel='next']")
    next_button.click()

# ── Export ────────────────────────────────────────────────────────────────────

df = pd.DataFrame(df)
df.to_csv("raw_datas_job_postings.csv", index=False)
print(f"Saved {len(df)} job postings to jobs.csv")

time.sleep(10)  # Brief pause before browser closes