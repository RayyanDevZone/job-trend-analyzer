import requests
import pandas as pd
import argparse
from config import APP_ID, APP_KEY, DEFAULT_QUERY, DEFAULT_LOCATION

def fetch_jobs(query=DEFAULT_QUERY, location=DEFAULT_LOCATION, country_code="in", page=1):
    url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/{page}"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": query,
        "where": location,
        "results_per_page": 10,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params)
    data = response.json()

    jobs = data.get("results", [])
    parsed = []
    for job in jobs:
        parsed.append({
            'job_id': job.get('id'),
            'title': job.get('title'),
            'company': job.get('company', {}).get('display_name'),
            'location': job.get('location', {}).get('display_name'),
            'created': job.get('created'),
            'description': job.get('description'),
            'redirect_url': job.get('redirect_url'),
            'category': job.get('category', {}).get('label'),
            'salary_predicted': job.get('salary_is_predicted')
        })

    df = pd.DataFrame(parsed)
    df.to_csv("jobs_data.csv", index=False)
    print(f"✅ {len(df)} jobs saved to jobs_data.csv for {query} in {location} ({country_code.upper()})")

# Command-line usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default=DEFAULT_QUERY, help="Job title to search")
    parser.add_argument("--location", default=DEFAULT_LOCATION, help="City or location name")
    parser.add_argument("--country", default="in", help="2-letter country code (e.g., 'in', 'us', 'au')")
    args = parser.parse_args()

    fetch_jobs(query=args.query, location=args.location, country_code=args.country)
