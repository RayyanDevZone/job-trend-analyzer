import streamlit as st
import pandas as pd
import requests
import re
from config import APP_ID, APP_KEY, COUNTRY, SKILLS_LIST

# --- Cleaning Functions ---
def clean_text(text):
    text = re.sub(r'…+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_skills(text):
    text = text.lower()
    return [skill for skill in SKILLS_LIST if skill in text]

# --- Fetch Data from Adzuna API ---
def fetch_jobs_live(query, location, page=1):
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
    
    jobs = data.get("results", [])
    parsed = []
    for job in jobs:
        desc = clean_text(job.get("description", ""))
        parsed.append({
            'Title': job.get('title'),
            'Company': job.get('company', {}).get('display_name'),
            'Location': job.get('location', {}).get('display_name'),
            'Created': job.get('created'),
            'Skills Found': extract_skills(desc),
            'redirect_url': job.get('redirect_url')
        })
    
    return pd.DataFrame(parsed)

# --- Streamlit UI ---
st.title("🌍 Live Job Trends Search")

# --- Sidebar input ---
job_title = st.sidebar.text_input("Job Title", value="Data Scientist")
location = st.sidebar.text_input("Location", value="Bangalore")

if st.sidebar.button("Search Jobs"):
    with st.spinner("Fetching live data..."):
        df = fetch_jobs_live(job_title, location)

    if not df.empty:
        st.success(f"{len(df)} jobs found.")
        
        # Plot skills
        all_skills = sum(df['Skills Found'], [])
        skill_counts = pd.Series(all_skills).value_counts().head(10)
        st.bar_chart(skill_counts)

        # Format columns
        df['Apply'] = df['redirect_url'].apply(lambda url: f'<a href="{url}" target="_blank">Apply</a>')
        df['Skills Found'] = df['Skills Found'].apply(lambda x: ', '.join(x[:4]) + ('...' if len(x) > 4 else ''))
        df['Created'] = pd.to_datetime(df['Created']).dt.date

        # Display only required columns with correct names
        df_display = df[['Title', 'Company', 'Location', 'Created', 'Skills Found', 'Apply']]

        # Render styled HTML table
        st.markdown(
            df_display.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

        # Inject CSS to style specific columns
        st.markdown("""
            <style>
            table td:nth-child(4), table th:nth-child(4) {
                min-width: 100px;
                text-align: center;
            }
            table td:nth-child(1), table th:nth-child(1) {
                min-width: 150px;
                text-align: center;
            }
            </style>
        """, unsafe_allow_html=True)

    else:
        st.warning("No results found. Try a different search.")
