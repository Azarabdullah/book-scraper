import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_jobs(keyword="python"):
    print(f"\n Searching jobs for: {keyword}")
    print("-" * 50)

    url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={keyword}&txtLocation="

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # Step 1: Get the page
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # Step 2: find all job cards
    job_cards = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")

    jobs = []

    # Step 3: pull data from each card
    for card in job_cards[:10]:  # Only first 10 jobs
        try:
            title   = card.find("h2").text.strip()
            company = card.find("h3", class_="joblist-comp-name").text.strip()
            skills  = card.find("span", class_="srp-skills").text.strip()
            posted  = card.find("span", class_="sim-posted").text.strip()

            jobs.append({
                "Job Title" : title,
                "Company"   : company,
                "Skills"    : skills,
                "Posted"    : posted
            })

            # print each job clearly
            print(f"✅ {title}")
            print(f"    {company}")
            print(f"    {skills}")
            print(f"   {posted}")
            print()

        except:
            continue

    # Step 4: Save to Excel
    if jobs:
        df = pd.DataFrame(jobs)
        filename = f"{keyword}_jobs.csv"
        df.to_csv(filename, index=False)
        print(f" Saved {len(jobs)} jobs to '{filename}'")
    else:
        print("❌ No jobs found. Try a different keyword.")

#  RUN HERE — just change the keyword
scrape_jobs("python")
