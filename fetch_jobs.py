import requests
import pandas as pd
from config import APP_ID, APP_KEY, COUNTRY, DEFAULT_QUERY, DEFAULT_LOCATION

def fetch_jobs(query=DEFAULT_QUERY, location=DEFAULT_LOCATION, page=1):
    url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/{page}"
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
    
    # Parse response into list of jobs
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
    print("Jobs saved to jobs_data.csv")

# If you want to run directly:
if __name__ == "__main__":
    fetch_jobs()
